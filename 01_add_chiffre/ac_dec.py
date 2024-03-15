from sys import argv
from ac import ac

"""
Script to decrypt a capital letter text with a known key
Run:
PROGNAME input.txt key output.txt
py -3 ../ac_enc.py ../Kryptotext_1_Key_7.txt 7 ../ac_dec_output.txt
"""
try:
    # INPUT using command line
    input_txt = str(argv[1])
    key = int(argv[2])
    output_txt = str(argv[3])

    # Decryption (param do_decryption = 1)
    ac(1, input_txt, key, output_txt)

except FileNotFoundError:
    print("Cannot find input args: [input.txt] [key] [output.txt]")
