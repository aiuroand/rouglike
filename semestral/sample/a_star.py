""" File that contains implementation of A* algorithm for 2d maze.
    Inspired by https://levelup.gitconnected.com/a-star-a-search-for-solving-a-maze-using-python-with-visualization-b0cae1c3ba92 """


from queue import PriorityQueue


def calculate_manhattan(cell1: tuple, cell2: tuple):
    """ Returns manhattan distance between 2 2d points.

    Args:
        cell1 (_type_): _description_
        cell2 (_type_): _description_

    Returns:
        _type_: _description_
    """
    return abs(cell1[0] - cell2[0]) + abs(cell1[1] - cell2[1])


def a_star(game_map, start, finish):
    height = len(game_map)
    width = len(game_map[0])
    g_score = []
    f_score = []
    for i in range(height):
        g_score.append([])
        f_score.append([])
        for j in range(width):
            g_score[i].append(float('inf'))
            f_score[i].append(float('inf'))
    g_score[start[0]][start[1]] = 0
    f_score[start[0]][start[1]] = calculate_manhattan(start, (1, 8))

    q = PriorityQueue()
    q.put((0 + calculate_manhattan(start, finish),
           calculate_manhattan(start, finish),
           start))

    aPath = {}
    found = False
    while not q.empty():
        curr_cell = q.get()[2]
        if curr_cell == finish:
            found = True
            break
        for d in 'ESNW':
            if d == 'E':
                child_cell = (curr_cell[0], curr_cell[1] + 1)
            elif d == 'W':
                child_cell = (curr_cell[0], curr_cell[1] - 1)
            elif d == 'N':
                child_cell = (curr_cell[0] - 1, curr_cell[1])
            else:
                child_cell = (curr_cell[0] + 1, curr_cell[1])

            if game_map[child_cell[0]][child_cell[1]] == ' ':
                temp_g_score = g_score[curr_cell[0]][curr_cell[1]] + 1
                temp_f_score = temp_g_score + calculate_manhattan(child_cell, finish)
                if temp_f_score < f_score[child_cell[0]][child_cell[1]]:
                    g_score[child_cell[0]][child_cell[1]] = temp_g_score
                    f_score[child_cell[0]][child_cell[1]] = temp_f_score
                    q.put((temp_f_score, calculate_manhattan(child_cell, finish), child_cell))
                    aPath[child_cell] = curr_cell
    if not found:
        return []
    fwd_path = []
    cell = finish
    while cell != start:
        fwd_path.append(aPath[cell])
        cell = aPath[cell]
    return fwd_path[::-1] + [finish]


assert (__name__ != "__main__")
