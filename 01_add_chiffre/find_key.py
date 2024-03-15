from collections import Counter
def find_key(input_txt):
    """
    function "find key" finds the key of a german text using frequency analysis.
    Hypothesis: Most common letter in any german text is E -> hence key = number(most common letter) - number(E)
    the counter class counts frequency of all letters (see doc below)
    looping over ctr.most_common() is a loop over all letters in ctr. The loop continues until a capital letter
    from A to Z appears, therefore the function finds the most common capital letter in the text and with this
    information returns the key.
    checking for capital letters is important, because whitespace or other characters may be present more often in text
    than cryptological relevant capital letters.
    if no most common capital letter exist, the key cannot be determined and find_key returns 0

    :param input_txt: cipher text in capital letters as .txt file
    :return: key as interger from 0 to 25 if a key is found, -1 if for the specific input file no valid key is found
    """
    with open(input_txt, 'r', encoding="utf-8") as cipher:  # only read
        ctr = Counter(cipher.read())
        for cha, count in ctr.most_common():  # cha, count as var: necessary for cha to be character
            if ord('A') <= ord(cha) <= ord('Z'):  # character is bold letter from A to Z
                key = ord(cha) - ord('E')
                return key
        # if no key found (because txt contains no capital letters etc) then no key is returned
        return -1

# Documentation on Counter

# A Counter is a dict subclass for counting hashable objects. It is a collection where elements are stored as
# dictionary keys and their counts are stored as dictionary values. Counts are allowed to be any integer value
# including zero or negative counts. The Counter class is similar to bags or multiset in other languages.
