import numpy as np
from PIL import Image
import argparse

BREAKING_STRING = '<endmsg>'

def read_image(path):
    im = Image.open(path)
    image_data = np.array(im)

    assert len(image_data.shape) == 3
    assert image_data.shape[-1] == 3

    h, w, _ = image_data.shape

    return w, h, image_data


def string_to_bits(string):
    return np.unpackbits(np.array(list(string.encode('utf-8')), dtype=np.ubyte))


def bits_to_string(bits):
    return bytearray(list(np.packbits(bits))).decode('utf-8')


def encode(string, input_path, output_path):
    w, h, image_data = read_image(input_path)
    bits_to_hide = np.concatenate([string_to_bits(string), np.ones(1, dtype=np.ubyte)])
    if bits_to_hide.shape[0] > w * h:
        raise ValueError('message is too large')

    bits_mask = np.pad(bits_to_hide, (0, w * h * 3 - bits_to_hide.shape[0]), 'constant').reshape(h, w, 3)
    image_data = image_data // 2 * 2 + bits_mask

    assert np.array_equal(image_data % 2, bits_mask)

    im = Image.fromarray(image_data)
    im.save(output_path)


def decode(image_path):
    w, h, image_data = read_image(image_path)
    data = image_data.reshape(-1) % 2
    data = np.trim_zeros(data, 'b')[:-1]
    return bits_to_string(data)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-i', '--input', action='store', dest='input', help='input file')
    parser.add_argument('-o', '--output', action='store', dest='output', help='output file')
    parser.add_argument('-m', '--message', action='store', dest='message', help='output file')
    parser.add_argument('-e', '--encode', action='store_true', dest='encode')
    parser.add_argument('-d', '--decode', action='store_true', dest='decode')

    args = parser.parse_args()
    if args.encode:
        encode(args.message, args.input, args.output)
    elif args.decode:
        print(decode(args.input))