class kuitti:

    def __init__(self, ostaja, loppusumma):
        self.ostaja = ostaja
        self.tuotteet = []
        self.loppusumma = loppusumma

    def tulostaKuitti(self):
        print("Kuitti\n")

        print("Ostaja: " +self.ostaja+ "\n")

        for tuote in self.tuotteet:
            print(tuote)

        print("Loppusumma: " +str(self.loppusumma)+ "€")

    def lisaaOstos(self, ostos):
        self.tuotteet.append(ostos)

