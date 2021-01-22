from abc import abstractmethod


class BasicEncoder:

    def __init__(self):
        self.code = None

    @abstractmethod
    def create(self, text: str) -> None:
        """
        docstring
        """
        raise NotImplementedError

    @abstractmethod
    def encode(self):
        """
        docstring
        """
        raise NotImplementedError

    @abstractmethod
    def decode(self):
        """
        docstring
        """
        raise NotImplementedError

    def save(self):
        """
        docstring
        """
        raise NotImplementedError

    def load(self):
        """
        docstring
        """
        raise NotImplementedError
