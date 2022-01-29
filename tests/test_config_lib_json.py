# -*- coding: utf-8 -*-

import os
import pytest
from configirl import (
    read_text, write_text,
)

dir_here = os.path.dirname(os.path.abspath(__file__))
path_temp_file = os.path.join(dir_here, "tmp.txt")


def test_read_write_text():
    write_text("hello world!", path_temp_file)
    assert read_text(path_temp_file) == "hello world!"


if __name__ == "__main__":
    import os

    basename = os.path.basename(__file__)
    pytest.main([basename, "-s", "--tb=native"])
