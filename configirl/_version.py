# -*- coding: utf-8 -*-

import os
import sys

sys.path.append(os.path.dirname(__file__))

from __init__ import __version__

if __name__ == "__main__":  # pragma: no cover
    print(__version__)
