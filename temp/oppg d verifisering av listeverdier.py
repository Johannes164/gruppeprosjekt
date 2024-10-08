import csv
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
        for linje in csv.reader(fil, delimiter=";"):
            dato_tid.append(linje[0])
            stoppeklokke.append(linje[1])
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

def main():
    rune_data = samle_rune_data(RUNE_FILSTI)
    #met_data = samle_met_data(MET_FILSTI)
    
if __name__ == "__main__":
    main()





    # Alt over er main filen ved tidspunktet jeg skriver denne testen

def test_samle_rune_data():
    linjer_som_sjekkes = [0, 1, 2, 3, 10, 100, 1000, 4000, 8000, 15000, 20000, 20220, 20221, 20222, 20223]
    rune_data = samle_rune_data(RUNE_FILSTI)
    for linje in linjer_som_sjekkes:
        assert rune_data["dato_tid"][linje] != ""
        assert rune_data["stoppeklokke"][linje] != ""
        #assert rune_data["trykk_barometer"][linje] != ""
        assert rune_data["trykk_absolutt"][linje] != ""
        assert rune_data["temperatur"][linje] != ""
    
    
    
        print(f"Linje {linje} i RUNE-filen har data")
        print(f"Dato og tid: {rune_data['dato_tid'][linje]}")
        print(f"Stoppeklokke: {rune_data['stoppeklokke'][linje]}")
        print(f"Trykk barometer: {rune_data['trykk_barometer'][linje]}")
        print(f"Trykk absolutt: {rune_data['trykk_absolutt'][linje]}")
        print(f"Temperatur: {rune_data['temperatur'][linje]}")

test_samle_rune_data()

# resultat: alt ser ut til å fungere som det skal