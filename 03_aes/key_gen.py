from aes_block import load_sbox, load_int_128, SBOX

def sub_word(w, sbox_enc):
    """
    function sub_word substitutes the bytes in the word using the sbox "S" provided:
    w = (b_0, b_1, b_2, b_3) -> (S[b_0], S[b_1], S[b_2], S[b_3])

    :param w: integer, 32 bit, word to be substituted
    :param sbox_enc: list of lists dim 16x16, s-box for encryption
    :return: integer, substituted word
    """
    sub_w = 0
    for i in range(4):  # i is index of byte b_0 to b_4, but never used explcitly
        row = w >> (8*(3-i)+4) & 0xF  # index of first 4 bits in current byte of string give row number.
        col = w >> (8*(3-i)) & 0xF  # last 4 bits in current byte give col number
        sub_w |= sbox_enc[row][col] << (8*(3-i))
    return sub_w

# TEST:
if __name__ == "__main__":
    w = 0x00010203
    sbox = load_sbox('SBox.txt')
    print("sub word: ", sub_word(w, sbox))
    print( "sub word: ", format( sub_word(w, sbox), 'x'))  # expected: 63 7c 77 7b
    w = 0x4b3f1536
    sbox = load_sbox('SBox.txt')
    print("sub word: ", sub_word(w, sbox))
    print("sub word: ", format(sub_word(w, sbox), 'x'))  # expected: b3 75 59 05


def rot_word(w):
    """
    function rot_word rotates the bytes of the word as follows: RotWord(b0, b1, b2, b3) = (b1, b2, b3, b0)

    :param w: integer, 32 bit, word to be rotated
    :return: integer, rotated word
    """
    # get b1, b2, b3 and shift, concatenate b0 = w >> (8*3) using bitwise or
    return ((w & 0xFFFFFF) << 8) | (w >> (8*3))

# TEST
if __name__ == "__main__":
    w = 0x01020304
    print("rot word: ", rot_word(w))
    print( "rot word: ", format( rot_word(w), 'x'))
    w = 0xAABBCCDD
    print("rot word: ", rot_word(w))
    print("rot word: ", format(rot_word(w), 'x'))


def rcon(i):
    """
    function rcon for key generation
    rc_i constant is determined trough table lookup

    :param i: integer from 1 to 10
    :return: integer, (rc_i 00_16 00_16 00_16)
    """
    rc = [0x01, 0x02, 0x04, 0x08, 0x10, 0x20, 0x40, 0x80, 0x1b, 0x36]
    return rc[i-1] << (8*3)

# TEST
if __name__ == "__main__":
    print('rcon: ', rcon(4))
    print('rcon hex: ', format(rcon(4), 'x'))# expected: 8 00 00 00
    print('rcon: ', rcon(7))
    print('rcon hex: ', format(rcon(7), 'x'))  # expected: 40 00 00 00


def key_gen(key_0, sbox_enc = SBOX):
    """
    function to generate 11 round keys for AES from initial key

    :param key_0: integer, 128 bit key/ 4 words
    :param sbox_enc: matrix (list of lists) dim 16x16, entries: 8 bit integers, sbox for encryption
    :return: list of 11 round keys as integers (128 bit)
    """
    w = [0 for count in range(44)]
    for i in range(4):
        w[i] = ( key_0 >> (32*(3-i)) ) & 0xFFFFFFFF
        # print(i, format(w[i], 'x'))
    for i in range(4,44):
        if i%4 == 0:
            w[i] = w[i-4] ^ rcon( i // 4 ) ^ sub_word( rot_word(w[i-1]), sbox_enc )
        else:
            w[i] = w[i-4] ^ w[i-1]
    keys = [0 for count in range(11)]
    for j in range(len(keys)):
        i = 4*j
        keys[j] = (w[i] << 3*32) | (w[i+1] << 2*32) | (w[i+2] << 32) | w[i+3]  # yes I know I could have put this in a loop too....
    return keys


# TEST
if __name__ == "__main__":
    # key_str = '2b 7e 15 16 28 ae d2 a6 ab f7 15 88 09 cf 4f 3c'
    key_0 = load_int_128('key_0.txt')
    sbox = load_sbox('SBox.txt')
    keys = key_gen(key_0, sbox)
    print(keys)
    for i in range(len(keys)):
        print(format(keys[i], '0>16x'))
    # the generated keys are the same keys as in example Beispiel_key.txt