from python.domain.camera import Camera
from python.domain.imagestream import ImageStream

try:
    import picamera.array
except ImportError:
    print("Can't import picamera, "
          "you probably should be running this on the IronCar or install the "
          "picamera library")


class PiCamera(Camera):
    def __init__(self, resolution, preview=False):
        super().__init__()
        self.resolution = resolution
        self._cam = picamera.PiCamera(resolution=resolution, framerate=60)
        self._cam.awb_mode = 'auto'

        if preview:
            self._cam.start_preview()

    def image_stream(self):
        stream = PiCameraImageStream(self._cam, self.resolution)
        return stream


class PiCameraImageStream(ImageStream):
    def __init__(self, camera, resolution, output_stream=None):
        self._camera = camera
        self._cam_output = output_stream or picamera.array.PiRGBArray(camera, size=resolution)
        self._stream = self._camera.capture_continuous(self._cam_output, format='rgb', use_video_port=True)

    def __iter__(self):
        for pict in self._stream:
            try:
                yield pict
            finally:
                self._cam_output.truncate(0)
                self._cam_output.seek(0)
