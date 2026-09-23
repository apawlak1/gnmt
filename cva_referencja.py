# -*- coding: utf-8 -*-
'''
SYGNATURA SKALOWA CVA DLA REFERENCJI NATYWNEJ (ground truth)

Osobny modul - liczy CVA TYLKO dla nieprzefiltrowanej, niezgeneralizowanej
referencji natywnej i zapisuje wynik do wlasnego raportu tekstowego.

PO CO OSOBNO OD analiza.py / fp_filters.py:
CVA referencji NIE ZALEZY od rozdzielczosci eksperymentalnej ani od metody
FP - to jedna, stala charakterystyka prawdziwej rzezby terenu. Liczenie jej
przy kazdym wywolaniu analiza_fp_generalizacji (dla kazdej testowanej
rozdzielczosci/metody z osobna) bylby zbednym duplikowaniem tej samej pracy.
Tutaj liczymy ja RAZ dla danego powiatu/roku (dla pliku uzywanego jako
'referencja_natywna' w analiza.py) i mamy jeden wspolny punkt odniesienia
do porownania ze wszystkimi metodami/rozdzielczosciami.

UWAGA (okna w PIKSELACH, nie w metrach):
rozmiary_okien_cva sa podane w pikselach - dzieki temu ten sam zestaw okien
mozna uzyc niezaleznie od rozdzielczosci natywnej referencji, bez problemu
nieparzystosci fizycznego okna przy roznych rozdzielczosciach (patrz
ustalenia ws. wspolnego mianownika np. 0.5-20 m / 20-60 m).

POLACZENIE Z RESZTA KODU:
Modul korzysta z funkcji juz istniejacych w fp_filters.py (wczytaj_nmt,
sygnatura_skalowa_cva) - te same funkcje, ktorych uzywa analiza.py, wiec
wyniki sa w pelni porownywalne z sekcjami CVA w *_RAPORT_FP.txt.
Nie importuje nic z analiza.py (celowo, zeby uniknac zaleznosci
kolowej/duplikowania calego pipeline'u - to ma byc lekki, niezalezny krok).
'''

import os
from pathlib import Path

from fp_filters import wczytaj_nmt, sygnatura_skalowa_cva


def _round_cva_dict(cva_dict, miejsca=3):
    #---ZAOKRAGLA WARTOSCI CVA (KLUCZ=ROZMIAR OKNA, WARTOSC=CVA) DO 'miejsca' MIEJSC---
    #(kopia z analiza.py - celowo, zeby ten modul dzialal niezaleznie)
    return {okno: (round(wartosc, miejsca) if wartosc is not None else None)
            for okno, wartosc in cva_dict.items()}


def raport_cva_referencji_natywnej(referencja_natywna, output_dir, base_name,
                                    rozmiary_okien_cva=(3, 5, 7, 9, 11, 15, 21)):
    '''
    Liczy sygnature skalowa CVA DLA SAMEJ REFERENCJI NATYWNEJ (ground truth,
    NIEPRZFILTROWANEJ, NIEZGENERALIZOWANEJ) i zapisuje ja do OSOBNEGO raportu.

    referencja_natywna : sciezka do rastra ground truth (ten sam plik, ktory
        w analiza_fp_generalizacji sluzy jako punkt odniesienia do MAE/RMSE)
    output_dir : folder docelowy raportu
    base_name : nazwa bazowa uzywana w nazwie pliku raportu (np. powiat+rok)
    rozmiary_okien_cva : rozmiary okien W PIKSELACH (nie w metrach)

    Zwraca (cva_referencja, report_path).
    '''
    dem_ref, cellsize_ref, profil_ref=wczytaj_nmt(referencja_natywna)

    print(f'[CVA REFERENCJA] Liczenie sygnatury CVA dla referencji natywnej '
          f'(rozdzielczosc {cellsize_ref} m)...')
    cva_referencja=sygnatura_skalowa_cva(dem_ref, cellsize_ref, rozmiary_okien_cva)

    #---RAPORT TEKSTOWY---
    linie=[]
    linie.append(f'RAPORT SYGNATURY CVA REFERENCJI NATYWNEJ: {base_name}')
    linie.append('-'*60)
    linie.append(f'Plik referencyjny: {referencja_natywna}')
    linie.append(f'Rozdzielczosc natywna referencji: {cellsize_ref} m')
    linie.append('')
    linie.append('(sygnatura NIEZALEZNA od rozdzielczosci eksperymentalnej i')
    linie.append(' metody FP - wspolny punkt odniesienia dla wszystkich')
    linie.append(' rastrow zgeneralizowanych/przefiltrowanych tego powiatu/roku)')
    linie.append('')
    linie.append('---SYGNATURA SKALOWA CVA (okna w pikselach, zaokraglone do 3 msc)---')
    linie.append(f'REFERENCJA NATYWNA: {_round_cva_dict(cva_referencja)}')
    linie.append('')

    Path(output_dir).mkdir(parents=True, exist_ok=True)
    report_path=os.path.join(output_dir, f'{base_name}_RAPORT_CVA_REFERENCJA.txt')
    with open(report_path, 'w', encoding='utf-8') as f:
        f.write('\n'.join(linie))
    print(f'[CVA REFERENCJA] Zapisano raport: {report_path}')

    return cva_referencja, report_path


# ======================================================================
# URUCHOMIENIE NA POJEDYNCZYM PLIKU - podmien sciezki i odpal
# (analogicznie do oal.py / wykres.py w Twoim projekcie)
# ======================================================================
if __name__ == '__main__':
    #---PODMIEN NA WLASNA SCIEZKE DO REFERENCJI NATYWNEJ I FOLDER WYJSCIOWY---
    referencja_natywna=r'E:\GNMT\new\nmt_2024_powiat_Rzeszów\referencja_natywna\powiat_Rzeszów_2024_REFERENCJA_NATYWNA.tif'
    output_dir=r'E:\GNMT\new\nmt_2024_powiat_Rzeszów\referencja_natywna'
    base_name='powiat_Swinoujscie_2019'

    cva_referencja, report_path=raport_cva_referencji_natywnej(
        referencja_natywna, output_dir, base_name)

    print(f'\n[CVA REFERENCJA] Gotowe. Sygnatura: {cva_referencja}')
