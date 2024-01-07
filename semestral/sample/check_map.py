""" File that contains funtion for checking if created map has correct format. """


def check_map(game_map: list, path: str) -> None:
    """Helping function that checks, if game_map is in given format.

    Args:
        game_map (list): 2D list that represents maze.
        path (str): name of file for printing if error found.

    Raises:
        AssertionError: If map does not have correct format. Also message with type of error provided in AssertionError.args[0]

    """
    height = len(game_map)
    assert height > 0, f'It is impossible for map to have height 0. Check if {path} was damaged.'

    width = len(game_map[0])
    assert height > 3 and width > 3, f'It is impossible for map to have height <= 3. Check if {path} was damaged.'

    for i in range(height):
        assert len(game_map[i]) == width, f'Map does not have rectangle shape. Check if {path} was damaged.'

    for j in range(width):
        assert game_map[0][j] == '#' and game_map[height - 1][j] == '#', f'Borders are not filled with \'#\'. Check if {path} was damaged.'
    for i in range(height):
        assert game_map[i][0] == '#' and game_map[i][width - 1] == '#', f'Borders are not filled with \'#\'. Check if {path} was damaged.'

    p_cnt = 0
    e_cnt = 0
    allowed_s = [' ', '#', 'b', 'y', 'p', 'B', 'Y', 'P', 'H', 'V', 'R']
    for i in range(height):
        for j in range(width):
            if game_map[i][j] == '@':
                p_cnt += 1
            elif game_map[i][j] == 'E':
                e_cnt += 1
            else:
                assert game_map[i][j] in allowed_s, f'Unexpected symbol {game_map[i][j]} on position ({i + 1},{j + 1}). Check if {path} was damaged.'
    assert p_cnt == 1, f'Wrong amount of players: {p_cnt}. Check if {path} was damaged.'
    assert e_cnt != 0, f'Wrong amount of exits: {e_cnt}. Check if {path} was damaged.'
