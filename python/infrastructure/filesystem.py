import logging
import os
from datetime import datetime

import numpy as np
from PIL import Image

from python.domain.directory import Directory

logger = logging.getLogger('controller_ironcar')


class FileSystemDirectory(Directory):
    def __init__(self, path):
        super().__init__(path)

    def save_image(self, rgb_data: np.ndarray, filename: str) -> None:
        image = Image.fromarray(rgb_data, "RGB")
        filepath = os.path.join(self.path, filename)
        image.save(filepath)

    def ensure_exists(self):
        os.makedirs(self.path)

    def __str__(self):
        return self.path


def create_output_dir(path: str, subdir=None):
    if subdir is None:
        date = datetime.now()
        timestamp = (date - datetime(1970, 1, 1)).total_seconds()
        subdir = '{}'.format(timestamp)
    output_dir = FileSystemDirectory(os.path.join(path, subdir))
    logger.info("create output_dir={output_dir}".format(output_dir=output_dir))
    output_dir.ensure_exists()
    return output_dir
