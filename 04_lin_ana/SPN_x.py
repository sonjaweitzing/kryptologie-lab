from sys import argv
from SPN import SPN_enc

try:
    # INPUT using command line
    input_txt = str(argv[1])
    key_txt = str(argv[2])
    output_txt = str(argv[3])

    with open(input_txt, 'r') as input:
        message = input.read()

    with open(key_txt, 'r') as input:
        key = input.read()

    with open(output_txt, 'w') as output:
        output.write( SPN_enc(message, key) )

except FileNotFoundError:
    print("Cannot find input args")