from aes_block import aes_block_enc, aes_block_dec, key_trans, load_int_128, SBOX
from key_gen import key_gen

def cut(hex_string, t):
    """
    function to divide hex_string into blocks of size t and return a list containing these blocks
    last block is padded with zeros if neccessary
    blocks are represented as integers

    :param hex_string: string of hex numbers  (without whitespaces etc) to be divided into blocks
    :param t: integer, block length (number of bits)
    :return: list of integers, t bits, each representing a block
    """
    block_lst = []
    int_value = int( hex_string, 16)

    # padding -> determine value for left shift
    bit_len = len(hex_string) * 4
    shift_left = (t - (bit_len % t)) % t  # additional mod t because if bit_len is multiple of t no padding is necessary (not one full block)
    int_value <<= shift_left

    # cut into blocks of size t
    ones_t = 2**t - 1
    while int_value != 0:
        block_lst.append( int_value & ones_t )
        int_value >>= t
    block_lst.reverse()
    return block_lst

# TEST
if __name__ == "__main__":
    str_test = 'F0F0F0F0F0'
    print(cut(str_test, 4))
    print(cut('FF', 3))



def ECB(hex_string, fct, key, t = 128):
    """
    function realising the ECB mode
    For encryption and decryption, for encryption use fct = encrypt_fct,
    for decryption use fct = decrypt_fct
    the function used has to take an interger with bitlength t an a key as input
    fct = fct(int_128, key) (the key can have whatever format the function requires)

    :param hex_string: string of hex numbers (without whitespaces etc.)
    :param fct: name of function to be used for en/decryption
    :param key: key for en/decryption function
    :param t: optional, bitlength of blocks, 128 per default
    :return: ciphertext as hex string (no whitespaces etc)
    """
    block_lst = cut(hex_string, t)
    cipher = 0
    for blk in block_lst:
        cipher = ( cipher << t ) | fct(blk, key)
    len_ciphertext = len(block_lst) * t // 4  # include leading zeros
    ciphertext = format( cipher, f'0>{len_ciphertext}x')
    return ciphertext


if __name__ == "__main__":
    # get some keys
    key_0 = load_int_128('key_0.txt')
    keys = key_gen(key_0, SBOX)
    keys_dec = key_trans(keys)

    print("\nECB\n")
    # test using example 2
    str_test = 'e7e459faa111b337aa5218595c3bdc8d' * 3
    # expected result: 20b3c686335f1e4fbcfdc9d34aaefe5 * 3
    print(ECB(str_test, aes_block_enc, keys))
    str_test_2 = 'e7e459faa111b337aa5218595c3bdc8d' * 2 + 'e7e459faa111b337a'
    print(ECB(str_test_2, aes_block_enc, keys))
    # expected result: 20b3c686335f1e4fbcfdc9d34aaefe5 * 2 + 1 block different
    print("test dec")
    res = ECB(str_test, aes_block_enc, keys)
    print(res)
    print(str_test)
    print(ECB(res, aes_block_dec, keys_dec))
    # ?????????
    str_test_3 = 'e7e459faa111b337aa5218595c3bdc8d'
    res_3 = ECB(str_test_3, aes_block_enc, keys)
    str_enc_3 = '020b3c686335f1e4fbcfdc9d34aaefe5'
    res_dec_3 = ECB(str_enc_3, aes_block_dec, keys_dec)
    print("---------------------------")
    print("result enc: ", res_3)
    print("result dec: ", res_dec_3)
    print("---------------------------")
    def xor(i1, i2):
        return i1 ^ i2
    key_xor = 2**128 - 1
    str_test_4 = 'e7e459faa111b337aa5218595c3bdc8d'
    res_4 = ECB(str_test_4, xor, key_xor )
    res_dec_4 = ECB(res_4, xor, key_xor)
    print("---------------------------")
    print("result enc: ", res_4)
    print("result dec: ", res_dec_4)
    print("---------------------------")




def CBC(do_decryption, hex_string, fct, key, iv = 0, t = 128):
    """
    function realising the CBC modus
    for en/decryption, use respective function. Use same IV for enc as for dec

    :param do_decryption: flag/boolean, 0 -> encryption // 1 -> decryption
    :param hex_string: string of hex numbers (without whitespaces etc.)
    :param fct: name of function to be used for en/decryption
    :param key: key for en/decryption function
    :param iv: optional, integer, t bit / eg. 128 bit, initialisation vector, 0 per default
    :param t: optional, bitlength of blocks, 128 per default
    :return: ciphertext as hex string (no whitespaces etc)
    """
    block_lst = cut(hex_string, t)
    cipher = 0
    add = iv
    for blk in block_lst:
        if do_decryption:
            cipher_blk = fct(blk, key) ^ add
            add = blk
        else:
            cipher_blk = fct(blk ^ add, key)
            add = cipher_blk
        cipher = (cipher << t) | cipher_blk
    len_ciphertext = len(block_lst) * t // 4  # include leading zeros
    ciphertext = format(cipher, f'0>{len_ciphertext}x')
    return ciphertext

if __name__ == "__main__":
    print("\nCBC\n")
    # test using example 2
    str_test = 'e7e459faa111b337aa5218595c3bdc8d' * 3
    # keys as above
    # expected result: 20b3c686335f1e4fbcfdc9d34aaefe5 + 2 different blocks
    print(CBC(0, str_test, aes_block_enc, keys))
    str_test_2 = 'e7e459faa111b337aa5218595c3bdc8d' * 2 + 'e7e459faa111b337a'
    iv_test = 0xe7e459faa111b337aa5218595c3bdc8d
    res = CBC(0, str_test_2, aes_block_enc, keys, iv_test)
    print(res)
    print("dec test")
    print(CBC(1, res, aes_block_dec, keys_dec, iv_test))
    print(str_test_2)


def OFB(hex_string, fct, key, iv = 0, t = 128):
    """
    function realising the OFB mode (enc and dec)
    Use the same function fct and the same keys for enc and dec!!!

    :param hex_string: string of hex numbers (without whitespaces etc.)
    :param fct: name of function to be used for en/decryption
    :param key: key for en/decryption function
    :param iv: optional, integer, 128 bit, initialisation vector, 0 per default
    :param t: optional, bitlength of blocks, 128 per default
    :return: ciphertext as hex string (no whitespaces etc)
    """
    block_lst = cut(hex_string, t)
    cipher = 0
    add = iv
    for blk in block_lst:
        add = fct( add, key)
        cipher = (cipher << t) | (blk ^ add)
    len_ciphertext = len(block_lst) * t // 4  # include leading zeros
    ciphertext = format(cipher, f'0>{len_ciphertext}x')
    return ciphertext

if __name__ == "__main__":
    print("\nOFB\n")
    # test using example 2
    str_test = 'e7e459faa111b337aa5218595c3bdc8d' * 3
    # keys as above
    print(OFB(str_test, aes_block_enc, keys))
    str_test_2 = 'e7e459faa111b337aa5218595c3bdc8d' * 2 + 'e7e459faa111b337a'
    iv_test = 0xe7e459faa111b337aa5218595c3bdc8d
    res = OFB(str_test_2, aes_block_enc, keys, iv_test)
    print(res)
    print("dec test")
    print(OFB(res, aes_block_enc, keys, iv_test))
    print(str_test_2)


def CTR(hex_string, fct, key, nonce = 0, t = 128):
    """
    function realising the CTR mode (enc and dec)
    Use the same function fct and the same keys for enc and dec!!!
    the counter starts at 0

    :param hex_string: string of hex numbers (without whitespaces etc.)
    :param fct: name of function to be used for en/decryption
    :param key: key for en/decryption function
    :param nonce: optional, integer, 128 bit, 0 per default
    :param t: optional, bitlength of blocks, 128 per default
    :return: ciphertext as hex string (no whitespaces etc)
    """
    block_lst = cut(hex_string, t)
    cipher = 0
    ctr = nonce
    for blk in block_lst:
        cipher = (cipher << t) | (blk ^ fct(ctr, key))
        ctr += 1
    len_ciphertext = len(block_lst) * t // 4  # include leading zeros
    ciphertext = format(cipher, f'0>{len_ciphertext}x')
    return ciphertext

if __name__ == "__main__":
    print("\nCTR\n")
    # test using example 2
    str_test = 'e7e459faa111b337aa5218595c3bdc8d' * 3
    # keys as above
    print(CTR(str_test, aes_block_enc, keys))
    str_test_2 = 'e7e459faa111b337aa5218595c3bdc8d' * 2 + 'e7e459faa111b337a'
    nonce = 0xe7e459faa111b337aa5218595c3bdc8d
    res = CTR(str_test_2, aes_block_enc, keys, nonce)
    print(res)
    print("dec test")
    print(CTR(res, aes_block_enc, keys, nonce))
    print(str_test_2)



