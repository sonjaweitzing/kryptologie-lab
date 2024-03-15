from aes_block import key_trans, aes_block_enc, aes_block_dec, load_int_128
from key_gen import key_gen
from modi import ECB, CBC, OFB, CTR

# Helper function for output formatation

def format_hex_string(hex_string):
    """
    function to format a string of hex numbers into an easy to read format
    lines: 32 hex numbers / 128 bit / 1 block
    hex numbers in groups of two, separated by whitespace

    :param hex_string: unformatted hex string
    :return: formatted hex string
    """
    # Remove any whitespaces or line breaks from the input hex string
    hex_string = hex_string.replace(" ", "").replace("\n", "")
    formatted_result = ""
    for i in range(len(hex_string)):
        if i % 32 == 0 and i != 0:
            formatted_result += "\n" + hex_string[i:i + 2] + " "
        elif i % 2 == 0:
            formatted_result += hex_string[i:i + 2] + " "

    return formatted_result

# TEST
if __name__ == "__main__":
    input_hex_string = "1a2b3c4d5e6f7a8b9c0d1e2f3a4b5c6d7e8f9a0b1c2d3e4f5a6b7c8d9e0f"
    formatted_output = format_hex_string(input_hex_string)
    print(formatted_output)

###########################################################################################
# aes encryption and decryption including key generation


def aes(do_decryption, modus, in_txt, key_txt, out_txt, iv_txt ='none'):
    """
    aes encryption or decryption in 4 modi.
    initialisationvector has to be passed as arg for CBC, OFB modus
    nonce = 0 for CTR modus

    :param do_decryption: flag, 0 -> encryption, 1 -> decryption
    :param modus: 'ECB', 'CBC', 'OFB', 'CTR' are possible modi, choose one
    :param in_txt: path to txt file with input text as hex numbers
    :param key_txt: path to txt file with key as hex numbers, 128 bit
    :param out_txt: path to txt file with output text as hex numbers. if file does not exist, it is created
    :param iv: path to txt file with key as hex numbers, 128 bit, initialisation vector, necessary for CBC, OFB only
    :OUTPUT: creates txt file with output text after aes enc/dec is performed
    """

    # keys
    key_0 = load_int_128(key_txt)
    keys = key_gen(key_0)
    keys_dec = key_trans(keys)

    # IV for CBC, OFB required
    iv = 0
    if modus in {'CBC', 'OFB'}:
        iv = load_int_128(iv_txt)

    # load text
    with open(in_txt, 'r') as f:
        hex_string = f.read()

        # Remove any spaces and line breaks from the input string
        hex_string = hex_string.replace(" ", "")
        hex_string = hex_string.replace("\n", "")

    # modus and IV if necessary
    ciphertext = ''
    if modus == 'ECB':
        if do_decryption:
            ciphertext = ECB(hex_string, aes_block_dec, keys_dec)
        else:
            ciphertext = ECB(hex_string, aes_block_enc, keys)
    elif modus == 'CBC':
        if do_decryption:
            ciphertext = CBC(do_decryption, hex_string, aes_block_dec, keys_dec, iv)
        else:
            ciphertext = CBC(do_decryption, hex_string, aes_block_enc, keys, iv)
    elif modus == 'OFB':
        ciphertext = OFB(hex_string, aes_block_enc, keys, iv)
    elif modus == 'CTR':
        ciphertext = CTR(hex_string, aes_block_enc, keys)
        # nonce = 0 here
    else:
        raise 'No valid operation modus. Modus must be ECB, CBC, OFB or CTR'

    # format string and write into output txt
    formatted_string = format_hex_string(ciphertext)
    with open(out_txt, 'w') as f:
        f.write(formatted_string)

    return 0

# TEST
if __name__ == "__main__":
    in_txt = 'Beispiel_1_lang_klar.txt'
    key_txt = 'key_0.txt'
    iv_txt = 'iv.txt'  # iv_0.txt for IV = 0
    for modus in ['ECB', 'CBC', 'OFB', 'CTR']:
        out_txt = f'aes_enc_out_{modus}.txt'
        out_txt_dec = f'aes_dec_out_{modus}.txt'
        aes(0, modus, in_txt, key_txt, out_txt, iv_txt)
        aes(1, modus, out_txt, key_txt, out_txt_dec, iv_txt)
