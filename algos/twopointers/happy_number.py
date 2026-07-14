def is_happy_number(n):

    def digs_sum(num):
        d_s = sum(int(char) ** 2 for char in str(num))

        return d_s

    lento = n
    veloce = digs_sum(n)

    while veloce != 1 and lento != veloce:
        l = digs_sum(lento)
        v = digs_sum(digs_sum(veloce))
        lento = l
        veloce = v

    return veloce == 1
