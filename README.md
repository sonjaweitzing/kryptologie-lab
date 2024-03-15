# Kryptologie LAB 2023/24 Sonja Weitzing

README


## Overview

This is a collection of programs for the cryptology LAB course 2023/24. All programs are written in python. For some programs (vigenere and SHA-3) the “numpy” package is required. Hence installing “numpy” might be necessary, before the programs can be executed (for example using "pip install numpy").



## 01 Additive Chiffre

**Files:**

<span style="color:blue;">ac.py</span>  ...  procedure for encryption or decryption with given key

<span style="color:blue;">find_key.py</span>  ...  finds the key of an encrypted german text using frequency analysis

<span style="color:blue;">ac_enc.py</span>  ...  script for encryption:
<span style="color:blue;">ac_enc.py [input_txt] [key] [output_txt]</span>

<span style="color:blue;">ac_dec.py</span> ...  script for decription (with known key):
<span style="color:blue;">ac_dec.py [input_txt] [key] [output_txt]</span>

<span style="color:blue;">ac_dec_find_key.py</span> ... script for decription (with an unknown key):
<span style="color:blue;">ac_dec_find_key.py [input_txt] [output_txt]</span>

**Description:**

The procedure “ac” can be used to encrypt or decryption texts in capital letters with a key. The input and output files are given as .txt files, and a function parameter specifies, whether encryption (ADDING the key) or decryption (SUBTRACTING the key) is done. The function “find_key” finds the key of a given ciphertext using frequency analysis. From this, the three scripts ac_enc.py, ac_dec.py and ac_dec_find_key.py are created to encrypt or decrypt (with known or unknown key) a text provided. These three scripts can be called using the command line (eg. Commands below).

**Example Commands:**

(Using Klartext_1.txt and Kryptotext_1_Key_7.txt)
```
py -3 ac_enc.py Klartext_1.txt 7 ac_enc_output.txt
py -3 ac_dec.py Kryptotext_1_Key_7.txt 7 ac_dec_output.txt
py -3 ac_dec_find_key.py Kryptotext_1_Key_7.txt ac_dec_key_output.txt
```


## 02 Vigenere

**Files:**

<span style="color:blue;">vig.py</span>  …  procedure to encrypt or decrypt messages using the vigenere chiffre with a key provided

<span style="color:blue;">find_key.py</span>  …  functions to determine the key length and the key (string) of a vigenere encrypted text

<span style="color:blue;">vig_enc.py</span> …  script for encryption:
<span style="color:blue;">vig_enc.py input.txt key output.txt</span>

<span style="color:blue;">vig_dec.py</span> …  script for decription (with an unknown key):
<span style="color:blue;">vig_dec.py input.txt output.txt</span>

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

<span style="color:blue;">key_gen.py</span> …  functions to generate 11 round keys from a single 128 bit key.

<span style="color:blue;">aes_block.py</span> …  functions realizing the encryption of one 128 bit block, when the 11 round keys are provided

<span style="color:blue;">modi.py</span> …  functions realising four operation modi for block chiffres, ECB,CBC, OFB and CTR

<span style="color:blue;">aes.py</span> …  function combining key generation, block encryption and operation modi into an AES encryption for texts.

<span style="color:blue;">aes_enc.py</span> …  script for encryption: 
<span style="color:blue;">aes_enc.py [modus] [Input_txt] [key_txt] [Output_txt] ([IV] if required (for CBC, OFB))</span>

<span style="color:blue;">aes_dec.py</span> …  script for decryption:
<span style="color:blue;">aes_dec.py [modus] [Input_txt] [key_txt] [Output_txt] ([IV] if required (for CBC, OFB))</span>


**Description:**

The AES module contains programs for the operation modi, the aes block encryption (128 bit block length) and the aes key generation.

The key generation generated 11 round keys from a single 128 bit key provided.

The AES block encryption realizes the encryption or decryption function of AES.

Both the key generation and the AES block encryption mainly works on integers, using bitwise operations. The sbox and invers sbox must be provided as txt files. They are loaded in the program using a helper function and then treated an constants.

The modi take formatted hex strings as an input and produce them as output (only hex numbers, no whitespaces etc.). The key for the modi must be provided in whatever form the used encryption function needs it. In case of AES as a list of 11 round keys for the aes_block_enc or aes_block_dec function. The initialization vector is passed as an Integer.

In the file aes.py the aes function combines the key generation, block encryption and operation modi into an AES encryption or decryption for texts. To make in- and output using .txt files with hexadecimal numbers possible, helper functions for conversion are used in the final AES implementation. The input and output of texts, the 128 bit key and if necessary an initialization vector is done using .txt files containing hex strings. The files can contain whitespaces etc. for better readability.

To call the aes function from the command line the two scripts aes_enc.py and aes_dec.py were created. They can be used as illustrated in the example commands below.

When using CBC or OFB an initialization vector must be given as an argument, otherwise an error will occur. Providing an obsolete IV for ECB or CTR mode will not cause an error, the IV simply has no effect, as it is not used for these modi.

**Example Commands:**

(Using Beispiel_1_lang_klar.txt which is simply a combination of the example blocks Beispiel_1_Klartext.txt and Beispiel_2_Klartext.txt; key_0.txt which is the first round key from Beispiel_key.txt; iv_0.txt which is the zero vector for initialization. iv.txt can be used to try a different initialization vector))
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

<span style="color:blue;">SPN.py</span> …  functions for SPN encryption; SPN for one block, longer texts encrypted like ECB modus

<span style="color:blue;">SPN_x.py</span> …  script for SPN encryption: 
<span style="color:blue;">SPN_x.py [input_txt] [key_txt] [output_txt]</span>

<span style="color:blue;">subkey.py</span> …  functions to generate clear-crypto-pairs and to find most likely subkey for pairs

<span style="color:blue;">subkey_x.py</span> …  script for searching most likely subkey: 
<span style="color:blue;">subkey_x.py [cleartexts.txt] [cryptotexts.txt]</span>

<span style="color:blue;">gen_pairs_x.py</span> …  script to generate n clear-crypto-pairs with a random key: 
<span style="color:blue;">gen_pairs_x.py [clear_txt] [crypto_txt] [(int) number of pairs]</span>

<span style="color:blue;">number_of_pairs_x.py</span> …  Small empiric analysis of number of pairs needed to produce the right subkey
<span style="color:blue;">number_of_pairs_x.py</span>

<span style="color:blue;">approx_quality.py</span> …  functions to calculate the quality of an approximation, -1 if approx. is not valid (all S-Boxes inactive)

<span style="color:blue;">approx._quality_x.py</span> …  script to calculate the quality of an approximation: 
<span style="color:blue;">approx._quality.py [S-Box] [approximation]</span>

**Description:**

The scripts that are meant to be executed from the command line (with input arguments) are marked with an “_x” suffix. The other files contain the functions used.

The SPN encryption is done using the SPN from the lecture slides. For longer texts encryption is done block by block, like ECB modus.
In subkey.py first there are some functions to generate cleartext – cryptotext – pairs. The main function is the function “subkey”, which finds the most likely subkey for the pairs given. In addition some analysis is done on how many pairs are needed to find the correct subkey. For more than 8000 pairs the right subkey is usually found, for ca. 4000 or even ca. 2000 pairs sometimes the right subkey is found, but it is not very likely. In subkey_x.py the most likely subkey for provided pairs is returned.
The gen_pairs_x.py script generates the desired number of pairs using a random key.

The number_of_pairs_x.py script provides a small empiric analysis of how many pairs are necessary to find the right subkey. The pairs are generated at random and with a random key, so results will differ for every program execution depending on the current random choice of cleartexts strings an key.

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
Small empiric analysis of number of pairs needed to produce the right subkey

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

<span style="color:blue;">eEA.py</span> …  function for extended Euclidian algorithm

<span style="color:blue;">squa_and_mult.py</span> …  function for square and multiply algorithm

<span style="color:blue;">find_prim.py</span> …  functions for the Miller-Rabin prim number test and to find (large) prim numbers

<span style="color:blue;">RSA_x.py</span> …  script for RSA: 
<span style="color:blue;">RSA.py [input_txt][key_txt][output_txt]</span>

<span style="color:blue;">RSA_key.py</span> …  function for RSA key generation

<span style="color:blue;">RSA_key_x.py</span> …  script for RSA key generation: 
<span style="color:blue;">RSA_key.py [length] [Output private] [Output public] [prims used]</span>

<span style="color:blue;">DH.py</span> …  functions that simulate a DH key exchange

<span style="color:blue;">DH_x.py</span> …  script that performs simulated DH key exchange, output as standard output: 
<span style="color:blue;">DH_X.py [bitlength] </span>

**Description:**

The scripts that are meant to be executed from the command line (with input arguments) are marked with an “_x” suffix. The other files contain the functions used.

The asymmetric cryptography systems RSA and Diffie-Hellman key exchange are grouped into one directory, because both use the same algorithm “Square and Multiply” to multiply large numbers with a modulo, and both use the “Miller-Rabin Prim number test” to find large prime numbers. While both RSA and DH need access to the files with these algorithms, they are otherwise independent of each other.

The implementation of the extended Euclidian algorithm “Square and Multiply” and the calculation of large prim numbers are done according to the pseudocode from the lecture. For the verification of a prim number the randomized Miller-Rabin test is performed 29 times. This results in an error probability of e^(-20), which is usually acknowledged as "secure".

RSA and RSA key generation can be used as shown in the example commands below.

The Diffie-Hellman key exchange is simulated. The results are given as standard output.
Important: bitlength should not be too large, as that results in very long runtimes; up to 1000 bits works fine, up to 2000 bits is still ok, above that runtimes tend to get to long.

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

<span style="color:blue;">SHA3.py</span> …  functions for SHA-3 hashing

<span style="color:blue;">SHA3_x.py</span> …  script to find a hashvalue of a given text (hex string, can be formatted with whitespace, linebreaks): 
<span style="color:blue;">SHA3_x.py [input_txt] [output_txt]</span>

**Description:**

The script that is meant to be executed from the command line (with input arguments) is marked with an “_x” suffix. The other file contains the functions used.
Numpy is necessary for this code to work.

Implementation of SHA-3-224. The hash value is written into the file specified by the path “output_txt”. If it does not exist, it is created.

The round constants and the rotations are hardwired as constants into the program, they are not read from the respective txt files every time.

**Example Commands:**

(using input_SHA_3_1.txt and input_SHA_3_2.txt which differ only in the last character)
```
py -3 SHA_x.py input_SHA_3_1.txt out_SHA_3_1.txt
py -3 SHA_x.py input_SHA_3_2.txt out_SHA_3_2.txt
```



The round constants and the rotations are hardwired as constants into the program, they are not read from the respective txt files every time.
Example Commands:
(using input_SHA_3_1.txt and input_SHA_3_2.txt which differ only in the last character)
py -3 SHA_x.py input_SHA_3_1.txt out_SHA_3_1.txt
py -3 SHA_x.py input_SHA_3_2.txt out_SHA_3_2.txt
