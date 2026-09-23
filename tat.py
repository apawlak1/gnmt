# -*- coding: utf-8 -*-
import numpy as np
import rasterio

sciezka=input('Podaj sciezke do rastra: ').strip().strip('"')

with rasterio.open(sciezka) as src:
    dane=src.read(1).astype('float64')
    nodata=src.nodata

if nodata is not None:
    if np.isnan(nodata):
        wazne=dane[~np.isnan(dane)]
    else:
        wazne=dane[dane != nodata]
else:
    wazne=dane[~np.isnan(dane)]

if wazne.size == 0:
    print('Brak wazynch danych w rastrze.')
else:
    srednia=np.mean(wazne)
    mediana=np.median(wazne)
    rms=np.sqrt(np.mean(wazne ** 2))

    print(f'Plik: {sciezka}')
    print(f'n_px    = {wazne.size}')
    print(f'srednia = {srednia:.3f}')
    print(f'mediana = {mediana:.3f}')
    print(f'RMS     = {rms:.3f}')