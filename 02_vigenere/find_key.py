import numpy as np
from collections import Counter


def calc_ic(text):
    """
    calc_ic function calculates the coincidence index (IC) of a given text

    :param text: string of capital letters
    :return: coincidence index of the text
    """
    n = len(text)  # text length
    h = Counter(text)  # absolute frequency counter for all characters
    ic = 0
    for a in 'ABCDEFGHIJKLMNOPQRSTUVWXYZ':
        ic += h[a] * (h[a] - 1)
    ic /= n * (n - 1)
    return ic


def find_key_length(text_txt):
    """
    find_key_len is a function that determines the length of a vigenere key from the IC

    :param text_txt: .txt file with a ciphertext in capital letters, for which the key length shall be determined
    :return: key length (that results in a maximal IC)
    """
    max_key_len = 100
    ic_lst = np.zeros(max_key_len)  # initialise list for IC
    with open(text_txt, 'r') as f:  # read txt file
        content = f.read()
        letters = []
        for c in content:
            if c.isupper():  # use only capital letters for decryption, ignore other characters
                letters.append(c)
        for i in range(1, max_key_len + 1):
            if len(letters) >= i:  # if input text is too short, function will not work
                while len(letters) % i != 0:  # padding of string so that it can be reshaped into matrix with i columns
                    letters.append('0')
                a = np.array(letters).reshape(-1, i)
                ic_values = []
                for j in range(i):  # calculate IC for each column separately, build average, add to list
                    column = a[:, j]
                    column_str = ''.join(column)
                    ic = calc_ic(column_str)
                    ic_values.append(ic)
                    ic_lst[i - 1] = np.mean(ic_values)
        key_len_max_ic = np.argmax(ic_lst) + 1  # gives key length i of maximal IC
        # print(max_ic)
        # print(ic_lst[max_ic-1])
        # print(ic_lst)
        delta = 0.05 * ic_lst[key_len_max_ic - 1]  # tolerance, key length might be shorter than max IC key length
        # tolerance is chosen as 5%, can be adjusted
        for i in range(1, key_len_max_ic + 1):
            if ic_lst[i - 1] >= (ic_lst[key_len_max_ic - 1] - delta):
                return i
                # if there is high IC within tolerance delta but with smaller key length return this key length
    return key_len_max_ic  # otherwise return max_ic


# TEST
if __name__ == "__main__":
    kl = find_key_length('Kryptotext_TAG.txt')
    print("key_length", kl)


def find_key_len_1(string):
    """
    finds key of vigenere encrypted text
    same procedure as for additive Chiffre, but function operates with strings as input/output instead of .txt

    finds 1 character key using frequency analysis (like addChiffre)
    key is returned as LETTER (not number)

    :param string: string to find key for
    :return: key as cha or -1 if no valid key is found
    """
    ctr = Counter(string)
    for cha, count in ctr.most_common():  # cha, count as var necessary for cha to be character
        if ord('A') <= ord(cha) & ord(cha) <= ord('Z'):  # character is bold letter from A to Z
            key = chr(((ord(cha) - ord('E')) % (ord('Z') - ord('A') + 1)) + ord('A'))
            return key
    return -1  # no key found (because txt contains no bold letters etc)


def find_key(key_len, input_txt):
    """
    finds key of vigenere encrypted text

    :param key_len: key length of vigenere key, integer
    :param input_txt: .txt file with ciphertext
    :return: key as string of length "key_len"
    """
    key = ''  # initialise string for key
    with open(input_txt, 'r') as f:  # read txt file
        content = f.read()
    letters = []
    for c in content:
        if c.isupper():  # use only capital letters for decryption, ignore other characters
            letters.append(c)
    while len(letters) % key_len != 0:  # padding of string so that it can be reshaped into matrix with i columns
        letters.append('0')
    a = np.array(letters).reshape(-1, key_len)
    for j in range(key_len):  # calculate key for each column separately, add to string
        column = a[:, j]
        column_str = ''.join(column)
        # print(find_key(column_str))
        key += find_key_len_1(column_str)
        # print(Counter(column_str))
    return key


# TEST
if __name__ == "__main__":
    print('findkey test - expected: B')
    print(find_key_len_1(
        'ABCDFFFFFFFFFFFFFFFFGHI'))  # expected: key = A (= 1) because F is most frequent letter "E + 1 = F"
    print('\nfindkey test - expected: J')
    print(find_key_len_1('ABNNNNNNNNNNNNNNCDEF'))

    print(find_key(5, 'C:/Users/sonja/python/KrypLABgit/vigenere/ABCkex.txt'))

    str1 = 'IOAKTESNHTDASRFMISRBTGECIERSNPCRGRBTGDBTGGNFMIEEHFGIPLIESEEELIAZLNRCNSDNLEVDWTHTDSNHTSNUEAUUKMITNFMIRNUIOAKEWKNGIMSTRNNNNTBKUSTEESEGAWTTINDÃKGGPKGUUFTVTKHTGGPQNGTNGFGUNPPXKTEQIPGGVFKYYCGGGGPKKPTVCGPCHOTFKQCMVPPKJHFUÃJÃSNEMGCEEUDZUTOFT'
    str2 = 'OSUJEXTTBVQYEJPBPWBFVETIUSGTHFIVWBFVVVFSVWJPBPOTBUUFJUOODJOSMOIVMCFIENFFFOPFJTBVXTTBCIAOSMOOPVLJJPBLJFOOSUFOJFBPUFPXFXEHEFBFOZFEVFEJMFBSCVTNGIRTCLIIVAWTCUDLSGMEROEUDGTTGNAVTHLIDDAUWSIIRINRNDTNDIEGRTNOIEINRTIEDASEEDSPIDUEVPMIJOFJVOFFO0'
    str3 = 'HOKUKKGEHPTKGPTVPGTKPKKOFGCWUKGPGTKPPGTCPQPTVPDEGKUUGGGVJFFQGPGCGGKGGQTPDUPTTEHPKGEHKKWVJVIFOPCQPTVGPPFHOKTVENNTJPHCCGWGCPPPFUOKPTKVGNPGGPVEXUFXLOFOFOPMIFJPVLQYQCNOJFBVJPUFFOPFJJSOFFFSCUMOVNFBFOSJFSTSFOFGNJTJZNDTMBUDWJWPGGKMVHTGMHTHG0'

    print('\n TEST: \n')

    print(find_key_len_1(str1))
    print(find_key_len_1(str2))
    print(find_key_len_1(str3))
    print(Counter(str1))

    Klartext = 'INFORMATIK IST DIE WISSENSCHAFT UND PRAXIS DER INFORMATIONSVERARBEITUNG, DIE SICH MIT DER ERFASSUNG, SPEICHERUNG, VERARBEITUNG UND UEBERTRAGUNG VON INFORMATIONEN BESCHAEFTIGT. SIE SPIELT EINE ENTSCHEIDENDE ROLLE IN NAHEZU ALLEN BEREICHEN DES MODERNEN LEBENS, VON DER WIRTSCHAFT UND WISSENSCHAFT BIS HIN ZU UNTERHALTUNG UND KOMMUNIKATION. INFORMATIKERINNEN UND INFORMATIKER ENTWICKELN ALGORITHMEN, SOFTWARE-ANWENDUNGEN, DATENBANKEN UND SYSTEME, DIE UNSERE DIGITALE WELT ANTREIBEN UND STÄNDIG WEITERENTWICKELN. SIE SIND VERANTWORTLICH FUER DIE LOESUNG KOMPLEXER PROBLEME UND DIE GESTALTUNG INNOVATIVER TECHNOLOGIEN, DIE DIE ART UND WEISE, WIE WIR ARBEITEN, LERNEN UND MITEINANDER INTERAGIEREN, TRANSFORMIEREN. DIE INFORMATIK IST EIN DYNAMISCHES FELD, DAS STÄNDIG WÄCHST UND NEUE MOEGLICHKEITEN FUER DIE ZUKUNFT EROEFFNET.'
    print(Counter(Klartext))
