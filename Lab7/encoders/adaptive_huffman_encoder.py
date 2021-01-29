import bitarray as ba

from encoders.basic_encoder import BasicEncoder


class AdaptiveHuffmanEncoder(BasicEncoder):

    def create(self, text: str) -> None:
        """
        docstring
        """
        pass

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

    code_path = osp.join('outputs', 'adaptive_huffman_code.json')
    file_path = osp.join('outputs', 'test_file.adaptive_huffman')
    original_text = 'ala ma kota'
    encoder = AdaptiveHuffmanEncoder()
    encoder.create(original_text)
    encoded_text = encoder.encode(original_text)
    encoder.save(code_path, file_path, encoded_text)
    encoder.code = None
    loaded_text = encoder.load(code_path, file_path)
    decoded_text = encoder.decode(loaded_text)
    assert original_text == decoded_text[:len(original_text)]
