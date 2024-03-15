from sys import argv
import random
from subkey import make_pairs
from SPN import SPN

try:
    # INPUT using command line
    clear_txt = str(argv[1])
    crypto_txt = str(argv[2])
    num_pairs = int(argv[3])

    # define key at random, keylength = 4
    key = ''.join(random.choice('0123456789abcdef') for j in range(4))
    print("Key: ", key)

    make_pairs(num_pairs, key, SPN, 4, clear_txt, crypto_txt)

except FileNotFoundError:
    print("Cannot find input args")