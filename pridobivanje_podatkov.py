import requests
import time

from bs4 import BeautifulSoup
import re

import pomozni_podatki as POM


# tričrkovne kode ekip pobere iz razpredelnice o konferencah, to uporabi tudi za id
def pridobi_kodo_ekip(soup):
    ...



def podatki_sezona(leto):

    stran = requests.get(POM.SEZONA_URL(leto), headers=POM.HEADERS)

    with open(f"UVP_projektna_naloga/spletne_strani/sezona_{leto}.html", "w", encoding="ISO-8859-1") as dat:
        dat.write(stran.text)

    soup = BeautifulSoup(stran.text, "html.parser")

    time.sleep(5)



podatki_sezona(2026)
