class Cereal:
    """ Point class for representing and manipulating x,y coordinates. """

    def __init__(self, name, brand, fiber):

        self.name = name
        self.brand = brand
        self.fiber=fiber


    def __str__(self):
        return "{} cereal is produced by {} and has {} grams of fiber in every serving!".format(self.name, self.brand, self.fiber)

c1 = Cereal("Corn Flakes","Kellogg's", 2)
c2 = Cereal("Honey Nut Cheerios","General Mills", 3)
print(c1)
print (c2)
