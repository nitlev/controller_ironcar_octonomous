import logging
import multiprocessing
import time
from queue import Queue

import numpy as np

from python.domain.capture import Capture
from python.infrastructure.filesystem.directory import create_output_dir

logger = logging.getLogger('controller_ironcar')


def open_capture(output_dir, capture_stream=False):
    manager = multiprocessing.Manager()
    image_queue = manager.Queue()

    if type(output_dir) == str:
        output_dir = create_output_dir(output_dir)

    writer = WriterProcess(output_dir, image_queue=image_queue)
    capture = AsyncCapture(capture_stream, image_queue)
    return AsyncFileSystemCaptureContext(capture, writer)


class AsyncFileSystemCaptureContext:
    def __init__(self, capture, writer):
        self.capture = capture
        self.writer = writer

    def __enter__(self) -> Capture:
        logger.debug("Starting capture writer subprocess")
        self.writer.start()
        time.sleep(1)
        return self.capture

    def __exit__(self, exc_type, exc_val, exc_tb) -> None:
        self.writer.shutdown()
        self.writer.join()
        logger.debug("Capture writer subprocess has been stopped")


class AsyncCapture(Capture):
    def __init__(self, capture_stream, queue: Queue):
        super().__init__(capture_stream)
        self.queue = queue

    def save_image(self, rgb_data: np.ndarray, filename: str) -> None:
        if self.capture_stream:
            self.queue.put((rgb_data, filename))


class WriterProcess(multiprocessing.Process):
    def __init__(self, output_dir, image_queue):
        multiprocessing.Process.__init__(self)
        self.output_dir = output_dir
        self.queue = image_queue
        self.exit = multiprocessing.Event()

    def run(self):
        while not self.exit.is_set():
            rgb_data, filename = self.queue.get()
            self.output_dir.save_image(rgb_data, filename)

    def shutdown(self):
        self.exit.set()
