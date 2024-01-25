class MaksuKortti:


    def __init__(self, omistaja, saldo):
        self.Omistaja = omistaja
        self.saldo = saldo

    def palautaNimi(self):
        return self.Omistaja

    def tulostaSaldo(self):
        print(self.Omistaja+ ": Kortilla on rahaa " +str(self.saldo)+ "€")

    def lataaRahaa(self, rahamaara):
        if rahamaara > 0:
            self.saldo += rahamaara
        else:
            print("Rahamäärän täytyy olla 0€ suurempi")

    def veloita(self, kokonaishinta):
        if self.saldo >= kokonaishinta:
            self.saldo -= kokonaishinta
        else:
            print("Kortilla ei ole tarpeeksi katetta")
