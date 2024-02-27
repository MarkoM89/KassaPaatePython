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


cur = conn.cursor()
'''
Päätoiminto 1: Osta tuote 

Päätoiminto 2: Poistu ohjelmasta
'''

while toiminto != 2:
    toiminto = int(input("\nPäätoiminto 1: Ostotapahtuma\n"
        			+ "Päätoiminto 2: Poistu ohjelmasta\n"))

    if toiminto == 1:
        print("Päätoiminto 1: Ostotapahtuma")

        syottoTuoteNimi = " "
        loppusumma = 0.0
        
        
        while syottoTuoteNimi != "":
            for tuote in ostetutTuotteet:
                print(tuote)

            tuoteLoydetty = False
            
            syottoTuoteNimi = input("Mitä tuotetta ostetaan? ")
            cur.execute(
            "SELECT tuotetunniste, tuotenimi, yksikköhinta FROM tuote WHERE tuotenimi=?", 
            (syottoTuoteNimi,))


            for (tuotetunniste, tuoteNimi, yksikköhinta) in cur:
                if tuoteNimi == syottoTuoteNimi:
                    tuoteMaara = int(input("Paljonko laitetaan: "))
                    ostetutTuotteet.append(tuoteNimi+ " " +str(tuoteMaara)+ "kpl")
                    loppusumma += (float(yksikköhinta)*tuoteMaara)
                    print(loppusumma)
                    tuoteLoydetty = True

            if tuoteLoydetty == False and syottoTuoteNimi != "":
                    print("Tuotetta ei ole valikoimassa")


        ostaja = input("Kuka ostaa? ")
        haettusaldo = 0.0
        ostajaLoytyi = False

        cur.execute(
        "SELECT tunniste, nimi, saldo FROM pankki WHERE nimi=?", 
        (ostaja,))


        for (tunniste, nimi, saldo) in cur:
            if nimi == ostaja:

                ostajaLoytyi = True
                haettusaldo = saldo

                kuitit.append(kuitti(nimi, loppusumma))

                for ostos in ostetutTuotteet:
                    kuitit[-1].lisaaOstos(ostos)

                kuitit[-1].tulostaKuitti()

        if ostajaLoytyi == True:

            cur.execute(  
            "UPDATE pankki SET saldo=? WHERE nimi=?",
            (float(haettusaldo) - loppusumma, ostaja))
            conn.commit()


        ostetutTuotteet.clear()
        loppusumma = 0
        
    elif toiminto == 2:
        print("Ohjelma sulkeutuu")

    elif toiminto == 5:
        print("Korttien tiedot")
        cur.execute("select * from pankki")

        for (tunniste, nimi, saldo) in cur:
            print(str(tunniste)+ " " +nimi+ " " +str(saldo)+ "€")

        print("\n\nKuitit\n-----------------------------------------\n")
        for kuitti in kuitit:
            kuitti.tulostaKuitti()

    else:
        print("Valikko toimii luvuilla 1-2")