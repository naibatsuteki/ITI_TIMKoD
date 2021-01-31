import bitarray as ba
from math import log2, ceil, pow
from encoders.basic_encoder import BasicEncoder


class LZWEncoder(BasicEncoder):

    def __init__(self, max_dict_size: int):
        super(LZWEncoder, self).__init__()
        self.max_dict_size = max_dict_size
        self.code_length = int(ceil(log2(max_dict_size)))

    def _init_dict(self):
        """
        docstring
        """
        lzw_dict = {}
        for i in range(256):
            lzw_dict[bin(i)[2:].zfill(8)] = i

        return lzw_dict

    def create(self, text: str) -> None:
        """
        docstring
        """
        # In this task this method should not be implemented.
        pass

    def encode(self, text: str) -> ba.bitarray:
        """
        docstring
        """
        lzw_dict = self._init_dict()
        max_dict_val = max(lzw_dict.values())

        inner_result = []
        buffer = ''
        for i, c in enumerate(text):
            next_part = f"{ord(c):0{8}b}"
            new_buffer = f'{buffer}{next_part}'
            if new_buffer in lzw_dict.keys():
                if len(lzw_dict) < self.max_dict_size or self.max_dict_size == -1:
                    buffer = new_buffer
                    continue
                else:
                    inner_result.append(lzw_dict[new_buffer])
                    buffer = ''

            else:
                inner_result.append(lzw_dict[buffer])
                max_dict_val += 1
                lzw_dict[new_buffer] = max_dict_val
                buffer = next_part
        else:
            if len(lzw_dict) < self.max_dict_size or self.max_dict_size == -1:
                inner_result.append(lzw_dict[buffer])
        result = ba.bitarray()

        # Save code for visualization purpose
        self.code = {k: ba.bitarray(f"{v:0{self.code_length}b}") for k, v in lzw_dict.items()}

        for i in inner_result:
            result.extend(ba.bitarray(f"{i:0{self.code_length}b}"))
        return result

    def decode(self, coded_text: ba.bitarray) -> str:
        """
        docstring
        """
        decoding_lzw_dict = {v: k for k, v in self._init_dict().items()}

        max_dict_key = max(decoding_lzw_dict.keys())
        # cut the redundant bits if they occurred while saving.
        length = (len(coded_text) // self.code_length) * self.code_length

        inner_result = ''
        last_key = None
        for i in range(0, length, self.code_length):
            next_key = int(coded_text[i:i + self.code_length].to01(), 2)
            if last_key is not None:
                mew = decoding_lzw_dict[last_key] + (decoding_lzw_dict[next_key][0:8])  # ASCII Specific
                decoding_lzw_dict[last_key] = mew
            inner_result += decoding_lzw_dict[next_key]
            if len(decoding_lzw_dict) < self.max_dict_size or self.max_dict_size == -1:
                max_dict_key += 1
                decoding_lzw_dict[max_dict_key] = decoding_lzw_dict[next_key]
                last_key = max_dict_key
            else:
                last_key = None

        return ''.join([chr(int(inner_result[i: i + 8], 2)) for i in range(0, len(inner_result), 8)])


# Local testing
if __name__ == '__main__':
    from os import path as osp

    code_path = osp.join('outputs', 'lzw_code.json')
    file_path = osp.join('outputs', 'test_file.lzw')
    original_text = 'aaaaaaaaaab'
    encoder = LZWEncoder(int(pow(2, 8)))
    # encoder.create(original_text)
    encoded_text = encoder.encode(original_text)
    encoder.save(code_path, file_path, encoded_text)
    encoder.code = None
    loaded_text = encoder.load(code_path, file_path)
    decoded_text = encoder.decode(loaded_text)
    assert original_text == decoded_text[:len(original_text)]
