import bitarray as ba
from collections import Counter

from encoders.basic_encoder import BasicEncoder


class HuffmanEncoder(BasicEncoder):

    def generate_code(self, state, history=''):
        """
        docstring
        """
        if len(state[0]) > 1:
            result = {}
            result.update(self.generate_code(state[0][0], history=f'{history}0'))
            result.update(self.generate_code(state[1][0], history=f'{history}1'))
            return result
        else:
            return {state[0]: history}

    def create(self, text: str) -> None:
        """
        docstring
        """
        # Huffman join
        frequency_list = Counter([c for c in text])
        while len(frequency_list) > 1:
            a = frequency_list.most_common()[-2:]
            del frequency_list[a[0][0]]
            del frequency_list[a[1][0]]
            frequency_list[tuple(a)] = a[0][1] + a[1][1]
        # Code generation
        state = list(frequency_list.keys())[0]
        code = self.generate_code(state)
        self.code = {k: ba.bitarray(v) for k, v in code.items()}

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
        buffer = 0
        for i in range(0, coded_text.length()):
            try:
                char_code = coded_text[i - buffer:i + 1].to01()
                result.append(reversed_dict[char_code])
                buffer = 0
            except KeyError:
                buffer += 1
                continue
        return ''.join(result)


# Local testing
if __name__ == '__main__':
    from os import path as osp

    code_path = osp.join('outputs', 'test_huffman_code.json')
    file_path = osp.join('outputs', 'test_file.huffman')
    original_text = 'ala ma kota'
    encoder = HuffmanEncoder()
    encoder.create(original_text)
    encoded_text = encoder.encode(original_text)
    encoder.save(code_path, file_path, encoded_text)
    encoder.code = None
    loaded_text = encoder.load(code_path, file_path)
    decoded_text = encoder.decode(loaded_text)
    assert original_text == decoded_text[:len(original_text)]
