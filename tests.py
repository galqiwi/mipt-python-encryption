import unittest
from rsa import common
from rsa import euclidean_algorithm
from rsa import primes
from rsa import rsa

from rsa.primes import check_base


class TestEuclideanAlgorithm(unittest.TestCase):
    def test_gcd(self):
        examples = [
            (1, 6, 1),
            (2, 6, 2),
            (3, 6, 3),
            (4, 6, 2),
            (5, 6, 1),
            (11 * 13, 11 * 239, 11),
            (11 * 2 * 13, 11 * 2 * 239, 11 * 2),
        ]
        for a, b, gcd_ab in examples:
            self.assertEqual(euclidean_algorithm.gcd(a, b), gcd_ab)
            self.assertEqual(euclidean_algorithm.gcd(b, a), gcd_ab)

    def test_lcm(self):
        examples = [
            (1, 6, 6),
            (2, 6, 6),
            (3, 6, 6),
            (4, 6, 12),
            (5, 6, 30),
            (11 * 13, 11 * 239, 11 * 13 * 239),
            (11 * 2 * 13, 11 * 2 * 239, 11 * 2 * 13 * 239),
        ]
        for a, b, gcd_ab in examples:
            self.assertEqual(euclidean_algorithm.lcm(a, b), gcd_ab)
            self.assertEqual(euclidean_algorithm.lcm(b, a), gcd_ab)

    def test_reverse(self):
        max_value = 200
        for mod in range(2, max_value + 1):
            for val in range(1, mod):
                if euclidean_algorithm.gcd(val, mod) != 1:
                    with self.assertRaises(ValueError):
                        euclidean_algorithm.reverse(val, mod)
                else:
                    reverse_val = euclidean_algorithm.reverse(val, mod)
                    self.assertEqual(val * reverse_val % mod, 1)


class TestCommon(unittest.TestCase):
    def test_power_mod(self):
        self.assertEqual(common.power_mod(2, 10, 2048), 1024)
        self.assertEqual(common.power_mod(2, 10, 1024), 0)
        self.assertEqual(common.power_mod(2, 10, 512), 0)
        self.assertEqual(common.power_mod(3, 3, 13), 1)
        self.assertEqual(common.power_mod(2, 6, 13), 12)

    def test_power_mod_fermats_little_theorem(self):
        primes_to_check = [3, 7, 13, 239, 2017]
        for prime in primes_to_check:
            for val in range(1, prime):
                self.assertEqual(common.power_mod(val, prime - 1, prime), 1)


class TestPrimeGeneration(unittest.TestCase):
    def test_is_prime(self):
        # https://en.wikipedia.org/wiki/Largest_known_prime_number
        self.assertTrue(primes.is_prime(2 ** 13 - 1))
        self.assertTrue(primes.is_prime(2 ** 17 - 1))
        self.assertTrue(primes.is_prime(2 ** 19 - 1))
        self.assertTrue(primes.is_prime(2 ** 31 - 1))
        self.assertTrue(primes.is_prime(2 ** 127 - 1))

        # 2 ** (2n) - 1 = (2 ** n - 1) * (2 ** n + 1)
        for power in range(4, 30, 2):
            self.assertFalse(primes.is_prime(2 ** power - 1))

        for value in range(1000):
            self.assertEqual(primes.is_prime(value), primes.is_prime_square(value))

    def test_prime_generation(self):
        nbits = 500
        prime = primes.gen_prime(nbits)
        self.assertTrue(primes.is_prime(prime))
        self.assertEqual(prime.bit_length(), nbits)

    def test_primes_generation(self):
        nbits = 500
        p, q = primes.gen_pq(nbits)
        self.assertTrue(primes.is_prime(p))
        self.assertTrue(primes.is_prime(q))
        n = p * q
        self.assertEqual(n.bit_length(), 2 * nbits)


class TestRSA(unittest.TestCase):
    def test_keygen(self):
        keys = rsa.gen_keys(1024)
        public = keys['public']
        private = keys['private']

        self.assertEqual(public[1].bit_length(), 1024)
        self.assertEqual(public[1], private[1])

    def test_signature(self):
        keys = rsa.gen_keys(1024)
        public = keys['public']
        private = keys['private']

        letter = 'This is a ' + 'very ' * 1000 + 'long and important public letter.'
        signature = rsa.sign(letter, private)
        self.assertTrue(rsa.validate_signature(letter, signature, public))

    def test_public_message(self):
        keys = rsa.gen_keys(1024)
        public = keys['public']
        private = keys['private']

        message = 'small public message from me'
        message_enc = rsa.encode(message.encode('utf-8'), private)

        self.assertEqual(rsa.decode(message_enc, public).decode('utf-8'), message)

    def test_private_message(self):
        keys = rsa.gen_keys(1024)
        public = keys['public']
        private = keys['private']

        message = 'small private message to you'
        message_enc = rsa.encode(message.encode('utf-8'), public)

        self.assertEqual(rsa.decode(message_enc, private).decode('utf-8'), message)

    def test_private_communication(self):
        alice_keys = rsa.gen_keys(1024)
        alice_public = alice_keys['public']
        alice_private = alice_keys['private']

        bob_keys = rsa.gen_keys(1024)
        bob_public = bob_keys['public']
        bob_private = bob_keys['private']

        message = 'Hi, Alice, I am bob.'
        message_enc = rsa.encode(rsa.encode(
            message.encode('utf-8'), bob_private), alice_public)

        message_decoded = rsa.decode(rsa.encode(
            message_enc, alice_private), bob_public).decode('utf-8')

        self.assertEqual(message_decoded, message)


if __name__ == '__main__':
    unittest.main()
