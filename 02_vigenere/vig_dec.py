from sys import argv
from find_key import find_key, find_key_length
from vig import vig
"""
script to open .txt files specified in command line args and decrypt the given vigenere encrypted cipher text.
The key is determined using frequency analysis and the coincidence index.
"""
try:
    # INPUT using command line
    input_txt = str(argv[1])
    output_txt = str(argv[2])

    # input_txt = 'Kryptotext_TAG.txt'
    # output_txt = 'vig_out_test.txt'

    # Decryption
    key_len = find_key_length(input_txt)
    key = find_key(key_len, input_txt)
    vig(1, input_txt, key, output_txt)

except FileNotFoundError:
    print("Cannot find input args: [input.txt] [output.txt]")
