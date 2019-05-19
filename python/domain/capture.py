from abc import ABCMeta, abstractmethod

import numpy as np


class Capture:
    __metaclass__ = ABCMeta

    def __init__(self, capture_stream=False):
        self.capture_stream = capture_stream

    @abstractmethod
    def save_image(self, rgb_data: np.ndarray, filename: str) -> None:
        raise NotImplementedError

    @abstractmethod
    def __enter__(self):
        raise NotImplementedError

    @abstractmethod
    def __exit__(self, exc_type, exc_val, exc_tb) -> None:
        raise NotImplementedError
