import csv
import datetime as dt
import matplotlib.pyplot as plt # importerer pyplot fra matplotlib modulen

RUNE_FILSTI = "trykk_og_temperaturlogg_rune_time.csv" # Definerer filstien til runedata
MET_FILSTI = "temperatur_trykk_met_samme_rune_time_datasett.csv" # Definerer filstien til metdata

def samle_rune_data(sti: str) -> dict:
    with open(sti, mode="r", encoding="utf-8-sig") as fil: # ingen forskjell på utf-8 og utf-8-sig her, men god praksis
        # Samler hver kolonne i en liste
        dato_tid = []
        stoppeklokke = []
        trykk_barometer = []
        trykk_absolutt = []
        temperatur = []

        # Hopper over header raden
        next(fil)

        for linje in csv.reader(fil, delimiter=";"):
            dato_tid.append(linje[0])
            stoppeklokke.append(int(linje[1]))
            trykk_barometer.append(linje[2])
            trykk_absolutt.append(linje[3])
            temperatur.append(linje[4])
        
        # Returnerer en dict med kolonnenavn som nøkler og kolonnelistene som verdier
        return {
            "dato_tid": dato_tid,
            "stoppeklokke": stoppeklokke,
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

def konverter_rune_dato_tid(data: dict):
    start_tid = dt.datetime.strptime(data["dato_tid"][1], "%m.%d.%Y %H:%M") + dt.timedelta(seconds=8) # konverterer datoen ved "Tid siden start" lik 0 til datetime objekt (man ser fra linje 12100 at starttiden egentlig er 8 sekunder senere)
    konverterte_datoer = []

    for sekunder_siden_start in data["stoppeklokke"]: # itererer gjennom listen med sekunder siden start
        konvertert = start_tid + dt.timedelta(seconds=sekunder_siden_start) # legger til antall sekunder siden start til start_tid, man kan plusse og trekke fra datetime objekter
        konverterte_datoer.append(konvertert)

    data["dato_tid"] = konverterte_datoer

def main():
    # samler dataen til ordbøker med lister
    rune_data = samle_rune_data(RUNE_FILSTI)    #   dato_tid, trykk_barometer, trykk_absolutt, temperatur
    met_data = samle_met_data(MET_FILSTI)       #   dato_tid, temperatur, trykk_hav
    
    # konverterer dato_tid til datetime objekter
    konverter_rune_dato_tid(rune_data)
    #konverter_met_dato_tid(met_data)

    # skriver ut datoene for å sjekke at konverteringen har gått riktig for seg
    #for i, dato in enumerate(rune_data["dato_tid"]):
    #    print(f"{i+1}: {dato.strftime('%d.%m.%Y %H:%M:%S')}") if i > 12092 and i < 12105 else None

    met_data_liste = list()
    met_data_liste_datetime = list()
    for element in met_data["dato_tid"]:
        met_data_liste.append(element)
    
    for tidspunkt in met_data_liste:
        datetime_tidspunkt = dt.datetime.strptime(tidspunkt,"%d.%m.%Y %H:%M")
        met_data_liste_datetime.append(datetime_tidspunkt)
    
    print(met_data_liste_datetime)
    

if __name__ == "__main__":
    main()