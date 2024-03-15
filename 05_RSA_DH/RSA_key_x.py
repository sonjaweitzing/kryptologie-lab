from RSA_key import RSA_key_gen
from sys import argv

"""
RSA key generation
"""

try:
    # INPUT using command line
    length = int(argv[1])  # key length required (roughly)
    out_privat = str(argv[2])  # txt with d, n
    out_public = str(argv[3])  # txt with e, n
    prims = str(argv[4])  # txt with p, q


    # py -3 RSA_x.py ExampleText.txt ExampleKey.txt OutputRSAEnc3.txt
    # py -3 RSA_x.py ExampleEncrypted.txt ExampleKeyDecrypt.txt OutputRSADec1.txt

    # # INPUT without command line
    # input_txt = 'C:/Users/sonja/python/KrypLABgit/RSA/RSA_dateien/ExampleText.txt'
    # key_txt = 'C:/Users/sonja/python/KrypLABgit/RSA/RSA_dateien/ExampleKey.txt'
    # output_txt = 'C:/Users/sonja/python/KrypLABgit/RSA/RSA_dateien/OutputRSAEnc.

    range_start = 2 ** length
    range_stop = 2 ** (length + 1)
    e, d, n, p, q = RSA_key_gen(range_start, range_stop)

    with open(out_privat, 'w') as f:
        f.write(str(d) + '\n')
        f.write(str(n) + '\n')
    with open(out_public, 'w') as f:
        f.write(str(e) + '\n')
        f.write(str(n) + '\n')
    with open(prims, 'w') as f:
        f.write(str(p) + '\n')
        f.write(str(q) + '\n')

except FileNotFoundError:
    print("Cannot find input args")

# works ^^