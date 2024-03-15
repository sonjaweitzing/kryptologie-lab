from subkey import find_subkey

# script to open .txt files specified in command line args and decrypt according to aC_decrypt
try:
    print("\n----------------------------------------------------------------------------------\n"
          "Small empiric analysis of number of pairs needed to produce the right subkey\n\n")

    for count in range(1, 12):
        find_subkey( count * 1000 )

    print("Result:\n"
          "Subkey is almost always right for number of pairs greater equal 8000."
          "That corresponds likely to the theoretic result, that roughly 8000 pairs are neccessary."
          "Even for smaller numbers sometimes right subkey is found, but it is less likely."
          "Because key and pairs are generated at random, results vary depending on the specific texts and key."
          "\n----------------------------------------------------------------------------------\n")

except FileNotFoundError:
    print("Cannot find input args")