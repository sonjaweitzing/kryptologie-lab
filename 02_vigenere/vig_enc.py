from sys import argv
from vig import vig
"""
script to open .txt files specified in command line args and encrypt according to vig_encrypt
"""
try:
    # INPUT using command line
    input_txt = str(argv[1])
    key = str(argv[2])
    output_txt = str(argv[3])

    # Encryption
    vig(0, input_txt, key, output_txt)

except FileNotFoundError:
    print("Cannot find input args: [input.txt] [key] [output.txt]")