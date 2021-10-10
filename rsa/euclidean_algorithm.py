def gcd(a, b):
    if a > b:
        a, b = b, a

    while a > 0:
        b %= a
        a, b = b, a

    return a + b


def lcm(a, b):
    return (a // gcd(a, b)) * b


def reverse(value, mod):
    if gcd(value, mod) != 1:
        raise ValueError('value and mod are not coprimes')

    # находим решение типа
    # value * x + mod * y == 1,
    # храним значение тройками (x, y, value * x + mod * y)

    a = (1, 0, value)
    b = (0, 1, mod)

    if a[-1] > b[-1]:
        a, b = b, a

    # далее значение a всегда меньше значения b
    while a[-1] > 0:
        k = b[-1] // a[-1]
        b = tuple(b_v - k * a_v for b_v, a_v in zip(b, a))
        a, b = b, a

    return b[0] % mod