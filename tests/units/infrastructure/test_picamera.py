from io import BytesIO
from unittest.mock import MagicMock

from python.infrastructure.picamera import PiCameraImageStream


def test_picamera_image_stream_is_iterable():
    # Given
    camera = MagicMock()
    resolution = (10, 10)
    output_stream = BytesIO()

    # Then
    assert iter(PiCameraImageStream(camera, resolution, output_stream))


def test_picamera_image_stream_resets_stream_after_each_loop():
    # Given
    camera = MagicMock()
    camera.capture_continuous.return_value = range(3)
    resolution = (10, 10)
    output_stream = MagicMock()

    # When
    for _ in PiCameraImageStream(camera, resolution, output_stream):
        pass

    # Then
    assert output_stream.truncate.call_count == 3
    assert output_stream.seek.call_count == 3
