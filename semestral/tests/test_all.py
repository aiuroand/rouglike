import pytest
import pycodestyle
import os

from sample.game import Game


@pytest.mark.skip(reason='Helping function')
def test_file(path=''):
    style = pycodestyle.StyleGuide()
    style.options.ignore = 'E501'
    res = style.check_files([path])
    return(res.total_errors)


def test_pep8(dir='sample/'):
    files = [dir + f for f in os.listdir(dir) if f.endswith('.py')]
    for f in files:
        print(f'Testing {f}')
        assert test_file(f) == 0, f'{f} has no correct PEP8 format'


def map_test():