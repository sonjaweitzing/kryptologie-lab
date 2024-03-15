def eEA(r_0, r_1):
    """
    extended euclidian algorithm

    :param r_0: integer, first number
    :param r_1: integer, second number
    :return: greatest common divisor GCD of r_0 and r_1
    """
    # erweiterter Euklidischer Algorithmus
    # Berechnung von ggT(a, b)
    #Initial Deklaration - a = r_0, b = r_1
    k = 0
    swap_coeff = 0
    if (r_1 > r_0):
        r_help = r_1
        r_1 = r_0
        r_0 = r_help
        swap_coeff = 1
    s_0 = 1
    s_1 = 0
    t_0 = 0
    t_1 = 1
    #Alg
    while(r_1 != 0):
        k = k+1
        q_k = r_0 // r_1  # // is Operator for Integerdivision
        r_2 = r_0 - q_k * r_1
        s_2 = s_0 - q_k * s_1
        t_2 = t_0 - q_k * t_1
        # nächster Schritt - umbenennen
        r_0 = r_1
        s_0 = s_1
        t_0 = t_1
        r_1 = r_2
        s_1 = s_2
        t_1 = t_2
    if swap_coeff:
        return r_0, t_0, s_0
    else:
        return r_0, s_0, t_0
    # the swap_coeff flag and condition with swapped order of output args ensures that first coeff
    # yielded by alg always belongs to first number entered


# Test
if __name__ == "__main__":
    r,s,t = eEA(693, 147)  # ggT = 21; s,t = 3, -14
    print("\nr: ", r, "\ns: ", s, "\nt: ", t, )
    r, s, t = eEA(32, 24)
    print("\nr: ", r, "\ns: ", s, "\nt: ", t, )
# works :)

