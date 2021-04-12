import rsa.euclidean_algorithm as euclidean_algorithm
import rsa.primes as primes
import rsa.common as common
import hashlib


def gen_keys(nbits=1024):
    while True:
        p, q = primes.gen_pq(nbits // 2)
        n = p * q
        phi_n = (p-1) * (q-1)
        e = 65537
        if euclidean_algorithm.gcd(phi_n, e) == 1:
            break

    d = euclidean_algorithm.reverse(e, phi_n)

    return {'public': (e, n), 'private': (d, n)}


def encode(data, key):
    power, n = key
    data = int.from_bytes(data, 'big')
    if data >= n:
        raise ValueError(f'data is too big, can only encode {n.bit_length()} bits')

    message = common.power_mod(data, power, n)
    return message.to_bytes(-(-message.bit_length() // 8), byteorder='big')


def decode(data, key):
    return encode(data, key)


def hash_string(string):
    hasher = hashlib.sha256()
    hasher.update(string.encode('utf-8'))
    return hasher.digest()


def sign(letter, key):
    if key[1].bit_length() <= 256:
        raise ValueError('key is too small, to encode sha256 you need at least nbits=257')

    return encode(hash_string(letter), key)


def validate_signature(letter, signature, key):
    if key[1].bit_length() <= 256:
        raise ValueError('key is too small, to encode sha256 you need at least nbits=257')

    return hash_string(letter) == decode(signature, key)
