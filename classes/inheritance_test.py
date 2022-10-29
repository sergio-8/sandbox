
today=2022

class Persona:

    def __init__(self, name, yob):

        self.name = name
        self.yob = yob

    def get_age(self):

        return  today- self.yob

    def __str__(self):
        return "il  nome e' {}, e l'eta' e' {} anni, giovane ehhh...".format(self.name, self.get_age())



class Studente :

    def __init__(self, name, yob):

        self.name = name
        self.yob = yob
        self.knowledge = 0

    def get_age(self):

        return  today- self.yob

    def __str__(self):
        return "il  nome e' {}, e l'eta' e' {} anni, giovane ehhh...".format(self.name, self.get_age())



p= Persona("ceppo", 1901)
print(p)