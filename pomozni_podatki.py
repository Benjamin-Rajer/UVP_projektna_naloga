# encoding za spletno stran je ISO-8859-1

# glave za HTTP zahtevo - pomagajo, da nam zahteva uspe
HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/138.0.0.0 Safari/537.36",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
    "Accept-Language": "en-US,en;q=0.9",
}


#-------------------------------URL-JI---------------------------------
# podatki o sezoni
def SEZONA_URL(leto):
    return f"https://www.basketball-reference.com/leagues/NBA_{leto}_standings.html"


# podatki o ekipi v sezoni, vsaka ekipa je podana s tričkrovno kodo
def EKIPA_URL(koda, leto):
    return f"https://www.basketball-reference.com/teams/{koda}/{leto}.html"


# splošni podatki o igralcu, igralčev id je sestavljen iz delov imena in priimka ter iz številke
def IGRALEC_URL(id):
    return f"https://www.basketball-reference.com/players/{id[0]}/{id}.html"


# podatki o igralcu v sezoni
def IGRALEC_SEZONA_URL(id, leto):
    return f"https://www.basketball-reference.com/players/{id[0]}/{id}/gamelog/{leto}/"
