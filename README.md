# geo_nmt

**„Inteligentna optymalizacja i generalizacja wieloczasowych zbiorów NMT w środowisku Python”**
Aleksandra Pawlak, Politechnika Gdańska

## Funkcje
1. **Pobieranie i scalanie arkuszy NMT**: automatyczne pobieranie z danych PZGiK i łączenie w spójną mozaikę (wykorzystuje core/)
2. **Generalizacja blokowa**: resampling realizowany blokami zamiast wczytywania całego obszaru naraz, co pozwala przetwarzać duże obszary bez nadmiernego zużycia pamięci
3. **Zapis do formatu Zarr**: wynik zapisywany jest jako store Zarr z wymiarem czasu; kolejne aktualizacje danych (nowy nalot/rok) dokładane są jako nowa "warstwa" zamiast tworzenia kolejnego, osobnego pliku
 4. **Dane wieloczasowe**: jeden store obejmuje wiele dat dla tego samego obszaru, gotowy do dalszej analizy bez wczytywania całości do pamięci


## Dla kogo?
Narzędzie ogranicza ręczną pracę przy przetwarzaniu wielu dat naraz. Użytkownik podaje obszar, zakres czasu i docelową rozdzielczość, a na wyjściu otrzymuje gotowy, przeszukiwalny store Zarr, zamiast osobno pobierać, scalać i generalizować dane dla każdej daty z osobna.


## Pliki


## Uruchomienie
Zależy od modułów w [`../core/`](../core/) — patrz `environment.yml` w katalogu głównym repozytorium.