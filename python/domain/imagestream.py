import logging
from abc import ABCMeta, abstractmethod

logger = logging.getLogger('controller_ironcar')


class ImageStream:
    __metaclass__ = ABCMeta

    @abstractmethod
    def __iter__(self):
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
        self._save_image(filename, index_capture, pict)
        return pict

    def _save_image(self, filename, index_capture, pict):
        logger.debug('Saving camera output filename={filename}'.format(filename=filename))
        try:
            self._output_dir.save_image(rgb_data=pict.array, filename=filename)
        except Exception as exception:
            logger.warning('Camera output capture failed - index_capture={}'.format(index_capture))
            logger.warning('exception={}'.format(exception))
