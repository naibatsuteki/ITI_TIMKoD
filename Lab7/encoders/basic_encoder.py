import json
from abc import abstractmethod

import bitarray as ba


class BasicEncoder:

    def __init__(self):
        self.code = {}

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

    def save(self, code_path: str, file_path, encoded_file: ba.bitarray) -> None:
        """
        docstring
        """
        self._save_code(code_path)
        self._save_encoded_file(file_path, encoded_file)

    def _save_code(self, path: str) -> None:
        """
        docstring
        """
        save_code = {key: value.to01() for key, value in self.code.items()}
        with open(path, 'w') as file:
            json_str = json.dumps(save_code)
            file.write(json_str)

    @staticmethod
    def _save_encoded_file(path: str, encoded_file: ba.bitarray) -> None:
        """
        docstring
        """
        with open(path, 'wb') as file:
            encoded_file.tofile(file)

    def load(self, code_path: str, file_path: str) -> ba.bitarray:
        """
        docstring
        """
        self._load_code(code_path)
        return self._load_encoded_file(file_path)

    def _load_code(self, path: str) -> None:
        """
        docstring
        """
        with open(path, 'r') as file:
            loaded_dict = json.load(file)
            self.code = {key: ba.bitarray(value) for key, value in loaded_dict.items()}

    @staticmethod
    def _load_encoded_file(path: str) -> ba.bitarray:
        """
        docstring
        """
        with open(path, 'rb') as file:
            a = file.read()
            loading_buffer = ba.bitarray()
            loading_buffer.frombytes(a)
            return loading_buffer
