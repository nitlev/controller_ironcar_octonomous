import logging
from abc import ABCMeta, abstractmethod
from collections import Iterator

logger = logging.getLogger('controller_ironcar')


class ImageStream(Iterator):
    __metaclass__ = ABCMeta

    @abstractmethod
    def __next__(self):
        raise NotImplementedError


class SavedImageStream(ImageStream):
    def __init__(self, stream, output_dir):
        self._stream = enumerate(iter(stream))
        self._output_dir = output_dir

    def __iter__(self):
        return self

    def __next__(self):
        index_capture, pict = next(self._stream)
        filename = '{name}.png'.format(name=index_capture)
        logger.debug('Saving camera output filename={filename}'.format(filename=filename))
        self._save_image(filename, index_capture, pict)
        return pict

    def _save_image(self, filename, index_capture, pict):
        try:
            self._output_dir.save_image(rgb_data=pict.array, filename=filename)
        except Exception as exception:
            logger.warning('Camera output capture failed - index_capture={}'.format(index_capture))
            logger.warning('exception={}'.format(exception))
