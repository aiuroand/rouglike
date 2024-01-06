import pytest
import pycodestyle
import os

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

# def code_style(d):
#     style = pycodestyle.StyleGuide()
#     style.check_files('sample/main.py')
#     pycodestyle('sample/main.py')
    
# directory_path = 'sample/'
# code_style(directory_path)
# @pytest.fixture(scope="session")
# def linter():
#     """ Test codestyle for files in sample folder. """
#     src_file = inspect.getfile(main)
#     rep = CollectingReporter()
#     # disabled warnings:
#     # 0301 line too long
#     # 0103 variables name (does not like shorter than 2 chars)
#     r = Run(['--disable=C0301,C0103 ', '-sn', src_file], reporter=rep, exit=False)
#     return r.linter