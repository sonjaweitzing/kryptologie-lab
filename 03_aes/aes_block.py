# Helper functions

def load_sbox(sbox_txt):
    """
    Helperfunction to load sbox (encryption or invers for decryption)

    :param sbox_txt: .txt file containing sbox, 16 lines with 16 entries each, entry 1 byte as hex number, separated by whitespace
    :return: sbox as list of lists, 16x16, entries are integers
    """
    sbox = []
    with open(sbox_txt, 'r') as f:
        lines = f.readlines()
        for line in lines:
            sbox_line = []
            numbers = line.split()  # splits at each whitespace, so that hex-numbers are written into matrtix
            for number in numbers:
                sbox_line.append(int(number, 16))
            sbox.append(sbox_line)
    return sbox


# Sboxes as constants, because of compatibility with modi but not loading sbox anew for every block
SBOX = load_sbox('SBox.txt')
SBOX_INV = load_sbox('SBoxInvers.txt')

def load_int_128(int_txt):
    """
    Helperfunction, loads key from .txt file and returns it as integer

    :param int_txt: .txt file containing key/ 128 bit in hex numbers
    :return: key/hex numbers as 128 bit integer
    """
    with open(int_txt, 'r') as f:
        hex_string = f.read()

        # Remove any spaces from the input string
        hex_string = hex_string.replace(" ", "")
        hex_string = hex_string.replace("\n", "")


        # Convert the cleaned hex string to an integer
        return int(hex_string, 16)


if __name__ == "__main__":
    key_str = '2b 7e 15 16 28 ae d2 a6 ab f7 15 88 09 cf 4f 3c'
    sbox = load_sbox('SBox.txt')
    print(sbox)
    result = load_int_128('key_0.txt')
    print(result)
    print( format(result, 'x'))
    #  print( format( 0x63 ))

#########################################################################################################
# functions for aes block encryption

def int_to_mat(int_blk):
    """
    function to convert a 128-bit integer into a 4x4 matrix with each entry being an 8-bit integer COLUMNWISE

    :param int_blk: integer, 128 bit, (block to be encrypted)
    :return: 4x4 list of lists (matrix) containing block
    """
    M = [[0 for _ in range(4)] for _ in range(4)]
    for j in range(4):  # fill matrix col by col
        for i in range(4):
            M[i][j] = ( int_blk >> ((4*(3-j) + (3-i)) * 8) ) & 0xFF  # current byte
    return M


def mat_to_int(matrix):
    """
    Converts a 4x4 matrix (each entry being an 8-bit integer COLUMNWISE) back into a 128-bit integer.

    :param matrix: 4x4 list of lists (matrix) containing block
    :return: integer, 128-bit (block)
    """
    int_blk = 0
    for j in range(4):
        for i in range(4):
            int_blk |= (matrix[i][j] << ((4 * (3 - j) + (3 - i)) * 8))
    return int_blk

# TEST
if __name__ == "__main__":
    def test_int_to_mat():
        int_value = 0x123456789ABCDEF0123456789ABCDEF0
        expected_matrix = [
            [0x12, 0x9A, 0x12, 0x9A],
            [0x34, 0xBC, 0x34, 0xBC],
            [0x56, 0xDE, 0x56, 0xDE],
            [0x78, 0xF0, 0x78, 0xF0]
        ]
        assert int_to_mat(int_value) == expected_matrix, "Test case failed!"

    test_int_to_mat()

    def test_mat_to_int():
        input_matrix = [
            [0x12, 0x9A, 0x12, 0x9A],
            [0x34, 0xBC, 0x34, 0xBC],
            [0x56, 0xDE, 0x56, 0xDE],
            [0x78, 0xF0, 0x78, 0xF0]
        ]
        expected_int_value = 0x123456789ABCDEF0123456789ABCDEF0
        assert mat_to_int(input_matrix) == expected_int_value, "Test case failed!"

    test_mat_to_int()



def add_round_key(A, K):
    """
    In-place addition of key with xor
    (no need for only quadratic matrices here, just same dimensions requiered)

    :param A: Matrix containing text
    :param K: Matrix containing key
    :return: Matrix with each entry XOR of text and key
    """
    for i in range(len(A)):
        for j in range(len(A[i])):
            A[i][j] = A[i][j] ^ K[i][j]
    return A

# TEST
if __name__ == "__main__":
    def test_add_round_key():
        A = [
            [0x00, 0x00, 0x00, 0x00],
            [0xFF, 0xFF, 0xFF, 0xFF],
            [0x00, 0x00, 0x00, 0x00],
            [0xFF, 0xFF, 0xFF, 0xFF]
        ]
        K = [
            [0xFF, 0xFF, 0xFF, 0xFF],
            [0x00, 0x00, 0x00, 0x00],
            [0xFF, 0xFF, 0xFF, 0xFF],
            [0x00, 0x00, 0x00, 0x00]
        ]

        # Expected result after XOR operation
        expected_result = [
            [0xFF, 0xFF, 0xFF, 0xFF],
            [0xFF, 0xFF, 0xFF, 0xFF],
            [0xFF, 0xFF, 0xFF, 0xFF],
            [0xFF, 0xFF, 0xFF, 0xFF]
        ]

        # Apply the function
        result = add_round_key(A, K)

        # Check if the result matches the expected outcome
        assert result == expected_result, "Test case failed!"


    test_add_round_key()


def sub_bytes(A, sbox):
    """
    function sub_bytes substitutes the bytes in the matrix according to the sbox
    to obtain sub_bytes_inv simply use invers sbox

    :param A: Matrix containing text
    :param sbox: 16x16 list of lists, sbox (for encryption or decryption)
    :return: Matrix with substituted bytes
    """
    S = [[0 for _ in range(4)] for _ in range(4)] # initialise substituted Matrix
    for i in range(4):
        for j in range(4):
            row = A[i][j] >> 4  # first 4 bits
            col = A[i][j] & 0xF  # last 4 bits
            S[i][j] = sbox[row][col] # find the right substitution in sbox- matrix
    return S

# TEST
if __name__ == "__main__":
    sbox = load_sbox('SBox.txt')
    A = [
        [0x00, 0x00, 0x00, 0x00],
        [0xFF, 0xFF, 0xFF, 0xFF],
        [0x00, 0x00, 0x00, 0x00],
        [0xFF, 0xFF, 0xFF, 0xFF]
    ]

    # ecpected
    S = [
        [0x63, 0x63, 0x63, 0x63],
        [0x16, 0x16, 0x16, 0x16],
        [0x63, 0x63, 0x63, 0x63],
        [0x16, 0x16, 0x16, 0x16]
    ]

    result = sub_bytes(A, sbox)

    assert result == S, "Test case failed!"


def shift_rows(A):
    """
    function shift rows enc is a cyclic permutation of all rows to the LEFT

    :param A: Matrix containing text
    :return: permuted Matrix
    """
    S = [[0 for _ in range(4)] for _ in range(4)] # initialise shifted Matrix
    for i in range(4):
        for j in range(4):
            S[i][j] = A[i][(j + i) % 4]
    return S


def shift_rows_inv(A):
    """
    function shift rows enc is a cyclic permutation of all rows to the RIGHT

    :param A: Matrix containing text
    :return: permuted Matrix
    """
    S = [[0 for _ in range(4)] for _ in range(4)]  # initialise shifted Matrix
    for i in range(4):
        for j in range(4):
            S[i][j] = A[i][(j - i) % 4]
    return S


# TEST
if __name__ == "__main__":
    def test_shift_rows_enc():
        # Example input matrix (4x4 for illustration)
        A = [
            [0x01, 0x02, 0x03, 0x04],
            [0x05, 0x06, 0x07, 0x08],
            [0x09, 0x0A, 0x0B, 0x0C],
            [0x0D, 0x0E, 0x0F, 0x10]
        ]

        # Expected result after left cyclic permutation
        expected_result = [
            [0x01, 0x02, 0x03, 0x04],
            [0x06, 0x07, 0x08, 0x05],
            [0x0B, 0x0C, 0x09, 0x0A],
            [0x10, 0x0D, 0x0E, 0x0F]
        ]

        # Apply the function
        result_left = shift_rows(A)

        # Check if the result matches the expected outcome
        assert result_left == expected_result, "Test case failed!"

        result_right = shift_rows_inv(expected_result)

        # Check if the result matches the expected outcome
        assert result_right == A, "Test case failed!"


    test_shift_rows_enc()


def xtime(a):
    """
    doubling function in GF(2^8), helper function for multiplication in Galois Field

    :param a: integer, 1 byte
    :return: 2xa in GF(2^8)
    """
    t = a << 1
    if (a >> 7) != 0:
        t ^= 0x1b  # XOR with hex number '1b', corresponding to bitstring '00011011', to stay in Galois field
    return t & 0xFF

# TEST
if __name__ == "__main__":
    a = 0b10010010
    b = 0b00010101
    print('Poly: ', a, 'xtime: ', xtime(a), 'in bin: ', format( xtime(a), 'b'))
    print('\nPoly: ', b, 'xtime: ', xtime(b), 'in bin: ', format( xtime(b), 'b'))

# Multiplication of two polynoms in Galoisfield GF(2^8)
def mult_GF(a1, a2):
    """
    function mult_GF performs multiplication in the Galois field

    :param a1: integer, 1 byte, factor 1 of multiplication
    :param a2: integer, 1 byte, factor 2 of multiplication
    :return: a1 * a2 in GF(2^8)
    """
    res = 0
    for i in range(8):
        if a2 & 1 == 1:
            res ^= a1
            res &= 0xFF  # stay in Galois field
        a1 = xtime(a1)
        a2 >>= 1
    return res

# TEST
if __name__ == "__main__":
    poly1 = 0b00001011
    poly2 = 0b00010110
    print('mult_GF: ', mult_GF(poly1, poly2), "bin: ", format(mult_GF(poly1, poly2), 'b') )  # expected: 1000 1010
    poly1 = 0b11101011
    poly2 = 0b11110110
    print('mult_GF: ', mult_GF(poly1, poly2), "bin: ", format(mult_GF(poly1, poly2), 'b'))  # expected: 01011001



def mix_columns(A):
    """
    function performs Mix Columns operation for AES encryption.

    :param A: matrix,  4x4 list of lists (each entry being an 8-bit integer)
    :return: Transformed matrix after Mix Columns
    """
    # AES Mix Colums encryption matrix
    M_enc = [[0x02, 0x03, 0x01, 0x01],
             [0x01, 0x02, 0x03, 0x01],
             [0x01, 0x01, 0x02, 0x03],
             [0x03, 0x01, 0x01, 0x02]]
    res = [[0 for _ in range(4)] for _ in range(4)]
    for i in range(4): # rows mat 1
        for j in range(4): # cols mat 2
            for k in range(4): # cols mat 1
                res[i][j] ^=  mult_GF( A[k][j], M_enc[i][k] )
    return res

# TEST
if __name__ == "__main__":
    # test case: first col https://crypto.stackexchange.com/questions/2402/how-to-solve-mixcolumns
    A = [
        [0xd4, 0x02, 0x03, 0x04],
        [0xbf, 0x06, 0x07, 0x08],
        [0x5d, 0x0A, 0x0B, 0x0C],
        [0x30, 0x0E, 0x0F, 0x10]
    ]
    res = mix_columns(A)
    print( format( res[0][0] , 'x') )
    print(format(res[1][0], 'x'))
    print(format(res[2][0], 'x'))
    print(format(res[3][0], 'x'))



def mix_columns_inv(A):
    """
    function performs invers Mix Columns operation for AES encryption.
    (very similar to mix_columns, just use different matrix)

    :param A: matrix,  4x4 list of lists (each entry being an 8-bit integer)
    :return: Transformed matrix after Mix Columns invers
    """
    # AES Mix Colums decryption matrix
    M_dec = [[0x0E, 0x0B, 0x0D, 0x09],
             [0x09, 0x0E, 0x0B, 0x0D],
             [0x0D, 0x09, 0x0E, 0x0B],
             [0x0B, 0x0D, 0x09, 0x0E]]
    res = [[0 for _ in range(4)] for _ in range(4)]
    for i in range(4):  # rows mat 1
        for j in range(4):  # cols mat 2
            for k in range(4):  # cols mat 1
                res[i][j] ^= mult_GF(A[k][j], M_dec[i][k])
    return res

# TEST
if __name__ == "__main__":
    A = [
        [0xd4, 0x02, 0x03, 0x04],
        [0xbf, 0x06, 0x99, 0x08],
        [0x5d, 0x0A, 0x0B, 0x0C],
        [0x30, 0x0E, 0x0F, 0xfb]
    ]
    B = mix_columns(A)
    C = mix_columns_inv(B)
    print(A)
    print(C)
    print(B)
    assert A == C, 'matrices not equal'


    input_matrix = [
        [0xdb, 0xdb, 0x53, 0x45],
        [0xf2, 0xf2, 0x22, 0x5c],
        [0x39, 0x01, 0x01, 0x01],
        [0xc6, 0xc6, 0xc6, 0xc6]
    ]


    result_mine = mix_columns(input_matrix)
    print("\nmix_col :")
    for row in result_mine:
        print(" ".join(f"{val:02x}" for val in row))


    result_mine = mix_columns(A)
    print("\nmix_col :")
    for row in result_mine:
        print(" ".join(f"{val:02x}" for val in row))



    print("\nINPUT MATRIX")
    for row in input_matrix:
        print(" ".join(f"{val:02x}" for val in row))


    final = mix_columns_inv(mix_columns(input_matrix))
    print("\nmix_inv(mix(.) ")
    for row in final:
        print(" ".join(f"{val:02x}" for val in row))

####################################################################################
# aes block encryption function


def aes_block_enc(block, keys, sbox = SBOX):
    """
    function performs encryption of one block using AES with the given keys and sbox

    :param block: integer, 128 bit, text block to be encrypted
    :param keys: list of 11 integers, each 128 bit, round keys for encryption K_i
    :param sbox: list of lists, 16x16, with the aes sbox for encryption
    :return: integer, 128 bit, ciphertext
    """
    # initialisation - write block and keys in matrix
    A = int_to_mat(block)
    K = []
    for k in keys:
        K.append( int_to_mat(k) )
    # AES enc alg
    A = add_round_key(A, K[0])
    for i in range(1, 10):
        A = sub_bytes(A, sbox)
        A = shift_rows(A)
        A = mix_columns(A)
        A = add_round_key(A, K[i])
    A = sub_bytes(A, sbox)
    A = shift_rows(A)
    A = add_round_key(A, K[10])
    return mat_to_int(A)  # transform matrix back into integer


def aes_block_dec(block, keys_dec, sbox_inv = SBOX_INV):
    """
    function performs encryption of one block using AES with the given keys and sbox.
    The round keys for decryption D_i are calculated once for all blocks and not inside the aes_block_dec function
    They are calculated with D_0 = K_0 and D_10 = K_10 and for i = 1...9: D_i = mix_columns_inv( K_i )
    (see exercise 2 of sheet 2 or
    https://braincoke.fr/blog/2020/08/the-aes-decryption-algorithm-explained/#the-equivalent-inverse-cipher)
    Using the key transformation (which can be done once for all blocks) results in a structure of the block
    decryption algorithm identical to the structure of the encryption algorithm

    :param block: integer, 128 bit, ciphertext block to be decrypted
    :param keys_dec: list of 11 integers, each 128 bit, round keys for decryption D_i
    :param sbox_inv: list of lists, 16x16, with the aes sbox for decryption (invers sbox)
    :return: integer, 128 bit, plaintext
    """
    # initialisation - write block and keys in matrix
    A = int_to_mat(block)
    D = []
    for d in keys_dec:
        D.append(int_to_mat(d))
    # AES dec alg
    A = add_round_key(A, D[10])
    for i in range(9, 0, -1):
        A = sub_bytes(A, sbox_inv)
        A = shift_rows_inv(A)
        A = mix_columns_inv(A)
        A = add_round_key(A, D[i])
    A = sub_bytes(A, sbox_inv)
    A = shift_rows_inv(A)
    A = add_round_key(A, D[0])
    return mat_to_int(A)  # transform matrix back into integer


def key_trans(keys):
    """
    function performs key transformation from encryption keys K_i to decryption keys D_i
    with D_0 = K_0 and D_10 = K_10 and for i = 1...9: D_i = mix_columns_inv( K_i )
    (as described in the aes_block_dec function description)

    :param keys: list of 11 integers, each 128 bit, round keys for encryption K_i
    :return: list of 11 integers, each 128 bit, round keys for decryption D_i
    """
    keys_dec = [ keys[0] ]
    for i in range(1, 10):
        keys_dec.append( mat_to_int(mix_columns_inv(int_to_mat(keys[i]))) )
    keys_dec.append( keys[10] )
    return keys_dec

# TEST
if __name__ == "__main__":
    plain_1 = load_int_128('Beispiel_1_Klartext.txt')  # works as load_block just as well
    plain_2 = load_int_128('Beispiel_2_Klartext.txt')
    key_0 = load_int_128('key_0.txt')
    # sbox = load_sbox('SBox.txt')
    # sbox_inv = load_sbox('SBoxInvers.txt')
    # keys = key_gen(key_0, sbox)
    keys = [57811460909138771071931939740208549692, 213979707136699034080426665618942227973,
            322683521860691055304824752543874283135, 81748971717375732427529955113938094139,
            318041918978483473513978995397404372224, 282885560754057025014958154753662064060,
            145595319617192629487101070522043110397, 104120947501223618343260406571147385935,
            312132068501784538530058535568082282799, 229247186667434634296614468440630755438,
            276588332753250198369059907516451982502]
    # obtained using key_gen
    print(keys)
    keys_dec = key_trans(keys)
    print("\nkey_dec: \n", keys_dec, "\n")

    crypto_1 = aes_block_enc(plain_1, keys)
    crypto_2 = aes_block_enc(plain_2, keys)

    encrypto_1 = aes_block_dec(crypto_1, keys_dec)
    encrypto_2 = aes_block_dec(crypto_2, keys_dec)

    print("plain 1: ", format(plain_1, 'x'))
    print("dec enc 1: ", format(encrypto_1, 'x'))
    print("enc 1: ", format(crypto_1, 'x'))
    print("----------------------------------")
    print("plain 2: ", format(plain_2, 'x'))
    print("dec enc 2: ", format(encrypto_2, 'x'))
    print("enc 2: ", format(crypto_2, 'x'))
    print("----------------------------------")

    # yields same result as in Beispiel_1/2_Kryptotext.txt :)

