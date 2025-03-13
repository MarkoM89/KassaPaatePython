
from Tuote import *

import mariadb
import sys

from datetime import datetime

toiminto = int(1)
maksukortit = []
kuitit = []
ostetutTuotteet = []



try:
    conn = mariadb.connect(
        user="tietokannan kayttaja",
        password="tietokannan salasana",
        host="ip-osoite tietokannalle",
        port="tietokannan portti",
        database="tietokannan nimi"

    )
except mariadb.Error as e:
    print(f"Error connecting to MariaDB Platform: {e}")
    sys.exit(1)


cur = conn.cursor()
'''
Päätoiminto 1: Osta tuote 

Päätoiminto 2: Muokkaa ostotapahtumaa 

Päätoiminto 3: Poistu ohjelmasta
'''

while toiminto != 3:
    toiminto = int(input("\nPäätoiminto 1: Ostotapahtuma\n"
                    + "Päätoiminto 2: Muokkaa ostotapahtumaa\n"
        			+ "Päätoiminto 3: Poistu ohjelmasta\n"))

    if toiminto == 1:
        print("Päätoiminto 1: Ostotapahtuma")

        syottoTuoteNimi = " "
        loppusumma = 0.0
        
        
        while syottoTuoteNimi != "":
            for tuote in ostetutTuotteet:
                tuote.tulostaTuote()

            print("Yhtensä: "+str(loppusumma)+ "€")

            tuoteLoydetty = False
            
            syottoTuoteNimi = input("Mitä tuotetta ostetaan? ")
            cur.execute(
            "SELECT tuotetunniste, tuotenimi, yksikköhinta FROM tuote WHERE tuotenimi=?", 
            (syottoTuoteNimi,))


            for (tuotetunniste, tuoteNimi, yksikköhinta) in cur:
                if tuoteNimi == syottoTuoteNimi:
                    tuoteMaara = int(input("Paljonko laitetaan: "))
                    ostetutTuotteet.append(Tuote(tuotetunniste, tuoteNimi, yksikköhinta, tuoteMaara))
                    loppusumma += (float(yksikköhinta)*tuoteMaara)
                    tuoteLoydetty = True

            if tuoteLoydetty == False and syottoTuoteNimi != "":
                    print("Tuotetta ei ole valikoimassa")


        maksettavana = loppusumma

        while maksettavana > 0:

            print("Maksettavana " +str(maksettavana)+ "€")
            maksutapa = int(input("Valitse maksutapa, \n1. Kortilla maksu\n2. käteisellä maksu\n"))

            if maksutapa == 1:

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

                
                if ostajaLoytyi == True:

                    cur.execute(  
                    "UPDATE pankki SET saldo=? WHERE nimi=?",
                    ((float(haettusaldo) - maksettavana), ostaja))
                    maksettavana = 0

            if maksutapa == 2:

                kateinen = float(input("Käteinen: "))
                maksettavana -= kateinen
            

        cur.execute(  
            "INSERT INTO kuitti (kokonaishinta) VALUES (?)",
            (loppusumma,))
            
        cur.execute("SELECT kuittitunnus FROM kuitti ORDER BY kuittitunnus DESC LIMIT 1")
        kuittitunnus = cur.fetchone()
            
        for ostos in ostetutTuotteet:
             cur.execute(  
             "INSERT INTO ostettu_tuote (kuittitunnus, tuotetunnus, tuotemäärä) values (?, ?, ?)",
             (kuittitunnus[0], ostos.haeTuotetunniste(), ostos.haeOstomaara()))

        conn.commit()


        print("\n\nKuitti\n")

        for tuote in ostetutTuotteet:
            tuote.tulostaTuote()

        print("\nLoppusumma: " +str(loppusumma)+ "€")


        ostetutTuotteet.clear()
        loppusumma = 0



        
    elif toiminto == 2:
        print("Ostotapahtuman muokkaus")



    elif toiminto == 3:
        print("Ohjelma sulkeutuu")
    


    else:
        print("Valikko toimii luvuilla 1-3")