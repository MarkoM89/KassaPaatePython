from MaksuKortti import *
from Tuote import *
from kuitti import *

import mariadb
import sys

toiminto = int(1)
maksukortit = []
tuotteet = []
kuitit = []
ostetutTuotteet = []



try:
    conn = mariadb.connect(
        user="root",
        password="T13t0k4!?t4",
        host="127.0.0.1",
        port=3306,
        database="kokeilutietokanta"

    )
except mariadb.Error as e:
    print(f"Error connecting to MariaDB Platform: {e}")
    sys.exit(1)

# Get Cursor
cur = conn.cursor()

cur.execute("select * from pankki")

for (tunniste, nimi, saldo) in cur:
    print(f"tunniste: {tunniste}, nimi: {nimi}, saldo: {saldo}")
    maksukortit.append(MaksuKortti(nimi, float(saldo)))


print("\n\n\n")

cur.execute("select * from tuote")

for (tuotetunnste, tuoteNimi, yksikköhinta) in cur:
    print(f"tuotetunnste: {tuotetunnste}, tuoteNimi: {tuoteNimi}, yksikköhinta: {yksikköhinta}")
    tuotteet.append(Tuote(tuoteNimi, float(yksikköhinta)))


print("\n\n\n")

'''cur.execute(
    "SELECT nimi,saldo FROM pankki WHERE tunniste=?", 
    (some_name,))

Päätoiminto 1: Osta tuote 

Päätoiminto 2: Poistu ohjelmasta
'''

while toiminto != 2:
    toiminto = int(input("\nPäätoiminto 1: Ostotapahtuma\n"
        			+ "Päätoiminto 2: Poistu ohjelmasta\n"))

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
                            ostetutTuotteet.append(tuoteNimi+ " " +str(tuoteMaara)+ "kpl")
                            loppusumma += (tuote.haeHinta()*tuoteMaara)

                ostaja.veloita(loppusumma)
                kuitit.append(kuitti(nimi, loppusumma))

                for ostos in ostetutTuotteet:
                    kuitit[-1].lisaaOstos(ostos)

                kuitit[-1].tulostaKuitti()
                ostetutTuotteet.clear()
                loppusumma = 0
        
    elif toiminto == 2:
        print("Ohjelma sulkeutuu")

    elif toiminto == 5:
        print("Korttien tiedot")
        for tieto in maksukortit:
            tieto.tulostaSaldo()

        print("\n\nKuitit\n-----------------------------------------\n")
        for kuitti in kuitit:
            kuitti.tulostaKuitti()

    else:
        print("Valikko toimii luvuilla 1-2")