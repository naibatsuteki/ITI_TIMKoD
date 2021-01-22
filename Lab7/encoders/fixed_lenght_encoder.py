import math

import bitarray as ba

from Lab7.encoders.basic_encoder import BasicEncoder


class FixedLengthEncoder(BasicEncoder):

    def __init__(self):
        super().__init__()

    @staticmethod
    def code_generator(code_length, power_factor=2):
        for i in range(int(math.pow(power_factor, code_length))):
            yield ba.bitarray(f"{i:0{code_length}b}")

    def create(self, text: str) -> None:
        """
        docstring
        """
        characters = ''.join(sorted(set(text)))
        code_length = math.ceil(math.log2(len(characters)))
        generator = self.code_generator(code_length)
        self.code = {char: generator.__next__() for char in characters}

    def encode(self, text: str) -> ba.bitarray:
        """
        docstring
        """
        result = ba.bitarray()
        result.encode(self.code, text)
        return result

    def decode(self, coded_text: ba.bitarray) -> str:
        """
        docstring
        """
        return ''.join(coded_text.decode(self.code))


if __name__ == '__main__':
    encoder = FixedLengthEncoder()
    original_text = "ala ma kota"
    encoder.create(original_text)
    encoded_text = encoder.encode(original_text)
    decoded_text = encoder.decode(encoded_text)
    assert original_text == decoded_text
