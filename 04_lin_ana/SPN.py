# construction of SPN
"""
Permutation, S-Box and invers S-Box treated as constants
"""

SBOX = [0xE, 0x4, 0xD, 0x1,
        0x2, 0xF, 0xB, 0x8,
        0x3, 0xA, 0x6, 0xC,
        0x5, 0x9, 0x0, 0x7]

INVSBOX = [0]*16
for i in range(16):
    INVSBOX[SBOX[i]] = i

if __name__ == "__main__":
    print("INVSBOX =", INVSBOX)


PERM = [ 1, 5, 9, 13,
         2, 6, 10, 14,
         3, 7, 11, 15,
         4, 8, 12, 16 ]


def permute(int_num, PERM):
    """
    helper function to perform the permutation of bits

    :param int_num: integer, 16 bit
    :param PERM: Permutation to be used
    :return: integer, 16 bit, with permutation performed
    """
    result = 0
    for index, bit in enumerate(PERM):
        if int_num & (1 << (bit - 1)):  # is bit specified in perm set in integer?
            result |= 1 << index  # if yes, then change bit in result to 1 at respective index
    return result

def substitute(int_num, SBOX):
    """
    helper function to perform substitution of bits

    :param int_num: integer, 16 bit
    :param SBOX: S-Box to be used for substitution
    :return: integer, 16 bit, with substitution performed
    """
    result = 0
    for i in range(4):
        block = (int_num >> (i * 4)) & 0xF  # Extract the 4-bit block
        substituted_block = SBOX[block]  # subs
        result |= substituted_block << (i * 4)
    return result

if __name__ == "__main__":
    i = 0x1234
    print("substitutions:")
    print( format( substitute(i, SBOX), 'x'))
    print( format( substitute(i, INVSBOX), 'x'))
    i = 0x1
    print( format( substitute(i, SBOX), 'x'))
    print( format( substitute(i, INVSBOX), 'x'))


def SPN(block, key, sbox = SBOX, perm = PERM):
    """
    function for SPN encryption of one block, 16 Bit block length, 4 rounds with same key

    :param block: text to encrypt, 4 Hex numbers/16 bits as string
    :param key: 4 Hex numbers/ 16 bits as string
    :param sbox: table containing subs for each Hex Number
    :param perm: table containing global permutaion, elements are integers (count beginning at 1!)
    :return: encrypted block, 4 Hex numbers as string
    """
    # checks
    assert len(block) == 4
    assert len(key) == 4
    assert len(perm) == 16
    assert len(sbox) == 16

    # encryption
    w = int(block, 16)
    k = int(key, 16)
    for i in range(4): # 3 full rounds with perm, in 4th round another key add instead
        u = w ^ k # key addition
        #print(u)
        v = substitute(u, sbox)  # subs
        #print(v)
        if i < 3:
            w = permute(v, perm)  # perm
            #print(w)
        else:
            w = v ^ k  # last key add
            #print(w)
    return format( w, '04x')  # format as 4-chara hex str with leading zeros

# TEST:
if __name__ == "__main__":
    message = 'ABCD'
    print("message: ", message)
    key = '4523'
    cipher = SPN(message, key)
    print("cipher: ", cipher)

    message = '3B5D'
    print("message: ", message)
    key = '75A3'
    cipher = SPN(message, key)
    print("cipher: ", cipher)

    message = '8367'
    print("message: ", message)
    key = 'FE59'
    cipher = SPN(message, key)
    print("cipher: ", cipher)

#################################################################################################
# actual encription


def cut(hex_str, t):
    """
    helper function to cut hex str into blocks (similar to cut function for modi)

    :param hex_str: string of hex numbers to be cut
    :param t: block length (in hex character number)
    :return: list with bitstring in blocks of size t, last block padded with zeros if neccessary
    """
    block_lst = []
    # cut string into blocks of size t
    i = 0
    while i + t <= len(hex_str):
        block_lst.append(hex_str[i:i + t])
        i += t
    # padding with zeros for remainder
    if len(hex_str) % t != 0:  # remainder of bitstring smaller than block len t exists
        pad = '0' * (t - len(hex_str[i:]))
        block_lst.append(hex_str[i:] + pad)
    return block_lst

# TESTING
if __name__ == "__main__":
    str = '01100110011ABFE0110011001100110011001E'
    print(cut(str, 4))


def SPN_enc(message, key):
    """
    SPN Encryption for long message (like ECB)

    :param message: hex str
    :param key: hex str len 4 (=16 Bit)
    :return: hex string, ciphertext
    """
    t = 4   # SPN block length is always t = 4 (=16 bits)
    assert len(key) == t
    blk_lst = cut(message, t)
    cipher = ''
    for blk in blk_lst:
        cipher += SPN(blk, key)
    return cipher

if __name__ == "__main__":
    mes = "123456789ABCDEF"
    print("long message: ", mes)
    key = "1111"
    print( "long cipher: ", SPN_enc(mes, key) )

    mes = "ABCD"
    print("long message: ", mes)
    key = "1198"
    print( "long cipher: ", SPN_enc(mes, key) )

    mes = "ABCDEF565656563425EF77777777778DEAF1100006"
    print("long message: ", mes)
    key = "1198"
    print("long cipher: ", SPN_enc(mes, key))
    print("done")


