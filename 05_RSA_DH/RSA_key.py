from find_prim import MAX_VERIFY, miller_rabin, find_prim, verified_miller_rabin
from eEA import eEA
from squa_and_mult import squa_and_mult
import random
# getting systemRandom instance out of random class
system_random = random.SystemRandom()
# This random class is suited for cryptographic purposes according to https://pynative.com/cryptographically-secure-random-data-in-python/
range_start = 10 ** 100
range_stop = 10 ** 101

def RSA_key_gen(range_start, range_stop):
    """
    function for RSA key generation
    (with p, q not to close)

    :param range_start: integer, lower boundary for prim numbers used
    :param range_stop: integer, upper boundary for prim numbers used
    :return: e, d, n, p, q (public key, privat key, modul, prim number 1, prim number 2)
    """
    # returns RAS keys in order e, d, n and also used prim numbers p, q
    # Generate two big prim numbers not to close
    min_distance = (range_stop - range_start) // 100  # mindestens ein Prozent der range difference
    p = 0
    q = 0
    while ( abs(p-q) <= min_distance):
        p = find_prim(range_start, range_stop)
        q = find_prim(range_start, range_stop)

    # generate random e coprime to phi(pq)
    phi = (p - 1) * (q - 1)
    e = 0
    ggT = 0
    while ggT != 1:
        e = system_random.randint(1, p * q)
        ggT, d = eEA(e, phi)[0:2]
        # Calc d with de = 1 mod phi(pq) using eEA - done automatically

    # for test - not strictly neccessary
    if d < 0:
        d += phi  # no negativ keys wanted, even thought technically ok -> mod phi, dh += phi
    return e, d, p*q, p, q


# Test
if __name__ == "__main__":
    r_start = 10 ** 6
    r_stop = 10 ** 7
    for i in range(30):
        e, d, n, p, q = RSA_key_gen(r_start, r_stop)
        print("e: ", e, "d: ", d, "n: ", n)

