class Classy():
    def __init__(self, item=str):
        self.items = []
        self.item = item



    def addItem(self, a=str):
        self.items.append(a)

    def getClassiness(self):
        self.value = 0

        for item in self.items:
            if item == "tophat":
                self.value += 2
            if item == "bowtie":
                self.value += 4
            if item == "monocle" :
                self.value += 5
            else:
                self.value = self.value


        return self.value




# Test cases
me = Classy()

# Should be 0
print(me.getClassiness())

me.addItem("tophat")
# Should be 2
print(me.getClassiness())

me.addItem("bowtie")
me.addItem("jacket")
me.addItem("monocle")
# Should be 11
print(me.getClassiness())

me.addItem("bowtie")
# Should be 15
print(me.items)
print(me.getClassiness())