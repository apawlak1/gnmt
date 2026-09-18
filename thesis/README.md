# geo_nmt: wersja z pracy magisterskiej

Ta wersja została wykorzystana w pracy magisterskiej:
**„Generalizacja Numerycznego Modelu Terenu z zastosowaniem filtracji adaptacyjnej”**
Aleksandra Pawlak, Politechnika Gdańska, Wydział Inżynierii Lądowej i Środowiska

**Filtracja adaptacyjna** zgeneralizowanych danych — dwiema metodami typu feature-preserving:
   - **FPDEMS** — filtr oparty na wygładzaniu pola wektorów normalnych, z zachowaniem krawędzi terenu (próg kątowy θt, parametr max_diff)
   - **Guided Filter** (wariant self-guided) — lokalne dopasowanie liniowe z zachowaniem krawędzi na podstawie samej filtrowanej powierzchni

**Analiza dokładności** wyniku względem referencji natywnej:
   - **MAE** i **RMSE** — dokładność geometryczna
   - **CVA** (sygnatura skalowa) — zachowanie struktury przestrzennej (szorstkości) rzeźby terenu

## Główny wynik pracy
Porównano wpływ trzech metod resamplingu (najbliższy sąsiad, biliniowa, bikubiczna) oraz dwóch metod filtracji na dokładność geometryczną i wierność odwzorowania rzeźby terenu, dla trzech obszarów testowych o zróżnicowanej charakterystyce (Świnoujście, Sopot, Rzeszów). Filtracja adaptacyjna w większości przypadków **pogarszała** dokładność geometryczną względem referencji natywnej; wynik przeciwny do postawionej hipotezy, choć spójny z redukcją szorstkości terenu (CVA).

## Pliki
| Plik | Opis |
|---|---|
| `fp_filters.py` | Implementacja FPDEMS i Guided Filter |
| `analiza.py` | Obliczanie MAE, RMSE, CVA i generowanie raportów |

## Uruchomienie
Zależy od modułów w [`../core/`](../core/) — patrz `environment.yml` w katalogu głównym repozytorium.