#  https://en.wikipedia.org/wiki/SHA-3
import numpy as np


def padding(hexstr, r):
    """
    Padding Funktion
    Add 01 at end of Message. Then add  a 1, j zeros, 0 <= j <= r-1, and add a final 1. -- 0110*1
    Input is given in hexadecimal. Hence, padding can be done in Hexadecimal

    :param hexstr: given input of hex numbers from txt file
    :param r: requiered block length in bit (multiple of 4 for hex-number compatibility) - padded str length is multiple of r
    :return: padded hex string
    """
    # check that r is multiple of 4 and calc block size in hex-character-number
    if r % 4 == 0 and r != 0:
        r_hex = r // 4  #  block length in hexadecimal
    else:
        return "error: r != 0 must be multiple of 4"

    padd_len = r_hex - (len(hexstr) % r_hex)
    # padd_len in hexadecimal, is r_hex if hexstr.len() is already multiple of r_hex
    # -> padd anyway
    # In this case a final block (100..001) with r-2 zeros must be included
    if padd_len > 1:
        return hexstr + '6' + (padd_len - 2) * '0' + '1'  # hexstr + 0110 + (r_hex - 2) * 0000 + 0001
    else:  # padd_len = 1 ... entspricht 4 bits - includes case that r_hex = 1
        return hexstr + '7'  # 7 = 0111 padding if r = 4 -> r_hex = 1


if __name__ == "__main__":
    h = "BEA7D009728"
    r = 32
    res = padding(h, r)
    print("blocksize: ", r)
    print("original string: ",h)
    print("padded string: ",res)

    h = "BEA7D009728"
    r = 16
    res = padding(h, r)
    print("blocksize: ", r)
    print("original string: ", h)
    print("padded string: ", res)

    h = "BEA7BEA7BEA7"
    r = 16
    res = padding(h, r)
    print("blocksize: ", r)
    print("original string: ", h)
    print("padded string: ", res)



#####################################################################################################

# Block to Array

# Block b = r + c
# a[i][j][k] (5 x 5 x 64 - Array) i...row, j...column, k...bit
# a[i][j][k] is bit ( ( 5i + j ) x w + k ) of the input block, where w is 64
# 5 * 5 * 64 = 1600 = b ... blocklength

def hexstr_to_array(hex_string):
    """
    convert hex string to 5x5x64 array

    :param hex_string: hex string, 1600 bits
    :return: 5x5x64 array
    """
    # Convert the hex string to bytes
    byte_data = bytes.fromhex(hex_string)

    # Create a boolean array from the bytes
    bool_array = np.unpackbits(np.frombuffer(byte_data, dtype=np.uint8), bitorder='little')

    # Reshape the array to 5x5x64
    bool_array = bool_array.reshape(5, 5, 64)

    return bool_array

def array_to_hexstring(bool_array):
    """
    convert 5x5x64 array to hex string

    :param bool_array: 5x5x64 array
    :return: hex string, 1600 bits
    """
    # Reshape the array to a 1D array
    flat_array = bool_array.ravel()

    # Convert the boolean array to bytes
    byte_data = np.packbits(flat_array, bitorder='little').tobytes()

    # Convert bytes to hexadecimal string
    hex_string = byte_data.hex()

    return hex_string

if __name__ == "__main__":
    # Example usage:
    input_hex = "8e71c61de6a2321336184f813379ec6bf4a3fb79" * 10 # 400 hexstr = 1600-bit hex string
    print("Length: ",len(input_hex))
    bool_array = hexstr_to_array(input_hex)
    output_hex = array_to_hexstring(bool_array)

    print("Input Hex String (1600 bits):", input_hex)
    print("Boolean Array Shape:", bool_array.shape)
    print(bool_array)
    print("Output Hex String:", output_hex)

    # Check if input and output hex strings are equal
    if input_hex == output_hex:
        print("Input and Output Hex Strings are equal.")
    else:
        print("Input and Output Hex Strings are different.")


#####################################################################################################
# getting the hex stings in a format for the functions to work with (compacting) and
# formatting them into an easy to read string
def compact_hex_string(hex_string):
    """
    helper function to format hex string for use in function

    :param hex_string:
    :return:
    """
    # Remove any spaces and line breaks from the input string
    hex_string = hex_string.replace(" ", "")
    hex_string = hex_string.replace("\n", "")
    return hex_string

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
        if i % 2 == 0:
            formatted_result += hex_string[i:i + 2] + " "
    return formatted_result



##########################################################################################################


# Theta: Parität einer Spalte berechnen

def parity(bool_array):
    """
    helper function to calc parity of an np-bool_ array

    :param bool_array: 5x5x64 array (boolean)
    :return: parity
    """
    return np.sum(bool_array) % 2

def theta(a):
    """
    Theta function from SHA-3-224, parity of column

    :param a: 5x5x64 np.bool_ array
    :return: theta(a)
    """
    # Clac all parities of all 5 x 64 columns
    a_parity = np.zeros((5, 64), dtype=np.bool_)
    for j in range(5):
        for k in range(64):
            a_parity[j, k] = parity(a[:, j, k])
    # XOR parities into array
    for i in range(5):
        for j in range(5):
            for k in range(64):
                a[i, j, k] = a[i, j, k] ^ a_parity[(j-1) % 5, k] ^ a_parity[(j+1) % 5, (k-1) % 64]
    return a


# some tests:
if __name__ == "__main__":
    # Test parity
    bool_array = np.array([True, False, True, False, True])
    print("Parity: \n", parity(bool_array))  # Expected output: True

    # Test theta
    a2 = np.ones((5, 5, 64), dtype=np.bool_)  # A 5x5x64 array of True values
    print("------------------------------------")
    print(theta(a2))  # Expected output: A 5x5x64 array of False values



##########################################################################################################

# function rho - bitwise rotation
def rho(a):
    """
    Rho function from SHA-3-224, bitwise rotation

    :param a: 5x5x64 np.bool_ array
    :return: rho(a)
    """
    b = np.zeros((5, 5, 64), dtype=np.bool_)
    # w from table (moodle)
    w = np.array(  [[0, 1, 62, 28, 27],
                    [36, 44, 6, 55, 20],
                    [3, 10, 43, 25, 39],
                    [41, 45, 15, 21, 8],
                    [18, 2, 61, 56, 14]])
    for i in range(5):
        for j in range(5):
            b[i, j, :] = a[i, j, :] << (w[i, j] % 64)
    return b


##########################################################################################################

# function pi - permutation
# following instructions on slides a[i][j] = a[j][3i + j] (different on wikipedia)
def pi(a):
    """
    Pi function from SHA-3-224, permutation

    :param a: 5x5x64 np.bool_ array
    :return: pi(a)
    """
    b = np.zeros((5, 5, 64), dtype=np.bool_)
    for i in range(5):
        for j in range(5):
            b[i, j, :] = a[j, (3 * i + j) % 5, :]
            # following wikipedia: https://de.wikipedia.org/wiki/SHA-3
            # b[( 3*i + 2*j ) % 5, i] = a[i, j]
    return b


##############################################################################################################

# function chi: Nichtlineare Bitweise Operationen
def chi(a):
    """
    Chi function from SHA-3-224, nonlinear bitwise rotation

    :param a: 5x5x64 np.bool_ array
    :return: chi(a)
    """
    b = np.zeros((5, 5, 64), dtype=np.bool_)
    for i in range(5):
        for j in range(5):
            b[i, j, :] = a[i, j, :] ^ ( ~ a[i, (j+1) % 5, :] & a[i, (j+2) % 5, :])
    return b

##############################################################################################################

# function iota: XOR Rundenkonstante C_R - table copied form moodle
def iota(a, r):
    """
    Iota function from SHA-3-224, xor round constant
    C_R - table copied form moodle

    :param a: 5x5x64 np.bool_ array
    :param r: r is current round index, 0 <= r <= 23
    :return: iota(a, r)
    """
    C = [   0x0000000000000001,
            0x0000000000008082,
            0x800000000000808A,
            0x8000000080008000,
            0x000000000000808B,
            0x0000000080000001,
            0x8000000080008081,
            0x8000000000008009,
            0x000000000000008A,
            0x0000000000000088,
            0x0000000080008009,
            0x000000008000000A,
            0x000000008000808B,
            0x800000000000008B,
            0x8000000000008089,
            0x8000000000008003,
            0x8000000000008002,
            0x8000000000000080,
            0x000000000000800A,
            0x800000008000000A,
            0x8000000080008081,
            0x8000000000008080,
            0x0000000080000001,
            0x8000000080008008 ]
    C_r_bits = np.array(list(format(C[r], '064b')), dtype=bool)  # convert current round constant into bits
    a[0, 0, :] ^= C_r_bits
    return a

######################################################################################################
# function f

def f(a):
    """
    function f for sponge construction of SHA-3-224
    Do 24 rounds of appliing theta, rho, pi, chi, iota
    r is round index 0 <= r < 24

    :param a: 5x5x64 np.bool
    :return: f(a)
    """
    for r in range(24):
        a = theta(a)
        a = rho(a)
        a = pi(a)
        a = chi(a)
        a = iota(a, r)
    return a

#####################################################################################################

# SHA3-224

# Konstanten
# d_const = 224
# r_const = 1152
# c_const = 448
# b_const = r_const + c_const

def SHA_3_224(N, d = 224, r = 1152, c = 448):
    """
    function performing SHA-3-224

    :param N: message given as a hexstr
    :param d: hashsize, optional, integer, constant, 224 per default
    :param r: rate, optional, integer, constant, 1152 per default
    :param c: capacity, optional, integer, constant, 448 per default
    :return: hashvalue of N
    """
    # check that r is multiple of 4 and calc block size in hex-character-number
    if r % 4 == 0 and r > 0:
        r_hex = r // 4  #  block length in hexadecimal
    else:
        return "error: r > 0 must be multiple of 4"

    # check that c is multiple of 4 and calc capacity size in hex-character-number
    if c % 4 == 0:
        c_hex = c // 4  #  c in hexadecimal
    else:
        return "error: c must be multiple of 4"

    # check that d is multiple of 4 and calc hashlength in hex-character-number
    if d % 4 == 0 and d > 0:
        d_hex = d // 4  # c in hexadecimal
    else:
        return "error: d > 0 must be multiple of 4"

    # compact hex string N
    N = compact_hex_string(N)

    # SHA-3
    N = padding(N, r)
    S = np.zeros((5, 5, 64), dtype=np.bool_)
    for i in range(0, len(N), r_hex):
        # print("i: ",i)
        P_i_and_c = hexstr_to_array( N[i : i + r_hex] + c_hex * '0' )
        # concatenate capacity to current block P_i of hexstr and form into array;
        # c is capacity in bits -> c // 4 is capacity in hex
        S = f( S ^ P_i_and_c)
    S_str = array_to_hexstring(S)
    Z = S_str[ : d_hex]

    # format hash value
    Z = format_hex_string(Z)
    return Z


# Testing
if __name__ == "__main__":
    N_str = "Hello, world!"
    encoded_bytes = N_str.encode("utf-8")
    N_hexstr = encoded_bytes.hex()
    print("-------------------------------------")
    print("-------------------------------------")
    print(f"Original String: {N_str}")
    print(f"Hex String: {N_hexstr}")

    hash = SHA_3_224(N_hexstr)

    print("Hash: ", hash)
    print("Hash length in hex (224 = 4 * 56): ", len(hash))

    N_str = "My Hashing function seems to actually work..."
    encoded_bytes = N_str.encode("utf-8")
    N_hexstr = encoded_bytes.hex()
    print("-------------------------------------")
    print("-------------------------------------")
    print(f"Original String: {N_str}")
    print(f"Hex String: {N_hexstr}")

    hash = SHA_3_224(N_hexstr)

    print("Hash: ", hash)
    print("Hash length in hex (224 = 4 * 56): ", len(hash))

    N_str = "This is a very long message for another test..." * 100
    encoded_bytes = N_str.encode("utf-8")
    N_hexstr = encoded_bytes.hex()
    print("-------------------------------------")
    print("-------------------------------------")
    print(f"Original String: {N_str[ : 50]} ...")
    print("len hex string: ", len(N_hexstr))
    print(f"Hex String: {N_hexstr[ : 20]} ...")


    hash = SHA_3_224(N_hexstr)

    print("Hash: ", hash)
    print("Hash length in hex (224 = 4 * 56): ", len(hash))

