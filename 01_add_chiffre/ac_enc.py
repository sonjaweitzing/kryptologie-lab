from sys import argv
from ac import ac

"""
Script to encrypt a capital letter text
Run:
PROGNAME input.txt key output.txt
py -3 ../ac_enc.py ../Klartext_1.txt 7 ../ac_enc_output.txt
"""
try:
    # INPUT using command line
    input_txt = str(argv[1])
    key = int(argv[2])
    output_txt = str(argv[3])

    # Encryption (param do_decryption = 0)
    ac(0, input_txt, key, output_txt)

except FileNotFoundError:
    print("Cannot find input args: [input.txt] [key] [output.txt]")
