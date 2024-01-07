""" File that contains all user-made exceptions """


class MapAmount(Exception):
    """Exception that is raised if maps directory has wrong amount of maps.
    """
    def __init__(self, str: str):
        """Constructor

        Args:
            str (str): Exception message
        """
        self.message = str


assert (__name__ != "__main__")
