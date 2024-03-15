def get_sbox(sbox_txt):
    """
    Reads an S-box from a text file and returns it as a list of strings.

    :param sbox_txt: Path to the .txt file containing the S-box.
    :return: List of strings representing the S-box.
    """
    with open(sbox_txt, 'r') as f:
        lines = f.readlines()
    sbox = []
    for line in lines:
        # split the line into characters and convert each to a hex number
        columns = [col for col in line.strip()]
        sbox.extend(columns)
    return sbox


def get_approx(approx_txt):
    with open(approx_txt, 'r') as f:
        lines = f.readlines()
    approx = []
    for line in lines:
        # split the line into columns and strip whitespace
        # columns = [int(col.strip(), 16) for col in line.split()]
        columns = [col.strip() for col in line.split()]
        approx.append(columns)
    return approx


if __name__ == "__main__":
    print("S-Box: ", get_sbox("Beispiel_SBox.txt"))
    print("Approximation: ", get_approx("Beispiel_Approximation.txt"))

# calc bias
# helper function calculating xor of bits in integer (= parity)
def xor_bits(n):
    """
    Calculates the XOR of the bits in an integer (parity).

    :param n: Integer value.
    :return: XOR of the bits.
    """
    result = 0
    while n:
        result ^= n & 1
        n >>= 1
    return result

def bias(sbox, approx_sbox):
    """
    Calculates the bias of an S-box approximation.

    :param sbox: List of strings representing the S-box.
    :param approx_sbox: Hexadecimal string representing the approximation S-box.
    :return: Bias value.
    """
    # sbox is list of hex numbers (as str)
    # approx_sbox is str with two hex numbers, first number input, last number output
    L_a_b = 0
    for i in range(16):
        # bits that are used in approx
        # bits of sbox input and output (U1, ..., U4, V1, ..., V4)
        sbox_bits = format(i, 'x') + sbox[i]
        # bits of approximation in/out are given directly in approx_sbox (eg. 'B8')
        # get bits that are relevant for calculating L_a_b
        bits = int(sbox_bits, 16) & int(approx_sbox, 16)
        if xor_bits(bits) == 0:
            L_a_b += 1
    return (L_a_b - 8) / 16.0

def approx_quality(sbox_txt, approx_txt):
    """
    Calculates the approximation quality of an S-box.

    :param sbox_txt: Path to the .txt file containing the S-box.
    :param approx_txt: Path to the .txt file containing the approximation matrix.
    :return: Approximation quality.
    """
    sbox = get_sbox(sbox_txt)
    approx = get_approx(approx_txt)
    T_S_total = 1.0 / 2.0  # becauase PuL: epsilon(...) = 2^(n-1) prod epsilon_i
    # use  definition of Piling up Lemma from lecture slides, WITH factor 2^(n-1),
    # not as given on LAB slides LinAna2. If not wanted, change factor 2 here and in T_S_total calc

    # check if approx is valid, therefore if at least one sbox is active, using "flag": all_inactive
    all_inactive = 1
    # calc prod of biases of active sboxes - Piling-up-lemma
    for row in approx:
        for approx_sbox in row:
            # only active sboxes
            if approx_sbox != '00':
                all_inactive = 0
                T_S_total *= 2*abs(bias(sbox, approx_sbox))
    if all_inactive:
        return -1
    else:
        return T_S_total

if __name__ == "__main__":
    quality = approx_quality("Beispiel_SBox.txt", "Beispiel_Approximation.txt")
    print("Quality: ", quality)
    print("Expected quality (lecture): ", 1.0 / 32.0)
