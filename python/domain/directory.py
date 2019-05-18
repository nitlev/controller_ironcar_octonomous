from abc import ABCMeta, abstractmethod

import numpy as np


class Directory:
    __metaclass__ = ABCMeta

    def __init__(self, path):
        self.path = path

    @abstractmethod
    def save_image(self, rgb_data: np.ndarray, filename: str) -> None:
        raise NotImplementedError

    @abstractmethod
    def ensure_exists(self) -> None:
        raise NotImplementedError
