
import pytest
import inspect
import pycodestyle
import os

@pytest.fixture
def test_file(path=''):
    style = pycodestyle.StyleGuide()
    print(f'Testing {path}')
    res = style.check_files([path])
    return(res.total_errors)


def test_pep8(dir='sample/'):
    files = [dir + f for f in os.listdir(dir) if f.endswith('.py')]
    for f in files:
        assert(test_file(f) == 0)

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


# # @pytest.mark.parametrize("limit", range(0, 11))
# # def test_codestyle_score(linter, limit, runs=[]):
# #     """ Evaluate codestyle for different thresholds. """
# #     if len(runs) == 0:
# #         print('\nLinter output:')
# #         for m in linter.reporter.messages:
# #             print(f'{m.msg_id} ({m.symbol}) line {m.line}: {m.msg}')
# #     runs.append(limit)
# #     # score = linter.stats['global_note']
# #     score = linter.stats.global_note

# #     print(f'pylint score = {score} limit = {limit}')
# #     assert score >= limit