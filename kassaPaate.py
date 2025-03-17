
from Tuote import *

import mariadb
import sys


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

Päätoiminto 2: Poistu ohjelmasta

Puuttuu takaisinmaksu käteisestä

'''

while toiminto != 2:
    toiminto = int(input("\nPäätoiminto 1: Ostotapahtuma\n"
        			+ "Päätoiminto 2: Poistu ohjelmasta\n"))

    if toiminto == 1:
        print("Päätoiminto 1: Ostotapahtuma")

        syottoTuoteNimi = int(-1)
        loppusumma = 0.0
        
        
        while syottoTuoteNimi != 0:
            for tuote in ostetutTuotteet:
                tuote.tulostaTuote()

            print("Yhteensä: "+str(loppusumma)+ "€")

            tuoteLoydetty = False
            
            syottoTuoteNimi = int(input("Mitä tuotetta ostetaan? "))
            cur.execute(
            "SELECT tuotetunniste, tuotenimi, yksikköhinta FROM tuote WHERE tuotetunniste=?", 
            (syottoTuoteNimi,))


            for (tuotetunniste, tuoteNimi, yksikköhinta) in cur:
                print(str(tuoteNimi)+" "+ str(yksikköhinta))
                if tuotetunniste == syottoTuoteNimi:
                    tuoteMaara = int(input("Paljonko laitetaan: "))
                    ostetutTuotteet.append(Tuote(tuotetunniste, tuoteNimi, yksikköhinta, tuoteMaara))
                    loppusumma += (float(yksikköhinta)*tuoteMaara)
                    tuoteLoydetty = True

            if tuoteLoydetty == False and syottoTuoteNimi != 0:
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
        print("Ohjelma sulkeutuu")

    elif toiminto == 5:
        print("Korttien tiedot")
        cur.execute("select * from pankki")

        for (tunniste, nimi, saldo) in cur:
            print(str(tunniste)+ " " +nimi+ " " +str(saldo)+ "€")

        print("\n\nKuitit\n-----------------------------------------\n")

        cur.execute("select * from kuitti")

        for (kuittitunnus, osto_aika, kokonaishinta) in cur:
            print(str(kuittitunnus)+ " " +str(osto_aika)+ " " +str(kokonaishinta)+ "€")


    else:
        print("Valikko toimii luvuilla 1-2")