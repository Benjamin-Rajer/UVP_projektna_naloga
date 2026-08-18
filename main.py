import csv
import os

import pridobivanje_podatkov as prid
import pomozni_podatki as POM



def shrani_v_csv(seznam, ime_datoteke):
    
    with open(f"CSV_datoteke/{ime_datoteke}", "a", newline="", encoding="utf-8") as dat:
        writer = csv.DictWriter(
            dat,
            fieldnames= list(seznam[0].keys())
        )

        if os.path.getsize(f"CSV_datoteke/{ime_datoteke}") == 0:
            writer.writeheader()

        writer.writerows(seznam)

# izprazni CSV datoteke ko še enkrat poženemo program, da lahko zajamemo vedno nove podatke
def izprazni_csv(ime_datoteke):
    with open(f"CSV_datoteke/{ime_datoteke}", "w", newline="", encoding="utf-8"):
        pass

def main():

    izprazni_csv("statistika.csv")
    izprazni_csv("konference.csv")
    izprazni_csv("razsirjeno.csv")

    for leto in POM.LETA:

        print(f"\rPridobivam podatke za leto {leto}.", end="")


        stran = prid.pridobi_stran(leto, POM.SEZONA_URL)

        statistika = prid.izlusci_statistiko(stran, leto)
        shrani_v_csv(statistika, "statistika.csv")


        stran_igre = prid.pridobi_stran(leto, POM.SEZONA_IGRE_URL)

        konferenca = prid.izlusci_igre_konference(stran_igre, leto)
        shrani_v_csv(konferenca, "konference.csv")

        razsirjeno = prid.izlusci_igre_razsirjeno(stran_igre, leto)
        shrani_v_csv(razsirjeno, "razsirjeno.csv")

    print("\nKončano.")




if __name__ == "__main__":
    main()