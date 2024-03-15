from DH import DH_key_exchange
from sys import argv

"""
Diffie Hellman key exchange
Output as standart output
"""

try:
    # INPUT using command line
    bitlength = int(argv[1])  # bitlength of prim number required (roughly)

    p, g, A, B, S = DH_key_exchange(bitlength)
    # Return as Standartoutput:
    print("Primnumber: ", p)
    print("Generator: ", g)
    print("Alice Calculation A: ", A)
    print("Bob Calculation B: ", B)
    print("Secret S: ", S)

except FileNotFoundError:
    print("Cannot find input args")

# works ^^