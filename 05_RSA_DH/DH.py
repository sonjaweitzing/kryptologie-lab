from find_prim import MAX_VERIFY, miller_rabin, find_prim, verified_miller_rabin
from squa_and_mult import squa_and_mult
import random

system_random = random.SystemRandom()
# This random class is suited for cryptographic purposes according to https://pynative.com/cryptographically-secure-random-data-in-python/
range_start = 10 ** 100
range_stop = 10 ** 101

def DH_parameters(bitlength):
    """
    function to calculate parameters for DH key exchange, namely generator g and large prim p

    :param bitlength: integer, desired bitlength of prim p
    :return: g, p (generator, large prim)
    """
    # p is large prim, p = 2q + 1, q is large prim, g random in [2, p-2]
    p = 0
    q = 0
    is_prim = 0
    while not is_prim:
        q = find_prim(2 ** (bitlength - 1), 2 ** (bitlength + 1))  # Bitlänge der Primzahl ca. bitlength ...  bitlength + 2
        p = 2 * q + 1
        is_prim = verified_miller_rabin(p, MAX_VERIFY)
    g = system_random.randrange(2, p-1)
    return g, p
    # ist g hier wirklich Erzeuger? Ist das Wichtig?
    # Ergebnisse sehen gut aus (geprüft mit Test-Vergleich)
    # Alternativ könnte die Funktion "DH_para_not_eff(bitlength)" gewählt werden.
    # Diese prüft alle Primfaktoren systematisch (Alg VL) -> g ist sicher Erzeuger, aber Faktorisierung dauert zu lang

def DH_key_exchange(bitlength):
    """
    function simulates a DH key exchange

    :param bitlength: desired bitlength for large prim
    :return: p, g, A, B, S (prim, generator, Alice' calculation, Bob's calculation, shared secret)
    """
    # Simulates DH key exchange
    # parameters
    g, p = DH_parameters(bitlength)
    # alice - chooses big enough a (here in range p/2 to p) and calc A
    a = system_random.randrange(p // 2, p)
    A = squa_and_mult(g, a, p)
    # bob - analog to alice
    b = system_random.randrange(p // 2, p)
    B = squa_and_mult(g, b, p)
    # alice and bob swap numbers A, B -> They each calculate secret key S
    # Here done only once for bobs calc, alice would calc     S = squa_and_mult(B, a, p)
    S = squa_and_mult(A, b, p)
    # Comparision here just for test purposes, not necessary
    if (S != squa_and_mult(B, a, p)):
        print("------ S ERROR ------")
    # else:
    #     print("------- S Fine")
    return p, g, A, B, S

    # # Return as Standartoutput:
    # print("Primnumber: ", p)
    # print("Generator: ", g)
    # print("ALice Calculation A: ", A)
    # print("Bob Calculation B: ", B)
    # print("Calculated secret S: ", S)

def bit_length(n):
    """
    helper function, returns bitlength

    :param n: integer
    :return: bitlength
    """
    return n.bit_length()


if __name__ == "__main__":
    l1 = 10
    l2 = 200
    p, g, A, B, S = DH_key_exchange(l1)
    # Return as Standartoutput:
    print("Primnumber: ", p, "bitlength:", bit_length(p))
    print("Generator: ", g)
    print("ALice Calculation A: ", A)
    print("Bob Calculation B: ", B)
    print("Calculated secret S: ", S)

    p, g, A, B, S = DH_key_exchange(l2)
    # Return as Standartoutput:
    print("Primnumber: ", p, "bitlength:", bit_length(p))
    print("Generator: ", g)
    print("ALice Calculation A: ", A)
    print("Bob Calculation B: ", B)
    print("Calculated secret S: ", S)


    # Check bit length


