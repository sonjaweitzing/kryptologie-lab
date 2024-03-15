from aes import aes
from sys import argv

"""
script to open .txt files specified in command line args and encrypt plain text using aes
"""
try:
    # INPUT using command line
    modus = str(argv[1])
    input_txt = str(argv[2])
    key_txt = str(argv[3])
    output_txt = str(argv[4])
    # iv only needed as arg for CBC and OFB
    iv_txt = 'none'
    if modus in {'CBC', 'OFB'}:
        iv_txt = str(argv[5])


    # Encryption
    aes(0, modus, input_txt, key_txt, output_txt, iv_txt)

except FileNotFoundError:
    print("Incorrect Input args: modus must be ECB, CBC, OFB, CTR, iv necessary for CBC, OFB; [input.txt] [key_txt] [output.txt]")