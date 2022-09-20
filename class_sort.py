class Fruit():
    def __init__(self, name, price):
        self.name = name
        self.price = price


    def sortit(self):
        return self.price


L = [Fruit("Ciliege", 10), Fruit("Mela", 5), Fruit("Pera", 20), Fruit("Bananazza",100), Fruit("La Mazza Dura", 1)]





for f in sorted(L, key=Fruit.sortit):
    print(f.price, f.name,)


for f in sorted(L,  key=lambda x: x.price, reverse=True):
    print( f.name, f.price )
