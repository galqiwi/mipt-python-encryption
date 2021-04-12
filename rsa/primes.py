import rsa.common as common
import random


# Тест Миллера -- Рабина на простоту
def check_base(n, a, s, d):
    if common.power_mod(a, d, n) == 1:
        return True

    two_pow_r = 1
    for r in range(s):
        if common.power_mod(a, two_pow_r * d, n) == n - 1:
            return True
        two_pow_r *= 2

    return False


def is_prime_square(val):
    if val < 10:
        return val in {2, 3, 5, 7}

    div = 2
    while div * div <= val:
        if val % div == 0:
            return False
        div += 1

    return True


def is_prime(val):
    if val < 10:
        return val in {2, 3, 5, 7}

    if val % 2 == 0:
        return False

    small_primes = [_ for _ in range(3, 100) if is_prime_square(_)]

    if val in small_primes:
        return True

    for small_prime in small_primes:
        if val % small_prime == 0:
            return False

    d = val - 1
    s = 0
    while d % 2 == 0:
        s += 1
        d //= 2

    for check_id in range(25):
        a = random.randint(1, val - 1)
        if not check_base(val, a, s, d):
            return False

    return True


def gen_prime(nbits):
    assert nbits > 3

    while True:
        out = random.getrandbits(nbits)
        if out.bit_length() == nbits and is_prime(out):
            return out


# Генерирует два простых числа p и q таких, что их произведение имеет размер 2 * nbits
def gen_pq(nbits):
    total_bits = nbits * 2
    shift = nbits // 16  # чтобы сложнее было факторизовать p * q
    pbits = nbits - shift
    qbits = nbits + shift

    def check(check_q, check_p):
        if check_p == check_q:
            return False

        n = check_p * check_q
        return n.bit_length() == total_bits

    p = gen_prime(pbits)
    q = gen_prime(qbits)

    change_p = True
    while not check(p, q):
        if change_p:
            p = gen_prime(pbits)
        else:
            q = gen_prime(qbits)

        change_p = not change_p

    return p, q
