import unittest
import os
import sys

from copa_transparente.tests import JSONTestRunner

if __name__ == "__main__":
    loader = unittest.TestLoader()
    JSONTestRunner().run(loader.discover('copa_transparente/tests/'))
