import unittest
import os
import sys

from copa_transparente.tests import JSONTestRunner

try:
    import coverage
except:
    coverage = None

if __name__ == "__main__":
    if coverage:
        cov = coverage.coverage(branch=True, source=['copa_transparente'])
        cov.start()

    loader = unittest.TestLoader()
    JSONTestRunner().run(loader.discover('copa_transparente/tests/'))

    if coverage:
        cov.stop()
        cov.save()
        cov.html_report(directory='htmlcov')
        cov.report(show_missing=False)
