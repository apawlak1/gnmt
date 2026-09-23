# -*- coding: utf-8 -*-
'''
GENEROWANIE WYKRESOW LINIOWYCH MAE/RMSE - FILTRACJA FP WZGLEDEM REFERENCJI NATYWNEJ

Wczytuje pliki *_baza_<metoda>_RAPORT_FP.txt (dla tego samego powiatu i roku,
we wszystkich testowanych rozdzielczosciach i bazach resamplingu) i rysuje
wykres liniowy:
    os X    = rozdzielczosc eksperymentalna
    kolor   = baza resamplingu (nearest / bilinear / bicubic)
    styl linii = etap (przed filtracja / FPDEMS / Guided Filter)
    os Y    = MAE lub RMSE WZGLEDEM REFERENCJI NATYWNEJ (nie wzgledem danych
              sprzed filtracji - to inna sekcja raportu)

Rekonstrukcja morfologiczna POMIJANA CELOWO (metoda odrzucona z dalszej analizy).

Uklad wykresu zgodny z wczesniejszym wykres_fp.py (linie skalowe NFP) -
ten sam styl kolorow/linii, zeby wykresy byly spojne wizualnie w calej pracy.
'''

import re
import glob
import os
import matplotlib
matplotlib.use('Agg')  # wymusza brak okien - tylko zapis do pliku
import matplotlib.pyplot as plt
import numpy as np

matplotlib.rcParams['font.family']='sans-serif'
matplotlib.rcParams['font.sans-serif']=['Arial']


def wczytaj_raport_fp(sciezka):
    '''
    Parsuje POJEDYNCZY plik RAPORT_FP.txt i zwraca:
      rozdzielczosc : float, rozdzielczosc eksperymentalna [m]
      baza          : str, baza resamplingu uzyta do filtracji (nearest/bilinear/bicubic)
      wzgledem_ref  : dict {'przed_filtracja': {'MAE':..,'RMSE':..},
                            'fpdems': {...}, 'guided_filter': {...}}
                      (rekonstrukcja_morfologiczna CELOWO POMINIETA)
    '''
    with open(sciezka, 'r', encoding='utf-8') as f:
        tresc=f.read()

    #---ROZDZIELCZOSC EKSPERYMENTALNA---
    dopasowanie_rozdz=re.search(r'Rozdzielczosc eksperymentalna:\s*([\d.]+)', tresc)
    if not dopasowanie_rozdz:
        raise ValueError(f'Nie znaleziono rozdzielczosci eksperymentalnej w {sciezka}')
    rozdzielczosc=float(dopasowanie_rozdz.group(1))

    #---BAZA RESAMPLINGU (nearest/bilinear/bicubic)---
    dopasowanie_baza=re.search(r'Mozaika bazowa dla filtracji FP:\s*(\w+)', tresc)
    if not dopasowanie_baza:
        raise ValueError(f'Nie znaleziono bazy resamplingu w {sciezka}')
    baza=dopasowanie_baza.group(1).strip().lower()

    #---WYCIECIE TYLKO SEKCJI "BLAD WZGLEDEM REFERENCJI NATYWNEJ"---
    #(w raporcie jest tez sekcja "BLAD WZGLEDEM DANYCH SPRZED FILTRACJI" -
    #ZUPELNIE INNA miara, ktorej tu NIE chcemy - stad wyciecie po nagłówku)
    dopasowanie_sekcji=re.search(
        r'=== BLAD WZGLEDEM REFERENCJI NATYWNEJ.*?===(.*?)(?:---SYGNATURY|$)',
        tresc, re.DOTALL)
    if not dopasowanie_sekcji:
        raise ValueError(f'Nie znaleziono sekcji "BLAD WZGLEDEM REFERENCJI NATYWNEJ" w {sciezka} '
                          f'(prawdopodobnie referencja_natywna nie byla podana przy generowaniu)')
    tresc_sekcji=dopasowanie_sekcji.group(1)

    wzgledem_ref={}

    #---PRZED FILTRACJA (osobny naglowek, bez "METODA")---
    dopasowanie_przed=re.search(
        r'---PRZED FILTRACJA.*?---\s*'
        r'liczba pikseli.*?\s*'
        r'MAE\s*=([\d.\-]+)\s*m\s*'
        r'RMSE\s*=([\d.\-]+)\s*m', tresc_sekcji)
    if dopasowanie_przed:
        wzgledem_ref['przed_filtracja']={'MAE': float(dopasowanie_przed.group(1)),
                                          'RMSE': float(dopasowanie_przed.group(2))}

    #---METODY FILTRACJI (fpdems, guided_filter) - REKONSTRUKCJA_MORFOLOGICZNA POMIJANA---
    bloki_metod=re.findall(
        r'---METODA (\w+) \(po filtracji.*?---\s*'
        r'liczba pikseli.*?\s*'
        r'MAE\s*=([\d.\-]+)\s*m\s*'
        r'RMSE\s*=([\d.\-]+)\s*m', tresc_sekcji)

    for nazwa_metody, mae, rmse in bloki_metod:
        nazwa_metody=nazwa_metody.strip().lower()
        if nazwa_metody == 'rekonstrukcja_morfologiczna':
            continue  # POMINIETA CELOWO - metoda odrzucona z analizy
        wzgledem_ref[nazwa_metody]={'MAE': float(mae), 'RMSE': float(rmse)}

    if not wzgledem_ref:
        raise ValueError(f'Nie udalo sie sparsowac zadnych statystyk w {sciezka}')

    return rozdzielczosc, baza, wzgledem_ref


#---KOLEJNOSC I ETYKIETY BAZ RESAMPLINGU (kolor)---
KOLEJNOSC_BAZ=['nearest', 'bilinear', 'bicubic']
ETYKIETY_BAZ={'nearest': 'Najbliższy sąsiad',
              'bilinear': 'Biliniowa',
              'bicubic': 'Bikubiczna'}
KOLORY_BAZ={'nearest': 'tab:blue', 'bilinear': 'tab:orange', 'bicubic': 'tab:green'}

#---KOLEJNOSC I STYLE ETAPOW FILTRACJI (linia)---
KOLEJNOSC_ETAPOW=['przed_filtracja', 'fpdems', 'guided_filter']
ETYKIETY_ETAPOW={'przed_filtracja': 'Przed filtracją',
                 'fpdems': 'FPDEMS',
                 'guided_filter': 'Guided Filter'}
STYLE_ETAPOW={'przed_filtracja': '-', 'fpdems': '--', 'guided_filter': ':'}


def wykres_liniowy_fp(sciezki_raportow, tytul, output_path, miara='RMSE'):
    '''
    sciezki_raportow : lista sciezek do plikow *_baza_<metoda>_RAPORT_FP.txt,
                        dla WSZYSTKICH testowanych rozdzielczosci i baz
                        resamplingu tego samego powiatu i roku
    tytul            : tytul wykresu, np. "Błąd filtracji NMT - Rzeszów 2024"
    output_path      : sciezka docelowa pliku PNG
    miara            : 'MAE' albo 'RMSE'
    '''
    #---WCZYTANIE: dane[baza][etap][rozdzielczosc] = wartosc miary---
    dane={}
    for sciezka in sciezki_raportow:
        rozdzielczosc, baza, wzgledem_ref=wczytaj_raport_fp(sciezka)
        dane.setdefault(baza, {})
        for etap, stats in wzgledem_ref.items():
            dane[baza].setdefault(etap, {})[rozdzielczosc]=stats[miara]

    if not dane:
        print(f'[WYKRES] Brak danych do narysowania ({tytul}).')
        return None

    #---KOLEJNOSC BAZ/ETAPOW: preferowana, reszta (jesli cos nieznanego) na koncu---
    bazy_obecne=sorted(dane.keys())
    bazy=[b for b in KOLEJNOSC_BAZ if b in bazy_obecne]
    bazy += [b for b in bazy_obecne if b not in KOLEJNOSC_BAZ]

    plt.figure(figsize=(8, 5))

    for baza in bazy:
        etapy_obecne=sorted(dane[baza].keys())
        etapy=[e for e in KOLEJNOSC_ETAPOW if e in etapy_obecne]
        etapy += [e for e in etapy_obecne if e not in KOLEJNOSC_ETAPOW]

        kolor=KOLORY_BAZ.get(baza, None)

        for etap in etapy:
            punkty=dane[baza][etap]
            rozdzielczosci=sorted(punkty.keys())
            wartosci=[punkty[r] for r in rozdzielczosci]

            plt.plot(rozdzielczosci, wartosci,
                     color=kolor, linestyle=STYLE_ETAPOW.get(etap, '-'),
                     marker='o', markersize=5, linewidth=1.8)

    #---LEGENDA 1: BAZA RESAMPLINGU (kolor) - linie-znaczniki bez stylu---
    legenda_baz=[plt.Line2D([0], [0], color=KOLORY_BAZ.get(b, 'gray'), lw=2,
                             label=ETYKIETY_BAZ.get(b, b.capitalize()))
                 for b in bazy]
    pierwsza_legenda=plt.legend(handles=legenda_baz, title='Baza resamplingu',
                                loc='upper left', bbox_to_anchor=(1.02, 1.0))
    plt.gca().add_artist(pierwsza_legenda)

    #---LEGENDA 2: ETAP FILTRACJI (styl linii) - czarne linie ze stylem---
    etapy_wszystkie=[e for e in KOLEJNOSC_ETAPOW
                     if any(e in dane[b] for b in bazy)]
    legenda_etapow=[plt.Line2D([0], [0], color='black', lw=1.8,
                               linestyle=STYLE_ETAPOW.get(e, '-'),
                               label=ETYKIETY_ETAPOW.get(e, e))
                    for e in etapy_wszystkie]
    plt.legend(handles=legenda_etapow, title='Seria',
              loc='center left', bbox_to_anchor=(1.02, 0.35))

    wszystkie_rozdzielczosci=sorted({r for b in dane.values() for e in b.values() for r in e.keys()})
    plt.xticks(wszystkie_rozdzielczosci, [f'{int(r)} m' for r in wszystkie_rozdzielczosci])
    plt.xlabel('Rozdzielczość eksperymentalna')
    plt.ylabel(f'{miara} względem referencji natywnej [m]')
    plt.title(f'{tytul}: {miara}')
    plt.grid(axis='both', linestyle='--', alpha=0.4)
    plt.tight_layout()

    plt.savefig(output_path, dpi=300, bbox_inches='tight')
    plt.close()
    print(f'[WYKRES] Zapisano: {output_path}')
    return output_path


if __name__ == '__main__':
    #---PRZYKLAD UZYCIA: znajdz wszystkie raporty FP dla danego powiatu i roku---
    #dopasuj sciezke do struktury folderow z Twojego cache_dir
    folder=r'C:\Users\strze\Pictures'

    #---KAZDY POWIAT/ROK OSOBNO: wzorzec dopasowuje wszystkie rozdzielczosci
    #i wszystkie bazy naraz (np. powiat_Rzeszów_2024_5m_baza_nearest_RAPORT_FP.txt,
    #..._10m_baza_bilinear_..., ..._20m_baza_bicubic_... itd.)---
    obszary={
        'Rzeszów_2024': 'Błąd filtracji NMT - Rzeszów 2024',
        'Sopot_2020': 'Błąd filtracji NMT - Sopot 2020',
        'Świnoujście_2019': 'Błąd filtracji NMT - Świnoujście 2019',
    }

    for prefiks, tytul in obszary.items():
        wzorzec=os.path.join(folder, f'powiat_{prefiks}_*_baza_*_RAPORT_FP.txt')
        sciezki=sorted(glob.glob(wzorzec))

        if not sciezki:
            print(f'[WYKRES] Brak plikow pasujacych do wzorca: {wzorzec}')
            continue

        print(f'[WYKRES] {prefiks}: znaleziono {len(sciezki)} raportow FP: {sciezki}')

        wykres_liniowy_fp(
            sciezki, tytul,
            os.path.join(folder, f'{prefiks}_FP_RMSE_liniowy.png'), miara='RMSE')
        wykres_liniowy_fp(
            sciezki, tytul,
            os.path.join(folder, f'{prefiks}_FP_MAE_liniowy.png'), miara='MAE')