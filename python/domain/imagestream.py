import logging
from abc import ABCMeta, abstractmethod

logger = logging.getLogger('controller_ironcar')


class ImageStream:
    __metaclass__ = ABCMeta

    @abstractmethod
    def __iter__(self):
        raise NotImplementedError
