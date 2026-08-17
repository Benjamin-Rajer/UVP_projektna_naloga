import requests
import time

from bs4 import BeautifulSoup, Comment
import re

import pomozni_podatki as POM


# podatki o sezoni, vrne BeautifulSoup
def pridobi_podatke_sezona(leto):

    stran = requests.get(POM.SEZONA_URL(leto), headers=POM.HEADERS)
    soup = BeautifulSoup(stran.text, "html.parser")

    time.sleep(5)

    return soup


def pridobi_podatke_igralec(id):
    ...

#======================== Pomožne funkcije =================================

# najde id in ime ekipe znotraj vrstice tabele
def id_ime_ekipe(vrstica):
    ekipa = vrstica.find("a")
    id = re.search(r"/teams/([A-Z]+)/\d+.html", ekipa["href"]).group(1)
    ime = ekipa.text
    return id, ime


# podatki znotraj ene celice tabele
def podatek_vrstice(vrstica, atribut):
    celica = vrstica.find("td", attrs = {"data-stat": atribut})

    if celica is None:
        return None

    return celica.text


# rezultate z vezajem (npr. 64-10) razdeli na dve števili
def razdeli_rezultat(podatek):
    return re.search(r"(\d+)-(\d+)", podatek).groups()

#======================== Glavne funkcije ==================================

def izlusci_podatke_konference(soup, leto):
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
            id_ekipe, ime_ekipe = id_ime_ekipe(vrstica)

            # konferenca
            if smer == "E":
                konferenca = "vzhodna"
            elif smer == "W":
                konferenca = "zahodna"
            else:
                konferenca = ""


            # zmage, porazi, točke
            zmage = podatek_vrstice(vrstica, "wins")
            porazi = podatek_vrstice(vrstica, "losses")
            povp_tocke = podatek_vrstice(vrstica, "pts_per_g") # povprečne dane točke na igro
            povp_prejeto = podatek_vrstice(vrstica, "opp_pts_per_g") # povprečne prejete točke na igro

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

    return seznam_podatkov


def izlusci_podatke_razsirjeno(soup, leto):
    seznam_podatkov = []

    # tabela razširjenih statistik - zakomentirana (poglej če je za vsa leta zakomentirana)
    tabela_raz = soup.find(
            string = lambda text: isinstance(text, Comment) and "div_expanded_standings" in text
                )

    tabela_soup = BeautifulSoup(tabela_raz, "html.parser").find("tbody")
    vrstice_raz = tabela_soup.find_all("tr")

    for vrstica in vrstice_raz:

        # id, ime
        id_ekipe, ime_ekipe = id_ime_ekipe(vrstica)

        # zmage, porazi kot domači, gosti, nevtralno
        doma = podatek_vrstice(vrstica, "Home")
        doma_z, doma_p = razdeli_rezultat(doma)

        gosti = podatek_vrstice(vrstica, "Road")
        gosti_z, gosti_p = razdeli_rezultat(gosti)

        # ne pojavi se vedno
        nevtralno = podatek_vrstice(vrstica, "Neutral")

        if nevtralno is None:
            nevtralno_z, nevtralno_p = "", ""
        else:
            nevtralno_z, nevtralno_p = razdeli_rezultat(nevtralno)

        # zmage, porazi z razliko točk manjšo ali enako 3
        mala_razlika = podatek_vrstice(vrstica, "3")
        mala_z, mala_p = razdeli_rezultat(mala_razlika)

        # zmage, porazi z razliko točk večjo ali enako 10
        velika_razlika = podatek_vrstice(vrstica, "10")
        velika_z, velika_p = razdeli_rezultat(velika_razlika)

        seznam_podatkov.append({
            "id": id_ekipe,
            "ime": ime_ekipe,
            "leto": leto,
            "zmage doma": doma_z,
            "porazi doma": doma_p,
            "zmage gosti": gosti_z,
            "porazi gosti": gosti_p,
            "zmage nevtralno": nevtralno_z,
            "porazi nevtralno": nevtralno_p,
            "zmaga <=3": mala_z,
            "poraz <=3": mala_p,
            "zmaga >=10": velika_z,
            "poraz >=10": velika_p
        })

    return seznam_podatkov

for leto in range(2020, 2027):
    spletna_soup = pridobi_podatke_sezona(leto)
    if spletna_soup:
        print(f"Uspešno pridobil podatke za leto {leto}")
    konf = izlusci_podatke_konference(spletna_soup, leto)
    raz = izlusci_podatke_razsirjeno(spletna_soup, leto)
    if konf and raz:
        print(f"Obdelal leto {leto}")
        print(konf[0])
        print(raz[0])

  





        

# začasno
#with open("UVP_projektna_naloga/spletne_strani/sezona_2026.html", "r",  encoding="ISO-8859-1") as dat:
#    soup1 = BeautifulSoup(dat.read(), "html.parser")
#
#print(izlusci_podatke_razsirjeno(soup1, 2026))

