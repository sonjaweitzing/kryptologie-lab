from SPN import SPN_enc, SPN, SBOX, INVSBOX
import random


def generate_hex_strings(n, l):
    """
    helper function to generate n random hex strings of length l

    :param n: number of hex strings
    :param l: length of hex strings
    :return: n random hex strings
    """
    hex_strings = []
    for i in range(n):
        hex_string = ''.join(random.choice('0123456789abcdef') for j in range(l))
        hex_strings.append(hex_string)
    return hex_strings


def make_pairs(n, key, enc_fct = SPN_enc, l = 4, clear_txt = 'cleartexts.txt', crypto_txt = 'cryptotexts.txt'):
    """
    Produce n cleartext-cryptotext pairs (hexstrings) and write into two respective .txt files

    :param n: desired number of pairs
    :param key: encryption key
    :param enc_fct: function that is used for encryption, args: (message, key)
    :param l: length of pairs
    :return: n pairs in the two .txt files cleartexts.txt and cryptotexts.txt
    """
    cleartexts = generate_hex_strings(n, l)
    cryptotexts = []
    for ct in cleartexts:
        cryptotexts.append( enc_fct( ct, key ) )

    # Write cleartexts to a file
    with open(clear_txt, 'w') as f:
        for item in cleartexts:
            f.write("%s\n" % item)

    # Write cryptotexts to a file
    with open(crypto_txt, 'w') as f:
        for item in cryptotexts:
            f.write("%s\n" % item)


##################################################################################################

# subkey can be used for any approx in general
# define approx, that is given for the LAB exercise

def approx_satisfied(x5, x7, x8, u6, u8, u14, u16):
    """
    function that returns 1 if approx from slides is satisfied and else 0
    """
    if x5 ^ x7 ^ x8 ^ u6 ^ u8 ^ u14 ^ u16 == 0:
        return 1
    else:
        return 0


# subkey (using alg from slides)

# here subkey len = 2 (L_1, L_2) per default because 2 s-boxes are active in 4th round
def subkey(cleartexts_txt, cryptotexts_txt, approx_sat = approx_satisfied, invsbox = INVSBOX):
    """
    function to find most likely subkey for the clear-crypto-pairs provided

    :param cleartexts_txt: path to txt file containing cleartexts
    :param cryptotexts_txt: path to txt file containing matching cryptotexts
    :param approx_sat: function that returns "1" if a specifiec approx is satisfied, else "0"
    :param invsbox: invers S-Box, treated as constant
    :return: most likely subkey, unknows key characters marked with "*"
    """
    # clear, cryptotexts have length 4 hex (= 16 bit)
    # texts are given as txt files with one text per line
    # initialiase alpha as 16x16 table
    alpha =  [[ 0 for i in range(0xF + 1) ] for j in range(0xF + 1)]

    # Read cleartexts and cryptotexts from files (in same dic)
    with open(cleartexts_txt, 'r') as f:
        cleartexts = [line.strip() for line in f]
    with open(cryptotexts_txt, 'r') as f:
        cryptotexts = [line.strip() for line in f]

    # check and determine number of pairs |M| = t
    assert len(cleartexts) == len(cryptotexts)
    t = len(cleartexts)

    # fill in alpha for each clear-crypto pair
    for clear, crypto in zip(cleartexts, cryptotexts):
        # format as int
        clear_int = int(clear, 16)
        crypto_int = int(crypto, 16)
        # loop over all possible tupels L_1, L_2
        for i in range((0xF + 1) ** 2):
            L_1, L_2 = divmod(i, 0xF + 1)  # L_1, L_2 are integers

            # do invers SPN Operations on hex num (2) = bits 5:8 and (4) = bits 12:16, because these are the active S-Boxes

            # Notation: u_2 = u^4_(2) etc, u6 is sixth bit of u^4 etc
            # hence u_2 is hex chara while u2 is bit

            v_2 = L_1 ^ ( (crypto_int >> 8) & 0xF)  # int, right shift by 8 and bitwise AND with 0xF to get the bits 5:8
            v_4 = L_2 ^ ( (crypto_int ) & 0xF)  # int, analog, no shift neccessary to get bits 12:16
            u_2 = invsbox[ v_2 ]   # inv subs
            u_4 = invsbox[ v_4 ]  # inv subs

            # get the bits needed for approx:
            x5 = (clear_int >> 11) & 1  # gets 5th bit from clear-str - right shift by 16 - 5 = 11
            x7 = (clear_int >> 9) & 1  # 7th
            x8 = (clear_int >> 8) & 1  # 8th
            u6 = (u_2 >> 2) & 1  # 6th bit of u is second bit of u_2
            u8 = u_2 & 1  # 8th bit is last bit of u_2
            u14 = (u_4 >> 2) & 1  # 14th ...
            u16 = u_4 & 1  # 16th ...

            if approx_sat( x5, x7, x8, u6, u8, u14, u16):
                alpha[L_1][L_2] += 1

    #print(alpha)

    # find maximum in alpha
    max = -1
    # initialise beta
    beta =  [[ 0 for i in range(0xF + 1) ] for j in range(0xF + 1)]
    maxkey = []
    for i in range((0xF + 1) ** 2):
        L_1, L_2 = divmod(i, 0xF + 1)
        beta[L_1][L_2] = abs( alpha[L_1][L_2] - t // 2 )
        if beta[L_1][L_2] > max:
            max = beta[L_1][L_2]
            maxkey = [L_1, L_2]
    #print(beta)
    maxkey = "*" + format(maxkey[0], 'x') + "*" + format(maxkey[1], 'x')
    return maxkey


############################################################################################################

# trial and error - how many pairs are needed? theory: ~ 8000

NUM_PAIRS = 8000

def find_subkey(num_pairs = NUM_PAIRS):
    """
    finds most likely subkey for a given number of pairs

    :param num_pairs: integer, number of pairs
    :return: most likely subkey
    """

    # number of pairs used
    print("Number of pairs: ", num_pairs)

    # define key at random, keylength = 4
    key = ''.join(random.choice('0123456789abcdef') for j in range(4))
    print("Key: ", key)

    # make pairs
    make_pairs(num_pairs, key, SPN)  # creates cleartexts.txt and cryptotexts.txt

    # find subkey
    maxkey = subkey( "cleartexts.txt", "cryptotexts.txt" )

    print("Most likely subkey: ", maxkey)
    if key[1] == maxkey[1] and key[3] == maxkey[3]:
        print("CORREKT SUBKEY!")
    else:
        print("WRONG SUBKEY")
    print("\n---------------------------------------------------------------------\n")


if __name__ == "__main__":
    count = 8
    num_pairs = 2**count
    while num_pairs <= NUM_PAIRS*4:
        find_subkey(num_pairs)
        count += 1
        num_pairs = 2**count

# finds correct subkey for > 8000 pairs pretty much all the time.
# for ~ 4000 or even ~ 2000 sometimes right, but not always