import csv
from datetime import datetime # importerer datetime objektet fra datetime modulen
import matplotlib.pyplot as plt # importerer pyplot fra matplotlib modulen

RUNE_FILSTI = "trykk_og_temperaturlogg_rune_time.csv" # Definerer filstien til runedata
MET_FILSTI = "temperatur_trykk_met_samme_rune_time_datasett.csv" # Definerer filstien til metdata

def samle_rune_data(sti: str) -> dict:
    with open(sti, mode="r", encoding="utf-8-sig") as fil: # ingen forskjell på utf-8 og utf-8-sig her, men god praksis
        # Samler hver kolonne i en liste
        dato_tid = []
        trykk_barometer = []
        trykk_absolutt = []
        temperatur = []

        for linje in csv.reader(fil, delimiter=";"):
            dato_tid.append(linje[0])
            trykk_barometer.append(linje[2])
            trykk_absolutt.append(linje[3])
            temperatur.append(linje[4])
        
        # Returnerer en dict med kolonnenavn som nøkler og kolonnelistene som verdier
        return {
            "dato_tid": dato_tid,
            "trykk_barometer": trykk_barometer,
            "trykk_absolutt": trykk_absolutt,
            "temperatur": temperatur
        }

def samle_met_data(sti: str) -> dict:
    with open(sti, mode="r", encoding="utf-8-sig") as fil: # -,-
        # Samler hver kolonne i en liste
        dato_tid = []
        temperatur = []
        trykk_hav = []

        for linje in csv.reader(fil, delimiter=";"):
            dato_tid.append(linje[2])
            temperatur.append(linje[3])
            trykk_hav.append(linje[4])
        
        # Returnerer en dict med kolonnenavn som nøkler og kolonnelistene som verdier
        return {
            "dato_tid": dato_tid,
            "temperatur": temperatur,
            "trykk_hav": trykk_hav
        }

def konverter_dato_tid(data: dict):
    konverterte_datoer = []
    for dato in data["dato_tid"]:
        try:
            if "am" in dato.lower() or "pm" in dato.lower():
                konvertert = datetime.strptime(dato, "%m/%d/%Y %I:%M:%S %p")
            else:
                konvertert = datetime.strptime(dato, "%m.%d.%Y %H:%M")
            konverterte_datoer.append(konvertert)
        except ValueError as e:
            print(f"Kunne ikke konvertere dato {dato} til datetime objekt: {e}")

    data["dato_tid"] = konverterte_datoer

def main():
    # samler dataen til ordbøker med lister
    rune_data = samle_rune_data(RUNE_FILSTI)    #   dato_tid, trykk_barometer, trykk_absolutt, temperatur
    met_data = samle_met_data(MET_FILSTI)       #   dato_tid, temperatur, trykk_hav
    
    # konverterer dato_tid til datetime objekter
    konverter_dato_tid(rune_data)
    konverter_dato_tid(met_data)
    

if __name__ == "__main__":
    main()