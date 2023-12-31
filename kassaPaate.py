from MaksuKortti import *
from Tuote import *
from kuitti import *

toiminto = int(1)
maksukortit = []
maksukortit.append(MaksuKortti("Mikko", 120.60))
maksukortit.append(MaksuKortti("Tapio", 200.00))
maksukortit.append(MaksuKortti("Noora", 175.20))

tuotteet = []
tuotteet.append(Tuote("Tomaatti", 1.25))
tuotteet.append(Tuote("Omena", 0.95))

kuitit = []
ostetutTuotteet = []


'''
Päätoiminto 1: Osta tuote 

Päätoiminto 2: Maksukorttin hallinta
		Toiminto 1: Luo Maksukortti
		Toiminto 2: Lataa rahaa
		Toiminto 3: Poista maksukortti
		Toiminto 4: Tulosta korttien tiedot

Päätoiminto 3: Tuotehallinta
		Toiminto 1: Lisää tuote
		Toiminto 2: Poista tuote
		Toiminto 3: Tulosta tuotteet
		
Päätoiminto 4: Poistu ohjelmasta
'''

while toiminto != 4:
    toiminto = int(input("\nPäätoiminto 1: Ostotapahtuma\nPäätoiminto 2: Varaston hallinta\nPäätoiminto 3: Tuotehallinta\n"
        			+ "Päätoiminto 4: Poistu ohjelmasta\nPäätoiminto 5: Tulosta korttien tiedot\n"))

    if toiminto == 1:
        print("Päätoiminto 1: Ostotapahtuma")
        nimi = input("Kuka ostaa? ")
        for ostaja in maksukortit:
            if ostaja.palautaNimi() == nimi:

                tuoteNimi = " "
                loppusumma = 0.0
                while tuoteNimi != "":
                    for tuote in tuotteet:
                        tuote.tulostaTuote()
                    tuoteNimi = input("Mitä tuotetta ostetaan? ")
                    for tuote in tuotteet:
                        if tuote.haeNimi() == tuoteNimi:
                            tuoteMaara = int(input("Paljonko laitetaan: "))
                            ostaja.veloita(tuote.haeHinta(), tuoteMaara)
                            ostetutTuotteet.append(tuoteNimi+ " " +str(tuoteMaara)+ "kpl")
                            loppusumma += (tuote.haeHinta()*tuoteMaara)

                kuitit.append(kuitti(nimi, loppusumma))

                for ostos in ostetutTuotteet:
                    kuitit[-1].lisaaOstos(ostos)

                kuitit[-1].tulostaKuitti()
                ostetutTuotteet.clear()
                loppusumma = 0

    elif toiminto == 2:
        print("Päätoiminto 2: Varaston hallinta")

    elif toiminto == 3:
        while toiminto != 4:

            print("\nPäätoiminto 3: Tuotehallinta")
				
            toiminto = int(input("\nToiminto 1: Lisää tuote\nToiminto 2: Poista tuote\nToiminto 3: Tulosta tuotteet\n"
				    		+ "Toiminto 4: Poistu tuotehallinnasta\n"))
        
            if toiminto == 1:
                nimi = (input("Tuotenimi: "))
                hinta = float(input("Tuotteen yksikköhinta: "))
                tuotteet.append(Tuote(nimi, hinta))
            
            elif toiminto == 2:
                nimi = input("Tuotenimi? Tyhjä kenttä ei poista mitään: ")
                for tuote in tuotteet:
                    if tuote.haeNimi() == nimi:
                        tuotteet.remove(tuote)
                    else:
                        #Tuotetta ei löytynyt tulostuu, joka kierroksella, virhe
                        print("Tuotetta ei löytynyt")

            elif toiminto == 3:
                print("Tuotelista")
                for tuote in tuotteet:
                    tuote.tulostaTuote()
        toiminto = 0
        
    elif toiminto == 4:
        print("Ohjelma sulkeutuu")

    elif toiminto == 5:
        print("Korttien tiedot")
        for tieto in maksukortit:
            tieto.tulostaSaldo()

        print("\n\nKuitit\n-----------------------------------------\n")
        for kuitti in kuitit:
            kuitti.tulostaKuitti()

    else:
        print("Valikko toimii luvuilla 1-5")