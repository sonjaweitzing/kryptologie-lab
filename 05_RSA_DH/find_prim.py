import random
from squa_and_mult import squa_and_mult

# getting systemRandom instance out of random class
system_random = random.SystemRandom()
# This random class is suited for cryptographic purposes according to https://pynative.com/cryptographically-secure-random-data-in-python/

# Auch mgl: Secure random number
# print(system_random.randint(1, 30))


# Miller Rabin Prim Number Test
def miller_rabin(n):
    """
    miller rabin prim number test, randomised
    there may be false positives, see lecture for details

    :param n: integer, potential prim number
    :return: integer (boolean) 1 -> prim, 0 -> composite
    """
    # Test ob n Primzahl ist
    # wenn n gerade, dann keine Primzahl
    if n % 2 == 0:
        return 0

    # Bestimme ungerades m mit n − 1 = 2^k · m
    m = n - 1  # m ist ungerade
    k = 0
    while m % 2 == 0:
        m //= 2
        k += 1

    a = system_random.randrange(2, n)
    b = squa_and_mult(a, m, n)  # (a**m) % n
    if (b%n == 1):
        return 1  # prim
    for i in range(1, k+1):
        if b % n == n - 1:  # b%n == -1
            return 1  # prim
        else:
            b = (b*b) % n
    return 0  # composite

# TEST
if __name__ == "__main__":
    prim_0 = 89
    print(prim_0, " prim?  ", miller_rabin(prim_0))
    prim_1 = 73
    print(prim_1, " prim?  ",miller_rabin(prim_1))
    prim_2 = 220807  # ist eine Primzahl
    print(prim_2, " prim?  ",miller_rabin(prim_2))
    not_prim = 220808  # ist keine primzahl
    print(not_prim, " prim?  ",miller_rabin(not_prim))

    # works :D





# number of Miller Rabin Tests for Verification
# Probability of "false positiv" is less equal 1/4
# Error Probability of e^(-20) usually acknoladged as "secure" - requires ~ 29 Test
MAX_VERIFY = 29

def verified_miller_rabin(n, max_verify):
    """
    verification of potential prim number
    returns 1/True only if possible prim n has passed miller-rabin test max_verify times

    :param n: integer, potential prim number
    :param max_verify: integer, number of tests performed for verification
    :return: integer (boolean) 1 -> verified prim, 0 -> composite
    """
    l = 0
    while (l <= max_verify):
        if miller_rabin(n):
            l += 1
        else:
            return 0
    return 1

# TEST
if __name__ == "__main__":
    print("verified: ", prim_2)
    print(prim_0, "verified: ", verified_miller_rabin(prim_0, MAX_VERIFY))
    print(prim_1, "verified: ", verified_miller_rabin(prim_1, MAX_VERIFY))
    print(prim_2, "verified: ", verified_miller_rabin(prim_2, MAX_VERIFY))


def find_prim(range_start, range_stop):
    """
    function to find a big prim number in a given range
    the prim number is usually in range [range_start, range_stop]   ,
    but because of randomisation, it might be larger than range_stop (but still in the same order)

    :param range_start: integer, lower boundary
    :param range_stop:  integer, upper boundary
    :return: prim number roughly in range
    """
    # Secure random number within a range
    # z. B. z = system_random.randrange(10**99//3, 10**100//3); Form x = 30z, x in Größenordnung 10^100
    z = system_random.randrange(range_start // 30, range_stop // 30)

    # Test Add
    i = [1, 7, 11, 13, 17, 19, 23, 29]

    # Teste 30z+i
    fac = 0  # accords for i > 29
    while fac < 100:
        for j in range(len(i)):
            if miller_rabin(30*z + 30*fac + i[j]):
                # print('candidate:', 30*z + 30*fac + i[j])
                if verified_miller_rabin(30*z + 30*fac + i[j], MAX_VERIFY):
                    # print('tried verification')
                    # print(fac, i[j])
                    return 30*z + 30*fac + i[j]
        fac += 1
    return 'took too long'

# TEST
if __name__ == "__main__":
    range_start = 10 ** 100
    range_stop = 10 ** 101
    p = find_prim(range_start, range_stop)
    print(p)






