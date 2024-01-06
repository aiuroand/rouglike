""" File that contains starting poinf of a program. """


import os

from loop import Loop


def main():
    settings_path = os.path.relpath('src/settings.conf')
    game_loop = Loop(settings_path)
    game_loop.loop()


if __name__ == "__main__":
    main()
