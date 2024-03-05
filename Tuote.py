class Tuote:

    def __init__(self, tuotetunniste, nimi, hinta, ostomaara):
        self.tuotetunniste = tuotetunniste
        self.nimi = nimi
        self.hinta = hinta
        self.ostomaara = ostomaara

    def haeTuotetunniste(self):
        return self.tuotetunniste

    def haeNimi(self):
        return self.nimi

    def haeHinta(self):
        return self.hinta
    
    def haeOstomaara(self):
        return self.ostomaara
    
    def tulostaTuote(self):
        print(self.nimi+ " " +str(self.hinta)+ "€")