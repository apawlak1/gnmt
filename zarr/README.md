# geo_nmt — wersja konferencyjna

Ta wersja została zaprezentowana na konferencji/seminarium naukowym:
**„Inteligentna optymalizacja i generalizacja wieloczasowych zbiorów NMT w środowisku Python”**
Aleksandra Pawlak, Politechnika Gdańska


## Dla kogo
Narzędzie ogranicza ręczną pracę przy przetwarzaniu wielu dat naraz — użytkownik podaje obszar, zakres czasu i docelową rozdzielczość, a na wyjściu otrzymuje gotowy, przeszukiwalny store Zarr, zamiast osobno pobierać, scalać i generalizować dane dla każdej daty z osobna.

## Stan projektu
Narzędzie działa i jest używane, natomiast **nie zostały jeszcze przeprowadzone formalne pomiary porównawcze** (np. rozmiar plików czy czas dostępu Zarr względem GeoTIFF) — to jeden z kierunków dalszego rozwoju.

## Pliki
| Plik | Opis |
|---|---|
| `zarr_writer.py` | Zapis zgeneralizowanych danych do formatu Zarr z osią czasu |

## Uruchomienie
Zależy od modułów w [`../core/`](../core/) — patrz `environment.yml` w katalogu głównym repozytorium.