from abc import ABCMeta, abstractmethod

from python.domain.imagestream import ImageStream


class Camera:
    __metaclass__ = ABCMeta

    @abstractmethod
    def image_stream(self) -> ImageStream:
        raise NotImplementedError
