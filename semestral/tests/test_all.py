import pytest
import pycodestyle
import os
import sys

sys.path.append('..')
from semestral.sample.check_map import check_map


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


@pytest.mark.parametrize('map_path',
                         ['tests/bad_maps/void.txt',
                          'tests/bad_maps/wrong_border1.txt',
                          'tests/bad_maps/wrong_border2.txt',
                          'tests/bad_maps/wrong_border3.txt',
                          'tests/bad_maps/wrong_border4.txt',
                          'tests/bad_maps/zero_players.txt',
                          'tests/bad_maps/many_players.txt',
                          'tests/bad_maps/zero_exits.txt',
                          'tests/bad_maps/wrong_symb1.txt',
                          'tests/bad_maps/wrong_symb2.txt',
                          'tests/bad_maps/small_size.txt'])
def test_map(map_path):
    game_map = []
    with open(map_path, 'r') as f:
        for line in f.readlines():
            row = [i for i in line][:-1]
            game_map.append(row)
    try:
        check_map(game_map, map_path)
    except AssertionError as e:
        pass
    except:
        assert False, f'Wrong error type for {map_path}'
    else:
        assert False, f'Nothing was raised for {map_path}'