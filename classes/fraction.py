
class Fraction:

    '''class fraction test'''

    def __init__(self, top, bottom  ):
        ''' constructor definition'''

        self.num = top
        self.den = bottom

    def show (self):
        print(f"{self.num}/{self.den}")


    def __str__(self):

        return f'{self.num}/{self.den}'

    def __add__(self, other):
        new_num = self.num * other.den + \
            self.den * other.num
        new_den = self.den * other.den
        common = Fraction.gcd(new_num, new_den)

        if new_num != new_den:
            return Fraction (new_num//common, new_den//common)
        else:
            return new_num//new_den


    def gcd (m, n):
        while m % n != 0:
            m , n = n , m % n
        return n








