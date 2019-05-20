from queue import Queue
from unittest.mock import MagicMock

import numpy as np

from python.infrastructure.filesystem.capture import AsyncCapture, AsyncFileSystemCaptureContext


def test_async_capture_should_add_job_to_queue_when_saving_image():
    # Given
    rgb_data = np.array([[[1, 2, 3]]])
    filename = "test.png"
    expected_job = (rgb_data, filename)
    queue = Queue()
    capture = AsyncCapture(capture_stream=True, queue=queue)

    # When
    capture.save_image(rgb_data, filename)

    # Then
    actual_job = queue.get()
    assert actual_job == expected_job


def test_async_capture_should_not_add_job_to_queue_when_capture_is_disabled():
    # Given
    rgb_data = np.array([[[1, 2, 3]]])
    filename = "test.png"
    queue = Queue()
    capture = AsyncCapture(capture_stream=False, queue=queue)

    # When
    capture.save_image(rgb_data, filename)

    # Then
    assert queue.empty()


def test_capture_manager_should_return_capture_object():
    # Given
    writer = MagicMock()
    expected_capture = MagicMock()

    # When
    with AsyncFileSystemCaptureContext(expected_capture, writer) as actual_capture:
        # Then
        assert actual_capture == expected_capture


def test_capture_manager_should_start_writer_and_close_context():
    # Given
    writer = MagicMock()
    expected_capture = MagicMock()

    # When
    with AsyncFileSystemCaptureContext(expected_capture, writer):
        # Then
        writer.start.assert_called_once()
        writer.shutdown.assert_not_called()

    # And Then
    writer.shutdown.assert_called_once()
