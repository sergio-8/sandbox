class punto():
    def __init__(self, x,y):
        self.x = x
        self.y = y

    def get_x(self):
        return self.x

    def get_y(self):
        return self.y

    def __str__(self):
        return 'Punto x={} y={}'.format(self.x, self.y)

    def midpoint(self, punto2):
        m1=(self.x +punto2.x)/2
        m2=(self.y +punto2.y)/2
        return print ('Puntodimezzo x={}, y={}'.format(m1, m2))

primo=punto(7,10)
secondo= punto(19,28)

primo.midpoint(secondo)



