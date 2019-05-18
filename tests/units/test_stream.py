from unittest.mock import MagicMock

import numpy as np

from python.domain.directory import Directory
from python.domain.imagestream import SavedImageStream


def test_saved_stream_save_the_image_of_the_input_stream():
    # Given
    expected_image_name = "0.png"
    rgb_array = np.array([[[255] * 3] * 100] * 100)
    pict = MagicMock(array=rgb_array)
    input_stream = [pict]
    output_dir = MagicMock(Directory)
    stream = SavedImageStream(input_stream, output_dir)

    # When
    _ = next(stream)

    # Then
    output_dir.save_image.assert_called_once_with(rgb_data=rgb_array, filename=expected_image_name)
