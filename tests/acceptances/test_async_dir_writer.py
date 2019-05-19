import multiprocessing
import os
import tempfile
import time

import numpy as np

from python.infrastructure.filesystem.capture import WriterProcess
from python.infrastructure.filesystem.directory import FileSystemDirectory


def test_writer_is_able_to_write_to_directory():
    # Given
    with tempfile.TemporaryDirectory() as tmpdir:
        print(tmpdir)
        rgb_data = np.array([[[0, 0, 0]]])
        filename = "test.png"
        expected_file_name = os.path.join(tmpdir, filename)
        output_dir = FileSystemDirectory(tmpdir)
        manager = multiprocessing.Manager()
        queue = manager.Queue()
        writer = WriterProcess(output_dir, queue)
        writer.start()
        time.sleep(1)

        # When
        queue.put((rgb_data, filename))
        writer.shutdown()
        writer.join()

        # Then
        assert os.path.isfile(expected_file_name)
