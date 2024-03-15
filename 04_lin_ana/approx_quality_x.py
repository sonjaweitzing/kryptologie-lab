from sys import argv
from approx_quality import approx_quality

try:
    # INPUT using command line
    sbox_txt = str(argv[1])
    approx_txt = str(argv[2])

    # sbox and approx for exercise on slides are given in sbox.txt and approx.txt
    # there is also a file approx_all_inactive.txt for test case of invalid approximation

    # I think theres a fault in the approx given on the slides, the "8" should be a "4". I changed that.

    quality = approx_quality(sbox_txt, approx_txt)
    print("Quality of the Approximation: ", quality)

except FileNotFoundError:
    print("Cannot find input args")