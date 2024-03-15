def vig(do_decryption, input_txt, key, output_txt):
    """
    Procedure to encrypt and decrypt messages using the vigenere chiffre with a provided key.
    (Implementation very similar to additive chiffre)

    :param do_decryption: boolean, 0 -> Encryption, ADD key, 1 -> Decryption, SUBTRACT key and write key into first line of output file
    :param input_txt: .txt file with a text to encrypt in capital letters
    :param key: string of length d, capital letters
    :param output_txt: .txt file for the cipher text. It can be an existing file, if it does not exist, it is created
    """
    # open input and output files
    with open(input_txt, 'r', encoding="utf-8") as message, open(output_txt, 'w', encoding="utf-8") as cipher:

        if do_decryption:
            # write key into first line of file if decryption
            cipher.write(key)
            cipher.write('\n')

        # use the right character from key for each text character by updating a pointer p for the current position
        # in the key
        p = 0

        # read character by character
        while True:
            cha = message.read(1)  # read one byte = 1 char from message
            # break while-loop if there is no character left to read
            if not cha:
                break

            # use utf numbers to add key and hence encrypt the message
            # utf number of character c is ord(c)
            # character to utf number n is chr(n)

            add = ord(key[p]) - ord('A')  # current character key, modifier to add to character utf number
            # A = 0, B = 1, ...

            # encrypt all bold characters from A to Z, use modulo operation to stay in alphabet bounds
            # ADD or SUBTRACT current character key "add"
            modulo = ord('Z') - ord('A') + 1
            if ord('A') <= ord(cha) <= ord('Z'):  # character is bold letter from A to Z
                if do_decryption:
                    enc_cha = chr(((ord(cha) - add - ord('A')) % modulo) + ord('A'))
                else:
                    enc_cha = chr(((ord(cha) + add - ord('A')) % modulo) + ord('A'))

                # write encrypted character into output file / cipher text
                cipher.write(enc_cha)

                # update key. skipped characters do not use key. increment key position using modulo operation
                p = (p + 1) % len(key)

            # Leave all other characters unchanged
            else:
                cipher.write(cha)
    return 0
