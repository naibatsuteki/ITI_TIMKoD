import math

from Lab7.encoders.basic_encoder import BasicEncoder


class FixedLengthEncoder(BasicEncoder):

    def __init__(self):
        super().__init__()

    @staticmethod
    def code_generator(code_length, power_factor=2):
        for i in range(int(math.pow(power_factor, code_length))):
            yield f"{i:0{code_length}b}"

    def create(self, text: str):
        """
        docstring
        """
        characters = ''.join(sorted(set(text)))
        code_length = math.ceil(math.log2(len(characters)))
        generator = self.code_generator(code_length)
        self.code = {char: generator.__next__() for char in characters}

    def encode(self):
        """
        docstring
        """
        raise NotImplementedError

    def decode(self):
        """
        docstring
        """
        raise NotImplementedError


if __name__ == '__main__':
    encoder = FixedLengthEncoder()
    encoder.create("ala ma kota")
