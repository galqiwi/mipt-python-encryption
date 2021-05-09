import base64


# Быстрое возведение в степень
def power_mod(value, power, mod):
    value %= mod

    power_bin = []

    while power > 0:
        power_bin.append(power % 2)
        power //= 2
    power_bin.reverse()

    out = 1
    for bit in power_bin:
        out = (out * out) % mod
        if bit == 1:
            out = (out * value) % mod

    return out


def int_to_bytes(value):
    return value.to_bytes(-(-value.bit_length() // 8), byteorder='big')


def int_to_base64(value):
    return base64.b64encode(int_to_bytes(value)).decode()


def bytes_to_int(data):
    return int.from_bytes(data, 'big')


def base64_to_int(string):
    return bytes_to_int(base64.b64decode(string))


def key_to_base64(key):
    return '-'.join([int_to_base64(_) for _ in key])


def base64_to_key(string):
    return (base64_to_int(_) for _ in string.split('-'))
