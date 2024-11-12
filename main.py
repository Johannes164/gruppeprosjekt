

import csv
import datetime as dt
import matplotlib.pyplot as plt # importerer pyplot fra matplotlib modulen
import numpy as np

RUNE_FILSTI = "trykk_og_temperaturlogg_rune_time.csv" # Definerer filstien til runedata
MET_FILSTI = "temperatur_trykk_met_samme_rune_time_datasett.csv" # Definerer filstien til metdata
SAUDA_SINNES_FILSTI = "temperatur_trykk_sauda_sinnes_samme_tidsperiode.csv.txt"


# oppgave d)
def samle_rune_data(sti: str) -> dict:
    """
    Samler runedataen i en ordbok med lister
    """
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

# oppgave d)
def samle_met_data(sti: str) -> dict:
    """
    Samler metdataen i en ordbok med lister
    """
    with open(sti, mode="r", encoding="utf-8-sig") as fil: # -,-
        # Samler hver kolonne i en liste
        dato_tid = []
        temperatur = []
        trykk_hav = []

        # Hopper over header raden
        next(fil)

        # Samler radene i en liste for å hoppe over siste rad
        rader = list(csv.reader(fil, delimiter=";"))

        for linje in rader[:-1]:
            dato_tid.append(linje[2])
            temperatur.append(linje[3])
            trykk_hav.append(linje[4])
        
        # Returnerer en dict med kolonnenavn som nøkler og kolonnelistene som verdier
        return {
            "dato_tid": dato_tid,
            "temperatur": temperatur,
            "trykk_hav": trykk_hav
        }
    
def samle_sinnes_sauda_data(sti):
    dato_tid_sinnes = []
    temp_sinnes = []
    trykk_sinnes = []

    dato_tid_sauda = []
    temp_sauda = []
    trykk_sauda = []

    with open(sti, "r", encoding="UTF8") as fila:
        next(fila)
        for linje in fila:

            liste_med_data = linje.split(";")
            if liste_med_data[0] == "Sirdal - Sinnes":
                dato_tid_sinnes.append(liste_med_data[2])
                temp_sinnes.append(liste_med_data[3])
                trykk_sinnes.append(liste_med_data[4])
            else:
                if liste_med_data[3] == "":
                    continue
                dato_tid_sauda.append(liste_med_data[2])
                temp_sauda.append(liste_med_data[3])
                trykk_sauda.append(liste_med_data[4])
    
    return {
        "dato_tid" : dato_tid_sinnes,
        "temperatur" : temp_sinnes,
        "trykk_hav" : trykk_sinnes
        }, {
           "dato_tid" : dato_tid_sauda,
           "temperatur" : temp_sauda,
           "trykk_hav" : trykk_sauda
        }

# oppgave e)
def konverter_dato_tid(data: dict, set="rune") -> None:
    """
    Konverterer dato_tid strengene til datetime objekter
    """
    if set == "rune":
        start_tid = dt.datetime.strptime(data["dato_tid"][0], "%m.%d.%Y %H:%M") + dt.timedelta(seconds=8) # konverterer datoen ved "Tid siden start" lik 0 til datetime objekt (man ser fra linje 12100 at starttiden egentlig er 8 sekunder senere)
        data["dato_tid"] = [start_tid + dt.timedelta(seconds=int(tid)) for tid in data["stoppeklokke"]] 
    elif set == "met":
        data["dato_tid"] = [dt.datetime.strptime(tidspunkt, "%d.%m.%Y %H:%M") for tidspunkt in data["dato_tid"]]
    elif set == "sinnes" or set == "sauda":
        data["dato_tid"] = [dt.datetime.strptime(tidspunkt, "%d.%m.%Y %H:%M") for tidspunkt in data["dato_tid"]]
    # ettersom liste og dict variabler er referanser, vil endringen her også endre den globale variabelen

def konverter_temperatur(data: dict) -> None:
    """
    Går gjennom listen med temperaturer og konverterer de til float verdier
    Her gjøres det permanent for ordbøkenes data, mens for trykkene gjøres det ikke permanent ettersom det ikke behøves
    fordi hver bare brukes én gang
    Her gjør vi det permanent fordi vi bruker temperatur dataen flere ganger og for å bevise at vi klarer dette
    """
    temperaturer = []
    for temperatur in data["temperatur"]:
        temperaturer.append(float(temperatur.replace(",", ".")))
    data["temperatur"] = temperaturer


# oppgave g)
def reduser_stoy(y_verdier: list, x_verdier: list, snitt_delta: int) -> tuple:
    """
    Reduserer volatiliteten til en gitt mengde y verdier ved å for hvert punkt ta snittet av de alle punktene fra x-snitt_delta til x+snitt_delta.
    Returnerer de x og y verdier for plotting
    """
    redusert_y = [] # tom liste for de reduserte y verdiene

    for i in range(snitt_delta, len(y_verdier) - snitt_delta):
        snitt = sum(y_verdier[i-snitt_delta:i+snitt_delta+1]) / (2*snitt_delta+1) # tar snittet av punktene fra og med x-snitt_delta til og med x+snitt_delta
        redusert_y.append(snitt) # legger til snittet i listen
    
    redusert_x = x_verdier[snitt_delta:len(x_verdier)-snitt_delta] # fjerner de første og siste snitt_delta punktene fra x verdiene
    return redusert_y, redusert_x

# oppgave h)
def temperaturfallrune(data: dict) -> tuple:
    """
    Finner temperaturfallet fra 11. juni 17.31 til 12. juni 03.05 og returnerer x og y verdier for plotting
    """
    indeks_11_juni = data["dato_tid"].index(dt.datetime(2021, 6, 11, 17, 31, 8)) # finner indeksen til 11. juni 17.31
    indeks_12_juni = data["dato_tid"].index(dt.datetime(2021, 6, 12, 3, 5, 8)) # finner indeksen til 12. juni 03.05
    x_verdier = [data["dato_tid"][indeks_11_juni], data["dato_tid"][indeks_12_juni]]
    y_verdier = [data["temperatur"][indeks_11_juni], data["temperatur"][indeks_12_juni]]
    return x_verdier, y_verdier

#Oppgave 10a
def temperaturfallmet(data: dict):
    indeks_11_juni = data["dato_tid"].index(dt.datetime(2021, 6, 11, 17)) # finner indeksen til 11. juni 17.31
    indeks_12_juni = data["dato_tid"].index(dt.datetime(2021, 6, 12, 3)) # finner indeksen til 12. juni 03.05
    x_verdier = [data["dato_tid"][indeks_11_juni], data["dato_tid"][indeks_12_juni]]
    y_verdier = [data["temperatur"][indeks_11_juni], data["temperatur"][indeks_12_juni]]
    return x_verdier, y_verdier

# oppgave i)
def konverter_trykk(data: dict, kolonnenavn: str, multipliser: float=1.0) -> tuple:
    """
    Konverterer trykkdata til float verdier og returnerer x og y verdier for plotting.
    Kolonnenavn definerer hvilken trykk-kolonne som skal konverteres.
    Multipliserer med en verdi for å korrigere for feil i dataen.
    """
    y_verdier = []
    x_verdier = []
    for i, trykk in enumerate(data[kolonnenavn]):
        if trykk:
            y_verdier.append(float(trykk.replace(",", ".")) * multipliser)
            x_verdier.append(data["dato_tid"][i])
    return y_verdier, x_verdier

def subplot(posisjon: int, x_label: str, y_label: str) -> None:
    """
    Setter opp en subplot med gitt posisjon og x og y labels
    """
    plt.subplot(2, 1, posisjon) # setter opp subplot
    plt.xlabel(x_label) # setter x label
    plt.ylabel(y_label) # setter y label


def differanse_trykk(data:dict):
    diff_liste = list()
    
    for i in range(len(data["trykk_absolutt"])):
        if data["trykk_barometer"][i] == "":
            continue
        diff_liste.append((float(data["trykk_barometer"][i].replace(",","."))-float(data["trykk_absolutt"][i].replace(",",".")))*10)
    return diff_liste







# oppgave 10 b)


def temperatur_histogram(rune_data: dict, met_data: dict, sinnes_data: dict, sauda_data: dict, splitt_datasett=False) -> tuple:
    """
    Forbereder data for plotting av et histogram over temperaturene fra alle datasettene.
    Returnerer den kontakinerte temperaturdataen og bin kantene.
    """

    samlet_rune_temp = rune_temperatur_timevis(rune_data) # henter gjennomsnittstemperaturen for hver time

    # konkatinerer alle temperaturdataene
    alle_temperaturer = (
        samlet_rune_temp["temperatur"]
        + met_data["temperatur"]
        + sinnes_data["temperatur"]
        + sauda_data["temperatur"]
    )
    
    # Finn minste og største temperatur, rundet til nærmeste heltall
    min_temp = int(min(alle_temperaturer))
    max_temp = int(max(alle_temperaturer)) + 1  # Legger til 1 for å også inkludere den høyeste temperaturen
    
    # lager bins for hver hele grad
    bins = np.arange(min_temp, max_temp, 1)
    
    if not splitt_datasett:
        return alle_temperaturer, bins
    return (
        samlet_rune_temp["temperatur"], 
        met_data["temperatur"], 
        sinnes_data["temperatur"], 
        sauda_data["temperatur"]
        ), bins

def rune_temperatur_timevis(rune_data: dict) -> dict:
    """
    Returnerer en dict med timen som nøkkel og snitt temperatur for den timen som verdi for å unngå overrepresentasjon
    grunnet høy frekvens av målinger
    """
    timevis_temperatur = {}

    for time, temp in zip(rune_data["dato_tid"], rune_data["temperatur"]):
        time = time.replace(minute=0, second=0, microsecond=0)
        # hvis timen ikke er i ordboken, legg til timen som nøkkel og en liste med temperaturene som verdi
        if time not in timevis_temperatur:
            timevis_temperatur[time] = [temp]
        else:
            timevis_temperatur[time].append(temp)

    # regner ut gjennomsnittstemperaturen for hver time
    samlede_temperaturer = {
        "dato_tid": [],
        "temperatur": []
    }

    for time, temperaturer in sorted(timevis_temperatur.items()):
        samlede_temperaturer["dato_tid"].append(time)
        samlede_temperaturer["temperatur"].append(sum(temperaturer) / len(temperaturer))

    return samlede_temperaturer


def main():
    
    # oppgave d) samler dataen til ordbøker med lister
    rune_data = samle_rune_data(RUNE_FILSTI)    #   dato_tid, trykk_barometer, trykk_absolutt, temperatur
    met_data = samle_met_data(MET_FILSTI)       #   dato_tid, temperatur, trykk_hav
    
    sinnes_data, sauda_data = samle_sinnes_sauda_data(SAUDA_SINNES_FILSTI)

    # oppgave e) konverterer dato_tid til datetime objekter
    konverter_dato_tid(rune_data)
    konverter_dato_tid(met_data, set="met")
    konverter_dato_tid(sinnes_data, set="sinnes")
    konverter_dato_tid(sauda_data, set="sauda")

    # konverterer strengene til float
    konverter_temperatur(rune_data)
    konverter_temperatur(met_data)
    konverter_temperatur(sinnes_data)
    konverter_temperatur(sauda_data)


    # oppgave f) plotter temperatur mot tid
    plt.figure(figsize=(7.8, 7.8)) # setter størrelsen på plottet
    subplot(1, "Tid", "Temperatur")
    plt.xticks(rotation=10)

    plt.plot(rune_data["dato_tid"], rune_data["temperatur"], label="Temperatur") # temp rune
    plt.plot(met_data["dato_tid"], met_data["temperatur"], color="green", label="Temperatur MET") # temp MET
    plt.plot(sinnes_data["dato_tid"], sinnes_data["temperatur"], color="red", label="Temperatur Sinnes") #temp Sinnes
    plt.plot(sauda_data["dato_tid"], sauda_data["temperatur"], color="black",label="Temperatur Sauda") #temp Sauda


    # Oppgave g) plotter gjennomsnittstemperaturen for +- 30 elementer (5 minutter) rundt hvert punkt
    redusert_temperatur, redusert_dato = reduser_stoy(rune_data["temperatur"], rune_data["dato_tid"], 30) # henter verdiene for x og y aksene
    plt.plot(redusert_dato, redusert_temperatur, color="orange", label="Gjennomsnittstemperatur") # Gjennomsnittstemperatur


    # oppgave h) plotter temperaturfall fra 11. juni 17.31 til 12. juni 03.05
    tempfall_tider_rune, tempfall_temperaturer_rune = temperaturfallrune(rune_data)
    plt.plot(tempfall_tider_rune, tempfall_temperaturer_rune, color="purple", label="Temperaturfall rune_data") # Temperaturfall

  # Oppgave 10 a)
    tempfall_tider_metdata, tempfall_temperaturer_metdata = temperaturfallmet(met_data)
    plt.plot(tempfall_tider_metdata, tempfall_temperaturer_metdata, color="blue", label="Temperaturfall met_data")

   
    # oppgave i)
    plt.legend()
    subplot(2, "Tid", "Trykk") # setter opp subplot
    plt.xticks(rotation=10)

    barometrisk_trykk, barometrisk_dato = konverter_trykk(rune_data, "trykk_barometer", multipliser=10) # 1. henter x og y verdier for barometrisk trykk
    plt.plot(barometrisk_dato, barometrisk_trykk, color="orange", label="Barometrisk trykk") #plotter barometrisk trykk mot tid

    absolutt_trykk, absolutt_dato = konverter_trykk(rune_data, "trykk_absolutt", multipliser=10) # 2. henter x og y verdier for absolutt trykk (atmosfærisk trykk)
    plt.plot(absolutt_dato, absolutt_trykk, label="Absolutt trykk") #plotter absolutt trykk mot tid

    hav_trykk_met, hav_trykk_dato_met = konverter_trykk(met_data, "trykk_hav") # 3. henter x og y verdier for hav trykk (atmosfærisk trykk)
    plt.plot(hav_trykk_dato_met, hav_trykk_met, color="green", label="Havtrykk MET") #plotter trykk hav mot tid


    # Oppgave 10 d)
    hav_trykk_sinnes, hav_trykk_dato_sinnes = konverter_trykk(sinnes_data,"trykk_hav")
    plt.plot(hav_trykk_dato_sinnes, hav_trykk_sinnes, color="purple", label="Havtrykk Sinnes")

    hav_trykk_sauda, hav_trykk_dato_sauda = konverter_trykk(sauda_data, "trykk_hav")
    plt.plot(hav_trykk_dato_sauda, hav_trykk_sauda, color="yellow", label="Havtrykk Sauda")
    
    plt.legend() 
    plt.show()

    # oppgave 10 b)
    splitt = True
    plt.figure(figsize=(7.8, 7.8)) # setter størrelsen på plottet
    subplot(1, "Temperatur", "Antall") # setter opp subplot

    #henter data for histogrammet
    if not splitt: # plotter histogrammet for alle datasettene samlet
        alle_temperaturer, bins = temperatur_histogram(rune_data, met_data, sinnes_data, sauda_data)

        # lager histogrammet
        plt.hist(alle_temperaturer, bins=bins, color="blue", edgecolor="black", alpha=0.7, label="Temperatur histogram")

    else: # plotter histogrammet for hvert datasett
        #henter temperaturdata for hvert datasett
        (rune_temp, met_temp, sinnes_temp, sauda_temp), bins = temperatur_histogram(rune_data, met_data, sinnes_data, sauda_data, splitt_datasett=splitt)
        datasett = [rune_temp, met_temp, sinnes_temp, sauda_temp]
        farger = ["blue", "green", "red", "black"]
        labels = ["Rune", "MET", "Sinnes", "Sauda"]

        # plotter histogrammet for hvert datasett
        plt.hist(datasett, bins=bins, color=farger, edgecolor="black", alpha=0.7, label=labels)

    plt.xticks(bins) # setter x ticks til hver hele grad
    
    # 10c)
    plt.legend()
    subplot(2, "Tid", "Trykk differanse")
    plt.xticks(rotation=10, fontsize=8)

    differanse = differanse_trykk(rune_data)
    diff_redusert, barometrisk_dato_redsert = reduser_stoy(differanse, barometrisk_dato, 10)
    plt.plot(barometrisk_dato_redsert, diff_redusert, label="Trykk differanse")

    plt.legend(loc="upper left") 

    plt.show()

    


if __name__ == "__main__":
    main()







"""
Plott data fra noen andre værstasjoner. Ei fil med data fra værstasjonene Sinnes og
Sauda er lagt ved. I denne fila er data for begge værstasjonene med i samme fil, bruk
første kolonne for å skille mellom de to værstasjonene. Denne fila er i samme format
som fila fra Sola værstasjon fra øving 7. Data for værstasjonene Sola, Sauda og Sinnes
skal alle plottes i samme plott og gjerne sammen med glattete data for UiS datasettet.

Hint 1: Den enkleste løsningen er kanskje å skrive et separat script som splitter fila med
værdata fra Sinnes og Sauda i separate filer, en for hver værstasjon. Disse separate filene
kan deretter leses med samme kode som for øving 6 deloppgave d).

Hint 2: Fila fra Sauda og Sinnes starter litt tidligere enn fila for Sola. Dere velger selv om
dere tar med alt fra Sauda og Sinnes eller om dere kutter starten slik at plottet starter på
tidspunktet hvor Sola-fila starter.
"""