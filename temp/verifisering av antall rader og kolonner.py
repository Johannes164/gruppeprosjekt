"""
Sjekker om CSV-fil har riktig antall kolonner i hver rad, samt riktig antall rader (altså at alle leses skikkelig).
"""

import csv

def sjekk_rader(fil, forventet_antall_kolonner):
    antall = 0
    feil = []

    with open(fil, "r", encoding="utf-8-sig") as f:
        leser = csv.reader(f, delimiter=";")
        neste = next(leser) # hopper over header rad

        for indeks, rad in enumerate(leser, start=2):
            antall += 1
            if len(rad) != forventet_antall_kolonner:
                feil.append(indeks)
    
    return antall, feil

filnavn = "trykk_og_temperaturlogg_rune_time.csv"
forventet = 5
antall_rader, feil_rader = sjekk_rader(filnavn, forventet)

print("Rune fil:")

print(f"Antall rader: {antall_rader}")
if feil_rader:
    print(f"Antall feilformaterte rader: {len(feil_rader)}")
    for indeks, rad in feil_rader:
        print(f"Feilformatert rad på linje {indeks+1}: {rad}")
else:
    print("Ingen feilformaterte rader funnet")




filnavn = "temperatur_trykk_met_samme_rune_time_datasett.csv"
forventet = 5
antall_rader, feil_rader = sjekk_rader(filnavn, forventet)

print("\nMet fil:")

print(f"Antall rader: {antall_rader}")
if feil_rader:
    print(f"Antall feilformaterte rader: {len(feil_rader)}")
    for indeks, rad in feil_rader:
        print(f"Feilformatert rad på linje {indeks+1}: {rad}")
else:
    print("Ingen feilformaterte rader funnet")