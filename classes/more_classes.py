class Bike():
    def __init__(self, color=str, price=float):
        self.color = color
        self.price = price

    def __str__(self):
        return self.color, self.price


testOne = Bike("blue", 89.99)
testTwo = Bike("purple", 25.0)


class AppleBasket():
    def __init__(self, apple_color=str, apple_quantity=int):
        self.apple_color = apple_color
        self.apple_quantity = apple_quantity

    def increase(self):
        self.apple_quantity = + self.apple_quantity + 1

    def __str__(self):
        return f"A basket of {self.apple_quantity} {self.apple_color} apples."


class BankAccount():
    def __init__(self, name=str, total=int):
        self.name = name
        self.atm = total

    def __str__(self):
        return f"Your account, {self.name}, has {self.atm} dollars."


t1 = BankAccount("Bob", 100)
print(t1)
