class WrongPlayersAmount(Exception):
    def __init__(self, str):
        self.message = str

class MapAmount(Exception):
    def __init__(self, str):
        self.message = str