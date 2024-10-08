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

def konverter_rune_dato_tid(data: dict):
    start_tid = dt.datetime.strptime(data["dato_tid"][0], "%m.%d.%Y %H:%M") + dt.timedelta(seconds=8) # konverterer datoen ved "Tid siden start" lik 0 til datetime objekt (man ser fra linje 12100 at starttiden egentlig er 8 sekunder senere)
    konverterte_datoer = []

    for sekunder_siden_start in data["stoppeklokke"]: # itererer gjennom listen med sekunder siden start
        konvertert = start_tid + dt.timedelta(seconds=sekunder_siden_start) # legger til antall sekunder siden start til start_tid, man kan plusse og trekke fra datetime objekter
        konverterte_datoer.append(konvertert)

    data["dato_tid"] = konverterte_datoer
    # ettersom liste og dict variabler er referanser, vil endringen her også endre den globale variabelen

def konverter_met_dato_tid(data: dict):
    met_data_liste_datetime = list()

    for tidspunkt in data["dato_tid"]:
            datetime_tidspunkt = dt.datetime.strptime(tidspunkt,"%d.%m.%Y %H:%M")
            met_data_liste_datetime.append(datetime_tidspunkt)
    data["dato_tid"] = met_data_liste_datetime
    # ettersom liste og dict variabler er referanser, vil endringen her også endre den globale variabelen

def konverter_temperatur(data: dict):
    temperaturer = []
    for temperatur in data["temperatur"]:
        temperaturer.append(float(temperatur.replace(",", ".")))
    data["temperatur"] = temperaturer


# oppgave g)
def reduser_stoy(y_verdier: list, x_verdier: list, snitt_delta: int):
    """
    Reduserer volatiliteten til en gitt mengde y verdier ved å for hvert punkt ta snittet av de alle punktene fra x-snitt_delta til x+snitt_delta.
    """
    redusert_y = [] # tom liste for de reduserte y verdiene

    for i in range(snitt_delta, len(y_verdier) - snitt_delta):
        snitt = sum(y_verdier[i-snitt_delta:i+snitt_delta+1]) / (2*snitt_delta+1) # tar snittet av punktene fra og med x-snitt_delta til og med x+snitt_delta
        redusert_y.append(snitt) # legger til snittet i listen
    
    redusert_x = x_verdier[snitt_delta:len(x_verdier)-snitt_delta] # fjerner de første og siste snitt_delta punktene fra x verdiene
    return redusert_y, redusert_x

# oppgave h)
#finner indeksen til 11. juni 17.31 og 12. juni 03.05
def temperaturfall(data: dict):
    indeks_11_juni = data["dato_tid"].index(dt.datetime(2021, 6, 11, 17, 31, 8)) # finner indeksen til 11. juni 17.31
    indeks_12_juni = data["dato_tid"].index(dt.datetime(2021, 6, 12, 3, 5, 8))
    x_verdier = [data["dato_tid"][indeks_11_juni], data["dato_tid"][indeks_12_juni]]
    y_verdier = [data["temperatur"][indeks_11_juni], data["temperatur"][indeks_12_juni]]
    return x_verdier, y_verdier


# oppgave i)
def konverter_barometrisk_trykk(data: dict):
    y_verdier = []
    x_verdier = []
    for i, trykk in enumerate(data["trykk_barometer"]):
        if trykk != "":
            y_verdier.append(float(trykk.replace(",", "."))*10) # ganger med 10, siden tallene ligger rundt 100 i csv fila som virker som en feil
            x_verdier.append(data["dato_tid"][i])
    return y_verdier, x_verdier

def konverter_absolutt_trykk(data: dict):
    y_verdier = []
    x_verdier = []
    for i, trykk in enumerate(data["trykk_absolutt"]):
        y_verdier.append(float(trykk.replace(",","."))*10) # ganger med 10, siden tallene ligger rundt 100 i csv fila som virker som en feil
        x_verdier.append(data["dato_tid"][i])
    return y_verdier, x_verdier

def konverter_trykk_hav(data: dict):
    y_verdier = []
    x_verdier = []
    for i, trykk in enumerate(data["trykk_hav"]):
        y_verdier.append(float(trykk.replace(",","."))) # ganger med 10, siden tallene ligger rundt 100 i csv fila som virker som en feil
        x_verdier.append(data["dato_tid"][i])
    return y_verdier, x_verdier
    

def plotting(oppg_f, oppg_g, oppg_h, oppg_i1, oppg_i2, oppg_i3):
    
    # oppgave f) plotter temperatur mot tid
    plt.subplot(2,1,1)
    xaksemet = oppg_f[0]["dato_tid"]
    yaksemet = oppg_f[0]["temperatur"]
    plt.plot(xaksemet,yaksemet, color="green", label="Temperatur MET")


    xakserune = oppg_f[1]["dato_tid"]
    yakserune = oppg_f[1]["temperatur"]
    plt.plot(xakserune,yakserune, label ="Temperatur")

    # oppgave g) plotter redusert temperatur med tid
    plt.plot(oppg_g[0], oppg_g[1], label="Gjennomsnittstemperatur", color="orange")

    # oppgave h) plotter temperaturfall som en linje mellom de to punktene
    plt.plot(oppg_h[0], oppg_h[1], color="purple", label="Temperaturfall")
    
    plt.xlabel("Tid")
    plt.ylabel("Temperatur")
    plt.legend()




    # oppgave i) 
    plt.subplot(2,1,2)
    plt.plot(oppg_i1[1], oppg_i1[0], color="orange", label="Barometrisk trykk") #plotter barometrisk trykk mot tid
    plt.plot(oppg_i2[1], oppg_i2[0], color="blue", label="Absolutt trykk") #plotter absolutt trykk mot tid
    plt.plot(oppg_i3[1], oppg_i3[0], color="green", label="Absolutt trykkk MET") #plotter trykk hav mot tid
    plt.xlabel("Tid")
    plt.ylabel("Trykk")
    
    
    plt.legend()
    plt.show()

def main():
    # samler dataen til ordbøker med lister
    rune_data = samle_rune_data(RUNE_FILSTI)    #   dato_tid, trykk_barometer, trykk_absolutt, temperatur
    met_data = samle_met_data(MET_FILSTI)       #   dato_tid, temperatur, trykk_hav
    
    # konverterer dato_tid til datetime objekter
    konverter_rune_dato_tid(rune_data)
    konverter_met_dato_tid(met_data)

    # konverterer temperatur til float
    konverter_temperatur(rune_data)
    konverter_temperatur(met_data)

    redusert_temperatur, redusert_dato = reduser_stoy(rune_data["temperatur"], rune_data["dato_tid"], 30) # oppgave g)

    tempfall_tider, tempfall_temperaturer = temperaturfall(rune_data) # oppgave h)
    
    barometrisk_trykk, barometrisk_dato = konverter_barometrisk_trykk(rune_data) # oppgave i)

    absolutt_trykk, absolutt_dato = konverter_absolutt_trykk(rune_data) #oppgave i

    hav_trykk, hav_trykk_dato = konverter_trykk_hav(met_data) #oppgave i

    plotting((met_data, rune_data), (redusert_dato, redusert_temperatur), (tempfall_tider, tempfall_temperaturer), (barometrisk_trykk, barometrisk_dato), (absolutt_trykk, absolutt_dato), (hav_trykk, hav_trykk_dato))

if __name__ == "__main__":
    main()