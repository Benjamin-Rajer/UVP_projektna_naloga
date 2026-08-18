# encoding za spletno stran je ISO-8859-1

# glave za HTTP zahtevo
HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/138.0.0.0 Safari/537.36",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
    "Accept-Language": "en-US,en;q=0.9",
}

LETA = range(1980, 2027)

#============================ URL-JI ===================================

# uporabljeni

# podatki o sezoni
def SEZONA_URL(leto):
    return f"https://www.basketball-reference.com/leagues/NBA_{leto}.html"

def SEZONA_IGRE_URL(leto):
    return f"https://www.basketball-reference.com/leagues/NBA_{leto}_standings.html"


# neuporabljeni

# končnica sezone 
def KONCNICA_URL(leto):
    return f"https://www.basketball-reference.com/playoffs/NBA_{leto}.html"

# podatki o vseh tekmah, razdeljenih po mesecih - oktober do junij
def TEKME_URL(leto, mesec):
    return f"https://www.basketball-reference.com/leagues/NBA_{leto}_games-{mesec}.html"

# podatki o ekipi v sezoni, vsaka ekipa je podana s tričkrovno kodo
def EKIPA_URL(koda, leto):
    return f"https://www.basketball-reference.com/teams/{koda}/{leto}.html"


# splošni podatki o igralcu, igralčev id je sestavljen iz delov imena in priimka ter iz številke
def IGRALEC_URL(id):
    return f"https://www.basketball-reference.com/players/{id[0]}/{id}.html"

# podatki o igralcu v sezoni
def IGRALEC_SEZONA_URL(id, leto):
    return f"https://www.basketball-reference.com/players/{id[0]}/{id}/gamelog/{leto}/"


#============================= PREVAJALNIK ==================================

PREVAJALNIK_DIVIZIJE = {
    # trenutne
    "Atlantic Division": "Atlantska",
    "Central Division": "Centralna",
    "Southeast Division": "Jugovzhodna",
    "Northwest Division": "Severozahodna",
    "Pacific Division": "Pacifiška",
    "Southwest Division": "Jugozahodna",

    # zgodovinske
    "Eastern Division": "Vzhodna",
    "Western Division": "Zahodna",
    "Midwest Division": "Srednjezahodna",
}

