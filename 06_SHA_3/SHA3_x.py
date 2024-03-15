from SHA3 import SHA_3_224
from sys import argv

"""
SHA-3-224
"""
try:
    # INPUT using command line
    input_txt = str(argv[1])
    output_txt = str(argv[2])

    with open(input_txt, 'r') as input:
        N = input.read()

    with open(output_txt, 'w') as output:
        output.write(SHA_3_224(N))

except FileNotFoundError:
    print("Cannot find input args")
