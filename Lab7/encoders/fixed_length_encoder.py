import math
import random
import bitarray as ba

from encoders.basic_encoder import BasicEncoder


class FixedLengthEncoder(BasicEncoder):

    def __init__(self):
        super().__init__()
        self.code_length = None

    @staticmethod
    def code_generator(code_length, power_factor=2):
        for i in range(0, int(math.pow(power_factor, code_length))):
            yield ba.bitarray(f"{i:0{code_length}b}")

    def create(self, text: str) -> None:
        """
        docstring
        """
        characters = ''.join(sorted(set(text)))
        self.code_length = math.ceil(math.log2(len(characters)))
        generator = self.code_generator(self.code_length)
        self.code = {char: generator.__next__() for char in characters}

    def encode(self, text: str) -> ba.bitarray:
        """
        docstring
        """
        result = ba.bitarray()
        for c in text:
            result.extend(self.code[c])
        return result

    def decode(self, coded_text: ba.bitarray) -> str:
        """
        docstring
        """
        reversed_dict = {v.to01(): k for k, v in self.code.items()}
        result = []
        for i in range(0, coded_text.length(), self.code_length):
            try:
                char_code = coded_text[i:i + self.code_length].to01()
                result.append(reversed_dict[char_code])
            except KeyError:
                continue
        return ''.join(result)

    def _load_code(self, path: str) -> None:
        # Fixed length code specific
        super(FixedLengthEncoder, self)._load_code(path)
        # Get any key. All codes have the same length.
        self.code_length = len(random.choice(list(self.code.values())))


# Local testing
if __name__ == '__main__':
    from os import path as osp
    code_path = osp.join('outputs', 'test_fixed_length_code.json')
    file_path = osp.join('outputs', 'test_file.fixed_length')
    original_text = 'ala ma kota'
    encoder = FixedLengthEncoder()
    encoder.create(original_text)
    encoded_text = encoder.encode(original_text)
    encoder.save(code_path, file_path, encoded_text)
    encoder.code = None
    loaded_text = encoder.load(code_path, file_path)
    decoded_text = encoder.decode(loaded_text)
    assert original_text == decoded_text[:len(original_text)]
