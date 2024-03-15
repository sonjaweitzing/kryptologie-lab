def squa_and_mult(x, m, n):
    """
    Calculate x^m mod n using "Square and Multiply" // Quadrieren und Multiplizieren

    :param x: integer, base
    :param m: integer, exponent
    :param n: integer, modul
    :return: x^m mod n
    """
    # Input: x...int, m...int, n...int
    # returns integer y = x^m mod n
    y = 1
    m_bin = format(m, 'b')
    r = len(m_bin)
    for i in range(r-1, -1, -1): #  Indices other way round compared to pseudocode, m = b0*2^r+b1*2^r-1+...+br
        if m_bin[i] == '1':
            y = (y*x) % n
        x = (x*x) % n
    return y

# Test
if __name__ == "__main__":
    a = squa_and_mult(10, 30, 17) # 8
    b1 = squa_and_mult(200, 5, 391) # 98
    b2 = squa_and_mult(98, 141, 391) # 200
    c = squa_and_mult(441, 3, 493) # 390
    d = squa_and_mult(7, 25, 11) # 10
    print("\n", a, "\n", b1, "\n", b2, "\n", c, "\n", d)

    # Test very large numbers
    l = squa_and_mult(2**1543, (2**1998)-3, (2**587)-19)
    print("\nLarge Number: ", l)

# Seems to work just fine :)
