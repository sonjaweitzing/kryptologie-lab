from sys import argv
from subkey import subkey

try:
    # INPUT using command line
    clear_txt = str(argv[1])
    crypto_txt = str(argv[2])

    maxkey = subkey( clear_txt, crypto_txt)
    print("Most likely subkey: ", maxkey)

except FileNotFoundError:
    print("Cannot find input args")