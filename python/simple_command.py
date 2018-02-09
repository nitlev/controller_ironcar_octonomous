import logging
import time
from argparse import ArgumentParser
from os.path import isfile

import Adafruit_PCA9685
import numpy as np
import picamera.array

DEFAULT_RESOLUTION = 240, 176
DEFAULT_MODEL_PATH = '/home/pi/ironcar/autopilots/my_autopilot_big.hdf5'
DEFAULT_SPEED = 0.2
DEFAULT_PREVIEW = False
DEFAULT_LOG_LEVEL = "INFO"

XTREM_DIRECTION_SPEED_COEFFICIENT = 1
DIRECTION_SPEED_COEFFICIENT = 1
STRAIGHT_COEFFICIENT = 1.5

CROPPED_LINES = 53


def main():
    kwargs = load_args()
    set_log_level(kwargs)

    logging.info("INPUTS: ")
    logging.info(kwargs)
    run(**kwargs)


def set_log_level(kwargs):
    log_level = getattr(logging, kwargs.pop("loglevel").upper())
    logging.basicConfig(level=log_level)


def load_args():
    parser = ArgumentParser(description='Control the OCTONOMOUS OCTOCAR.')
    parser.add_argument('--resolution', '-r', dest='resolution',
                        type=int, nargs=2,
                        default=DEFAULT_RESOLUTION,
                        help='the (width, height) resolution')
    parser.add_argument('--model-path', '-m', dest='path',
                        type=str, nargs=1,
                        default=DEFAULT_MODEL_PATH,
                        help='absolute path to the model')
    parser.add_argument('--speed', '-s', dest='speed',
                        type=float, default=DEFAULT_SPEED,
                        help='the car speed (ratio to max speed, from 0 to 1)')
    parser.add_argument('--preview', '-p', dest='preview',
                        action='store_true', default=DEFAULT_PREVIEW,
                        help='if given, camera input will be displayed')
    parser.add_argument('--log-level', '-l', dest='loglevel',
                        type=str, nargs=1,
                        default=DEFAULT_LOG_LEVEL,
                        help='the log level used (from CRITICAL to DEBUG)')

    args = parser.parse_args()
    check_valid_args(args)
    return extract_values(args)


def check_valid_args(args):
    assert isfile(args.path), "Model must exist"


def extract_values(args):
    return {
        "resolution": tuple(args.resolution),
        "model_path": args.path,
        "speed": int(400 + 100 * args.speed),
        "preview": args.preview,
        "loglevel": args.loglevel,
    }


def run(resolution, model_path, speed, preview):
    from keras.models import load_model

    # Objects Initialisation
    # Camera
    cam, cam_output, stream = init_cam(resolution)
    # Model
    model_mlg = load_model(model_path)
    # Arduino
    pwm = Adafruit_PCA9685.PCA9685()
    pwm.set_pwm_freq(60)

    # Start loop
    if preview:
        cam.start_preview()
    timer(seconds=5)
    start_run(stream, pwm, model_mlg, cam_output, speed)


def timer(seconds=5):
    for i in range(seconds, 0, -1):
        logging.info("Starting in {}".format(i))
        time.sleep(1)
    logging.info("GO !")


def init_cam(resolution=(250, 70)):
    cam = picamera.PiCamera(resolution=resolution, framerate=60)
    cam_output = picamera.array.PiRGBArray(cam, size=resolution)
    stream = cam.capture_continuous(cam_output, format='rgb',
                                    use_video_port=True)
    return cam, cam_output, stream


def start_run(stream, pwm, model_mlg, cam_output, speed):
    start = time.time()
    for i, pict in enumerate(stream):
        try:
            control_car(pwm, pict, model_mlg, speed)
            cam_output.truncate(0)
        except KeyboardInterrupt:
            stop = time.time()
            elapsed_time = stop - start
            logging.info("Image per second: {}".format(i / elapsed_time))
            time.sleep(2)
            stop_car(pwm)
            break
        except Exception:
            stop_car(pwm)
            raise


def control_car(pwm, pict, model_mlg, speed):
    pred = model_mlg.predict(np.array([pict.array[CROPPED_LINES:, :, :]]))
    logging.info(pred)
    direction = direction_command_from_pred(pred)
    pwm.set_pwm(2, 0, direction)
    pwm.set_pwm(1, 0, int(speed_control(direction, speed)))


def direction_command_from_pred(pred):
    command = {
        0: 470,
        1: 420,
        2: 370,
        3: 305,
        4: 240
    }
    direction = command[np.argmax(pred)]
    return direction


def speed_control(direction, speed):
    if direction == 470 or direction == 240:
        return speed * XTREM_DIRECTION_SPEED_COEFFICIENT
    elif direction == 420 or direction == 305:
        return speed * DIRECTION_SPEED_COEFFICIENT
    else:
        return speed * STRAIGHT_COEFFICIENT


def stop_car(pwm):
    pwm.set_pwm(1, 0, 400)
    pwm.set_pwm(2, 0, 400)


if __name__ == '__main__':
    main()
