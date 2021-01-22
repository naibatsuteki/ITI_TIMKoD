from abc import abstractmethod

import bitarray as ba


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
    def encode(self, text: str) -> ba.bitarray:
        """
        docstring
        """
        raise NotImplementedError

    @abstractmethod
    def decode(self, coded_text: ba.bitarray) -> str:
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
