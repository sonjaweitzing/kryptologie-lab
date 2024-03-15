def ac(do_decryption, input_txt, key, output_txt):
    """
    ac_encrypt performs an encryption or the respective decryption with a key provided of a
     text in capital letters with the additive chiffre

    :param do_decryption: boolean indicator: 0 -> Encryption, ADD the key; 1 -> Decryption, SUBTRACT the key
    :param input_txt: .txt file with a text to encrypt in capital letters
    :param key: Integer from 0 to 25
    :param output_txt: .txt file for the cipher text. It can be an existing file, if it does not exist, it is created
    """
    with open(input_txt, 'r', encoding="utf-8") as message, open(output_txt, 'w', encoding="utf-8") as cipher:

        # read character by character
        while True:
            cha = message.read(1)  # read one byte = 1 char from message

            # break while-loop if there is no character left to read
            if not cha:
                break

            # use utf numbers to add key and hence encrypt the message
            # utf number of character c is ord(c)
            # character to utf number n is chr(n)

            # encrypt all capital characters from A to Z
            # ADD or SUBTRACT key using modulo operation to stay in alphabet bounds,
            # + 1 to include 'A' [(ord('Z') - ord('A') = 25]
            modulo = ord('Z') - ord('A') + 1
            if ord('A') <= ord(cha) <= ord('Z'):  # character is capital letter from A to Z
                if do_decryption:
                    enc_cha = chr(((ord(cha) - key - ord('A')) % modulo) + ord('A'))
                else:
                    enc_cha = chr( ((ord(cha) + key - ord('A')) % modulo) + ord('A') )

                # write encrypted character into output file / cipher text
                cipher.write(enc_cha)

            # Leave all other characters unchanged
            else:
                cipher.write(cha)
    return 0