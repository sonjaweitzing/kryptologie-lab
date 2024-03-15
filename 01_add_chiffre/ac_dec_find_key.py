from sys import argv
from ac import ac
from find_key import find_key

"""
Script to decrypt a capital letter text with an unknown key

Run:
PROGNAME input.txt output.txt
py -3 ../ac_enc.py ../Kryptotext_1_Key_7.txt ../ac_dec_key_output.txt

If line 21 is uncommented and line 22 commented, then the
file "ac_dec_key_output.txt" is created containing the output/decrypted text, because, according to the exercise,
there is to be no command line arg for an output file.

the output file contains the key in the first line in addition to the decrypted text
"""
try:
    # INPUT using command line
    input_txt = str(argv[1])
    # output_txt = 'ac_dec_key_output.txt'
    output_txt = str(argv[2])

    # find key and use for decryption
    key = find_key(input_txt)
    ac(1, input_txt, key, output_txt)

    # write key in first line of file and decrypted text in remainder of file
    with open(output_txt, 'r') as file:
        text = file.readlines()

    with open(output_txt, 'w') as file:
        file.write(str(key) + '\n')
        file.writelines(text)

except FileNotFoundError:
    print("Cannot find input args: [input.txt] [output.txt]")

