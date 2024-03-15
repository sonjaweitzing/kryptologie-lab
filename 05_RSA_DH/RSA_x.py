from squa_and_mult import squa_and_mult
from sys import argv

"""
Implementation of RSA
"""

try:
    # INPUT using command line
    input_txt = str(argv[1])
    key_txt = str(argv[2])
    output_txt = str(argv[3])

    # py -3 RSA_x.py ExampleText.txt ExampleKey.txt OutputRSAEnc3.txt
    # py -3 RSA_x.py ExampleEncrypted.txt ExampleKeyDecrypt.txt OutputRSADec1.txt

    # # INPUT without command line
    # input_txt = 'C:/Users/sonja/python/KrypLABgit/RSA/RSA_dateien/ExampleText.txt'
    # key_txt = 'C:/Users/sonja/python/KrypLABgit/RSA/RSA_dateien/ExampleKey.txt'
    # output_txt = 'C:/Users/sonja/python/KrypLABgit/RSA/RSA_dateien/OutputRSAEnc.txt'

    with open(key_txt, 'r') as k:
        e_or_d = int(k.readline())
        n = int(k.readline())

    with open(input_txt, 'r') as i:
        x = int(i.read())
        if x < 2**2000 and x < n:  # x < n, da sonst mehrdeutigkeit der Nachricht möglich wäre
            y = squa_and_mult(x, e_or_d, n)

    with open(output_txt, 'w') as o:  # write in txt file
        o.write(str(y))

except FileNotFoundError:
    print("Cannot find input args: [input.txt] [key] [output.txt]")

# It Works!!! :)





# Different Exercise - left in for now in case it's useful later

#
# def RSA_enc(x, e, n):
#     # (e, n) is public key
#     # x is "text" = sequence of numbers to encrypt
#     y = []
#     for i in range(len(x)):
#         y.append(squa_and_mult(x[i], e, n))
#     return y
#
# def RSA_dec(y, d, n):
#     # (d, n) is private key
#     # y is encripted "text" = sequence of numbers to decrypt
#     x = []
#     for i in range(len(y)):
#         x.append(squa_and_mult(y[i], d, n))
#     return x
#
# # TEST
# if __name__ == "__main__":
#     e = 5
#     d = 141
#     n = 391 # gültiger Schlüssel, siehe Übung 3 A3
#     x1 = [1,2,3,4,5,6,7,8,9]
#     x2 = [52, 78, 23, 47, 56, 39, 99]
#     y1 = RSA_enc(x1, e, n)
#     y2 = RSA_enc(x2, e, n)
#     x1_dec = RSA_dec(y1, d, n)
#     x2_dec = RSA_dec(y2, d, n)
#     print('\n', x1, '\n', y1, '\n', x1_dec, '\n\n\n', x2, '\n', y2, '\n', x2_dec)



