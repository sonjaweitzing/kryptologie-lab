# Kryptologie LAB 2023/24 Sonja Weitzing

Python implementations of classical and modern cryptographic algorithms, written for the cryptology lab course at the University of Jena: the additive and Vigenère ciphers (including breaking them by frequency analysis), AES with the ECB, CBC, OFB and CTR modes of operation, linear cryptanalysis of an SPN, RSA and Diffie-Hellman key exchange, and the SHA-3 hash function.


## Overview

This is a collection of programs for the cryptology LAB course 2023/24. All programs are written in python. For some programs (vigenere and SHA-3) the “numpy” package is required. Hence installing “numpy” might be necessary, before the programs can be executed (for example using "pip install numpy").



## 01 Additive Chiffre

**Files:**

`ac.py`  ...  procedure for encryption or decryption with given key

`find_key.py`  ...  finds the key of an encrypted German text using frequency analysis

`ac_enc.py`  ...  script for encryption:
`ac_enc.py [input_txt] [key] [output_txt]`

`ac_dec.py` ...  script for decryption (with known key):
`ac_dec.py [input_txt] [key] [output_txt]`

`ac_dec_find_key.py` ... script for decryption (with an unknown key):
`ac_dec_find_key.py [input_txt] [output_txt]`

**Description:**

The procedure “ac” can be used to encrypt or decrypt texts in capital letters with a key. The input and output files are given as .txt files, and a function parameter specifies, whether encryption (ADDING the key) or decryption (SUBTRACTING the key) is done. The function “find_key” finds the key of a given ciphertext using frequency analysis. From this, the three scripts ac_enc.py, ac_dec.py and ac_dec_find_key.py are created to encrypt or decrypt (with known or unknown key) a text provided. These three scripts can be called using the command line (e.g. commands below).

**Example Commands:**

(Using Klartext_1.txt and Kryptotext_1_Key_7.txt)
```
py -3 ac_enc.py Klartext_1.txt 7 ac_enc_output.txt
py -3 ac_dec.py Kryptotext_1_Key_7.txt 7 ac_dec_output.txt
py -3 ac_dec_find_key.py Kryptotext_1_Key_7.txt ac_dec_key_output.txt
```


## 02 Vigenere

**Files:**

`vig.py`  …  procedure to encrypt or decrypt messages using the vigenere chiffre with a key provided

`find_key.py`  …  functions to determine the key length and the key (string) of a vigenere encrypted text

`vig_enc.py` …  script for encryption:
`vig_enc.py input.txt key output.txt`

`vig_dec.py` …  script for decryption (with an unknown key):
`vig_dec.py input.txt output.txt`

**Description:**

The function “vig” encrypts or decrypts texts (capital letters) with the vigenere chiffre for a provided key. The function “find_key_length” determines the most likely key length from the coincidence index of a cipher text. The function “find_key” finds the key of a vigenere encrypted text using frequency analysis. The script vig_enc.py can be called to encrypt a plain text. The script vig_dec.py decrypts a given ciphertext with an unknown key.

Numpy is necessary for this code to work.

**Example Commands:**

(Using Klartext_1.txt and Kryptotext_TAG.txt)
```
py -3 vig_enc.py Klartext_1.txt TAG vig_enc_output.txt
py -3 vig_dec.py Kryptotext_TAG.txt vig_dec_output.txt
```



## 03 AES

**Files:**

`key_gen.py` …  functions to generate 11 round keys from a single 128 bit key.

`aes_block.py` …  functions realizing the encryption of one 128 bit block, when the 11 round keys are provided

`modi.py` …  functions realising four operation modi for block chiffres: ECB, CBC, OFB and CTR

`aes.py` …  function combining key generation, block encryption and operation modi into an AES encryption for texts.

`aes_enc.py` …  script for encryption: 
`aes_enc.py [modus] [Input_txt] [key_txt] [Output_txt] ([IV] if required (for CBC, OFB))`

`aes_dec.py` …  script for decryption:
`aes_dec.py [modus] [Input_txt] [key_txt] [Output_txt] ([IV] if required (for CBC, OFB))`


**Description:**

The AES module contains programs for the operation modi, the aes block encryption (128 bit block length) and the aes key generation.

The key generation generates 11 round keys from a single 128 bit key provided.

The AES block encryption realizes the encryption or decryption function of AES.

Both the key generation and the AES block encryption mainly work on integers, using bitwise operations. The S-box and inverse S-box must be provided as txt files. They are loaded in the program using a helper function and then treated as constants.

The modi take formatted hex strings as an input and produce them as output (only hex numbers, no whitespaces etc.). The key for the modi must be provided in whatever form the used encryption function needs it. In case of AES as a list of 11 round keys for the aes_block_enc or aes_block_dec function. The initialization vector is passed as an Integer.

In the file aes.py the aes function combines the key generation, block encryption and operation modi into an AES encryption or decryption for texts. To make in- and output using .txt files with hexadecimal numbers possible, helper functions for conversion are used in the final AES implementation. The input and output of texts, the 128 bit key and if necessary an initialization vector is done using .txt files containing hex strings. The files can contain whitespaces etc. for better readability.

To call the aes function from the command line the two scripts aes_enc.py and aes_dec.py were created. They can be used as illustrated in the example commands below.

When using CBC or OFB an initialization vector must be given as an argument, otherwise an error will occur. Providing an obsolete IV for ECB or CTR mode will not cause an error, the IV simply has no effect, as it is not used for these modi.

**Example Commands:**

(Using Beispiel_1_lang_klar.txt which is simply a combination of the example blocks Beispiel_1_Klartext.txt and Beispiel_2_Klartext.txt; key_0.txt which is the first round key from Beispiel_key.txt; iv_0.txt which is the zero vector for initialization. iv.txt can be used to try a different initialization vector)
Encryption in all modi
```
py -3 aes_enc.py ECB Beispiel_1_lang_klar.txt key_0.txt out_enc_ECB.txt
py -3 aes_enc.py CBC Beispiel_1_lang_klar.txt key_0.txt out_enc_CBC.txt iv_0.txt
py -3 aes_enc.py OFB Beispiel_1_lang_klar.txt key_0.txt out_enc_OFB.txt iv_0.txt
py -3 aes_enc.py CTR Beispiel_1_lang_klar.txt key_0.txt out_enc_CTR.txt
```
Decryption in all modi (yields original text)
```
py -3 aes_dec.py ECB out_enc_ECB.txt key_0.txt out_dec_ECB.txt
py -3 aes_dec.py CBC out_enc_CBC.txt key_0.txt out_dec_CBC.txt iv_0.txt
py -3 aes_dec.py OFB out_enc_OFB.txt key_0.txt out_dec_OFB.txt iv_0.txt
py -3 aes_dec.py CTR out_enc_CTR.txt key_0.txt out_dec_CTR.txt
```



## 04 Lin Ana

**Files:**

`SPN.py` …  functions for SPN encryption; SPN for one block, longer texts encrypted like ECB modus

`SPN_x.py` …  script for SPN encryption: 
`SPN_x.py [input_txt] [key_txt] [output_txt]`

`subkey.py` …  functions to generate clear-crypto-pairs and to find most likely subkey for pairs

`subkey_x.py` …  script for searching most likely subkey: 
`subkey_x.py [cleartexts.txt] [cryptotexts.txt]`

`gen_pairs_x.py` …  script to generate n clear-crypto-pairs with a random key: 
`gen_pairs_x.py [clear_txt] [crypto_txt] [(int) number of pairs]`

`number_of_pairs_x.py` …  Small empirical analysis of number of pairs needed to produce the right subkey
`number_of_pairs_x.py`

`approx_quality.py` …  functions to calculate the quality of an approximation, -1 if approx. is not valid (all S-Boxes inactive)

`approx_quality_x.py` …  script to calculate the quality of an approximation: 
`approx_quality_x.py [S-Box] [approximation]`

**Description:**

The scripts that are meant to be executed from the command line (with input arguments) are marked with an “_x” suffix. The other files contain the functions used.

The SPN encryption is done using the SPN from the lecture slides. For longer texts encryption is done block by block, like ECB modus.
In subkey.py first there are some functions to generate cleartext – cryptotext – pairs. The main function is the function “subkey”, which finds the most likely subkey for the pairs given. In addition some analysis is done on how many pairs are needed to find the correct subkey. For more than 8000 pairs the right subkey is usually found, for ca. 4000 or even ca. 2000 pairs sometimes the right subkey is found, but it is not very likely. In subkey_x.py the most likely subkey for provided pairs is returned.
The gen_pairs_x.py script generates the desired number of pairs using a random key.

The number_of_pairs_x.py script provides a small empirical analysis of how many pairs are necessary to find the right subkey. The pairs are generated at random and with a random key, so results will differ for every program execution depending on the current random choice of cleartext strings and key.

In approx_quality.py functions to calculate the quality of a given approximation are implemented. The last few lines contain a comparison of the result from the lecture to the result of the program, so executing this file might be helpful. In the script approx_quality_x.py the quality of an approximation is returned for a given S-Box and its approximation.

**Example Commands:**

(Using input_1.txt, key_1.txt, Beispiel_SBox.txt Beispiel_Approximation.txt, approx_all_inactive.txt)
SPN encryption
```
py -3 SPN_x.py input_1.txt key_1.txt output_1.txt
```
Generate n = 8000 pairs and print key
```
py -3 gen_pairs_x.py clear_8000.txt crypto_8000.txt 8000
```
Find most likely subkey (if wrong key, regenerate the pairs, because for 8000 pairs there is still a small but significant likelihood, that the subkey might be wrong)
```
py -3 subkey_x.py clear_8000.txt crypto_8000.txt
```
Small empirical analysis of number of pairs needed to produce the right subkey

```
py -3 number_of_pairs_x.py
```
Quality of the approximation
```
py -3 approx_quality_x.py Beispiel_SBox.txt Beispiel_Approximation.txt
```
For invalid approximation, all S-Boxes inactive
```
py -3 approx_quality_x.py Beispiel_SBox.txt approx_all_inactive.txt
```
Additional Information on approximation quality
```
py -3 approx_quality.py
```



## 05 RSA and Diffie-Hellman

**Files:**

`eEA.py` …  function for extended Euclidean algorithm

`squa_and_mult.py` …  function for square and multiply algorithm

`find_prim.py` …  functions for the Miller-Rabin prime number test and to find (large) prime numbers

`RSA_x.py` …  script for RSA: 
`RSA_x.py [input_txt] [key_txt] [output_txt]`

`RSA_key.py` …  function for RSA key generation

`RSA_key_x.py` …  script for RSA key generation: 
`RSA_key_x.py [length] [Output private] [Output public] [primes used]`

`DH.py` …  functions that simulate a DH key exchange

`DH_x.py` …  script that performs simulated DH key exchange, output as standard output: 
`DH_x.py [bitlength]`

**Description:**

The scripts that are meant to be executed from the command line (with input arguments) are marked with an “_x” suffix. The other files contain the functions used.

The asymmetric cryptography systems RSA and Diffie-Hellman key exchange are grouped into one directory, because both use the same algorithm “Square and Multiply” to multiply large numbers with a modulo, and both use the “Miller-Rabin prime number test” to find large prime numbers. While both RSA and DH need access to the files with these algorithms, they are otherwise independent of each other.

The implementation of the extended Euclidean algorithm “Square and Multiply” and the calculation of large prime numbers are done according to the pseudocode from the lecture. For the verification of a prime number the randomized Miller-Rabin test is performed 29 times. This results in an error probability of e^(-20), which is usually acknowledged as "secure".

RSA and RSA key generation can be used as shown in the example commands below.

The Diffie-Hellman key exchange is simulated. The results are given as standard output.
Important: bitlength should not be too large, as that results in very long runtimes; up to 1000 bits works fine, up to 2000 bits is still ok, above that runtimes tend to get too long.

**Example Commands:**

(Using ExampleText.txt ExampleKey.txt ExampleEncrypted.txt ExampleKeyDecrypt.txt)
RSA encryption
```
py -3 RSA_x.py ExampleText.txt ExampleKey.txt out_RSA_encrypted.txt
```
RSA decryption
```
py -3 RSA_x.py ExampleEncrypted.txt ExampleKeyDecrypt.txt out_RSA_decrypted.txt
```
RSA key generation
```
py -3 RSA_key_x.py 500 out_RSA_key_privat.txt out_RSA_key_public.txt out_RSA_key_prims.txt
```
DH
```
py -3 DH_x.py 200
```



## 06 SHA-3

**Files:**

`SHA3.py` …  functions for SHA-3 hashing

`SHA3_x.py` …  script to find the hash value of a given text (hex string, can be formatted with whitespace, linebreaks): 
`SHA3_x.py [input_txt] [output_txt]`

**Description:**

The script that is meant to be executed from the command line (with input arguments) is marked with an “_x” suffix. The other file contains the functions used.
Numpy is necessary for this code to work.

Implementation of SHA-3-224. The hash value is written into the file specified by the path “output_txt”. If it does not exist, it is created.

The round constants and the rotations are hardwired as constants into the program, they are not read from the respective txt files every time.

**Example Commands:**

(using input_SHA_3_1.txt and input_SHA_3_2.txt which differ only in the last character)
```
py -3 SHA3_x.py input_SHA_3_1.txt out_SHA_3_1.txt
py -3 SHA3_x.py input_SHA_3_2.txt out_SHA_3_2.txt
```
