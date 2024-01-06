""" File that contains all user-made exceptions """


class WrongPlayersAmount(Exception):
    def __init__(self, str):
        self.message = str


class MapAmount(Exception):
    def __init__(self, str):
        self.message = str


assert (__name__ != "__main__")
