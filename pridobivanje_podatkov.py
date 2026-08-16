import requests
import time

from bs4 import BeautifulSoup, Comment
import re

import pomozni_podatki as POM


# tričrkovne kode ekip pobere iz razširjene tabele (v HTML datoteki je zakomentirana), to uporabi tudi za id
def pridobi_kodo_ekip(soup):
    slovar = {}

    tabela = soup.find(
        string = lambda text: isinstance(text, Comment) and "div_expanded_standings" in text
            )

    tabela_soup = BeautifulSoup(tabela, "html.parser")
    ekipe = tabela_soup.find_all("a")

    for ekipa in ekipe:
        kratica = re.search(r"/teams/([A-Z]+)/\d+.html", ekipa["href"]).group(1)
        ime = ekipa.text
        slovar.update({kratica: ime})

    return slovar



# podatki o sezoni, vrne BeautifulSoup
def pridobi_podatke_sezona(leto):

    stran = requests.get(POM.SEZONA_URL(leto), headers=POM.HEADERS)

    # to je pomoje boljše odstraniti potem, niti ni treba shraniti spletne strani
    #with open(f"UVP_projektna_naloga/spletne_strani/sezona_{leto}.html", "w", encoding="ISO-8859-1") as dat:
    #    dat.write(stran.text)

    soup = BeautifulSoup(stran.text, "html.parser")

    time.sleep(5)

    return soup


def pridobi_podatke_igralec(id):
    ...

def izlusci_podatke_sezona(soup, leto):
    seznam_podatkov = []

    # tabeli po konferencah - od leta 1971 naprej - prej je samo brez E in W, na koncu je underscore
    # lahko to daš v ločeno funkcijo pa daš še default value da je "" ali pa kaj takega
    for smer in ["E", "W"]:
        tabela = soup.find("table", id = f"divs_standings_{smer}").find("tbody")
        vrstice = tabela.find_all("tr")

        for vrstica in vrstice:

            if "thead" in vrstica.get("class", []): # vrstica, v kateri piše ime divizije
                divizija = POM.PREVAJALNIK_DIVIZIJE[vrstica.find("strong").text]
                continue

            # id in ime ekipe
            ekipa = vrstica.find("a")
            id_ekipe = re.search(r"/teams/([A-Z]+)/\d+.html", ekipa["href"]).group(1)
            ime_ekipe = ekipa.text

            # konferenca
            if smer == "E":
                konferenca = "vzhodna"
            else:
                konferenca = "zahodna"


            # zmage, porazi, točke

            def podatek_vrstice(atribut):
                return vrstica.find("td", attrs = {"data-stat": atribut}).text
                
            zmage = podatek_vrstice("wins")
            porazi = podatek_vrstice("losses")
            povp_tocke = podatek_vrstice("pts_per_g") # povprečne dane točke na igro
            povp_prejeto = podatek_vrstice("opp_pts_per_g") # povprečne prejete točke na igro

            seznam_podatkov.append({
                "id": id_ekipe,
                "ime": ime_ekipe,
                "leto": leto,
                "konferenca": konferenca,
                "divizija": divizija,
                "zmage": zmage,
                "porazi": porazi,
                "povprečne dane točke": povp_tocke,
                "povprečne prejete točke": povp_prejeto
            })

    
    # tabela razširjenih statistik - zakomentirana (poglej če je za vsa leta zakomentirana)
    tabela_raz = soup.find(
            string = lambda text: isinstance(text, Comment) and "div_expanded_standings" in text
                )

    tabela_soup = BeautifulSoup(tabela_raz, "html.parser").find("tbody")
    vrstice_raz = tabela_soup.find_all("tr")

    for vrstica in vrstice_raz:
        ...
        


   


    return seznam_podatkov






# začasno
with open("UVP_projektna_naloga/spletne_strani/sezona_2026.html", "r",  encoding="ISO-8859-1") as dat:
    soup1 = BeautifulSoup(dat.read(), "html.parser")

print(izlusci_podatke_sezona(soup1, 2026))

