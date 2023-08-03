class Tuote:

    def __init__(self, nimi, hinta):
        self.nimi = nimi
        self.hinta = hinta

    def haeNimi(self):
        return self.nimi

    def haeHinta(self):
        return self.hinta
    
    def tulostaTuote(self):
        print(self.nimi+ ", hinta " +str(self.hinta)+ "€")