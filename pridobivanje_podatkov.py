import requests
import time

from bs4 import BeautifulSoup, Comment
import re

import pomozni_podatki as POM


# pridobi spletno stran, vrne BeautifulSoup
def pridobi_stran(leto, url_funkcija):

    stran = requests.get(url_funkcija(leto), headers=POM.HEADERS)
    soup = BeautifulSoup(stran.text, "html.parser")

    time.sleep(5)

    return soup



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

def izlusci_statistiko(soup, leto):
    seznam_podatkov = []

    tabela = soup.find("table", id="totals-team").find("tbody")
    vrstice = tabela.find_all("tr")

    for vrstica in vrstice:

        # id, ime
        id_ekipe, ime_ekipe = id_ime_ekipe(vrstica)

        # odigrane minute
        minute = podatek_vrstice(vrstica, "mp")

        # število metov in poskusov
        meti_3 = podatek_vrstice(vrstica, "fg3")
        poskusi_3 = podatek_vrstice(vrstica, "fg3a")

        meti_2 = podatek_vrstice(vrstica, "fg2")
        poskusi_2 = podatek_vrstice(vrstica, "fg2a")

        meti_ft = podatek_vrstice(vrstica, "ft")
        poskusi_ft = podatek_vrstice(vrstica, "fta")

        # skoki (rebounds)
        skoki_nap = podatek_vrstice(vrstica, "orb")
        skoki_obr = podatek_vrstice(vrstica, "drb")

        # asistence (assists)
        asist = podatek_vrstice(vrstica, "ast")

        # ukradene žoge (steals)
        ukrad = podatek_vrstice(vrstica, "stl")

        # blokade (blocks)
        blokade = podatek_vrstice(vrstica, "blk")

        # izgubljene žoge (turnovers)
        izg = podatek_vrstice(vrstica, "tov")

        # osebni prekrški (personal fouls)
        prek = podatek_vrstice(vrstica, "pf")

        seznam_podatkov.append({
            "id": id_ekipe,
            "ime": ime_ekipe,
            "leto": leto,
            "odigrane minute": minute,
            "meti 3 točke": meti_3,
            "poskusi 3 točke": poskusi_3,
            "meti 2 točki": meti_2,
            "poskusi 2 točki": poskusi_2,
            "prosti meti": meti_ft,
            "poskusi prostih metov": poskusi_ft,
            "skoki v napadu": skoki_nap,
            "skoki v obrambi": skoki_obr,
            "asistence": asist,
            "ukradene žoge": ukrad,
            "blokade": blokade,
            "izgubljene žoge": izg,
            "osebni prekrški": prek
        })

    return seznam_podatkov


def izlusci_igre_konference(soup, leto):
    seznam_podatkov = []

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


def izlusci_igre_razsirjeno(soup, leto):
    seznam_podatkov = []

    # tabela razširjenih statistik - zakomentirana
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

        # zmage, porazi z razliko točk <= 3
        mala_razlika = podatek_vrstice(vrstica, "3")
        mala_z, mala_p = razdeli_rezultat(mala_razlika)

        # zmage, porazi z razliko točk >= 10
        velika_razlika = podatek_vrstice(vrstica, "10")
        velika_z, velika_p = razdeli_rezultat(velika_razlika)

        seznam_podatkov.append({
            "id": id_ekipe,
            "ime": ime_ekipe,
            "leto": leto,
            "zmage doma": doma_z,
            "porazi doma": doma_p,
            "zmage v gosteh": gosti_z,
            "porazi v gosteh": gosti_p,
            "zmage <= 3": mala_z,
            "porazi <= 3": mala_p,
            "zmage >= 10": velika_z,
            "porazi >= 10": velika_p
        })

    return seznam_podatkov
