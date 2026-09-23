
import os
from pathlib import Path
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

#USTAWIENIE ARIAL
plt.rcParams["font.family"] = "sans-serif"
plt.rcParams["font.sans-serif"] = ["Arial"]

csv_folder = r"C:\Users\strze\Desktop\SKOROWIDZE"

lata = [str(rok) for rok in range(2018, 2027)]

folder = Path(csv_folder)
pliki_csv = list(folder.glob("*.csv"))

# Nazwy kolumn w csv
kolumna_rok = "akt_rok"
kolumna_format = "format"

ramki = []
for f in pliki_csv:
    try:
        df_temp = pd.read_csv(f, sep=",", dtype=str)
        ramki.append(df_temp)
    except Exception as e:
        print(f"NIE WCZYTANO: {f.name}: {e}")

#lacze w 1 tabele i usuwam ewentualne spacje
df = pd.concat(ramki, ignore_index=True)
df.columns = df.columns.str.strip()

#ujednolicam kolumny na txt i wielkie litery
df[kolumna_rok] = df[kolumna_rok].astype(str).str.strip()
df[kolumna_format] = df[kolumna_format].astype(str).str.strip().str.upper()

df = df[df[kolumna_rok].isin(lata)]

#LICZBA REKORDOW I UDZIAL PROCENTOWY
laczna_liczba_rekordow = len(df)

print("\n" + "=" * 60)
print(f"ŁĄCZNA LICZBA REKORDÓW (2018–2026): {laczna_liczba_rekordow}")
print("=" * 60)

#zliczanie wystapien i udzialu
stats_formaty = df[kolumna_format].value_counts().reset_index()
stats_formaty.columns = ["Format", "Liczba_rekordow"]
stats_formaty["Udzial_procentowy"] = (
    stats_formaty["Liczba_rekordow"] / laczna_liczba_rekordow
) * 100

for _, row in stats_formaty.iterrows():
    print(
        f"Format: {row['Format']:<30} | Liczba: {row['Liczba_rekordow']:<6} | Udzial: {row['Udzial_procentowy']:.2f}%"
    )
print("=" * 60 + "\n")

df_counts = (
    df.groupby([kolumna_rok, kolumna_format])
    .size()
    .unstack(fill_value=0)
    .reindex(lata, fill_value=0)
)
df_counts_masked = df_counts.replace(0, np.nan)

#WYKRES
plt.figure(figsize=(6, 4), dpi=300)

for format_nazwa in df_counts_masked.columns:
    plt.plot(
        df_counts_masked.index,
        df_counts_masked[format_nazwa],
        marker="o",
        markersize=4,  #tu zmniejszam kropki
        linewidth=1,
        label=format_nazwa,
    )

plt.title("Liczba plików w danych formatach w latach 2018–2026", fontsize=12, pad=12)
plt.xlabel("Rok", fontsize=9)
plt.ylabel("Liczba plików", fontsize=9)
plt.xticks(rotation=60, ha="right")

plt.grid(True, linestyle="--", alpha=0.5)

plt.legend(
    title="Format pliku",
    fontsize=7,  # Mniejszy tekst
    title_fontsize=9,  # Mniejszy tytuł legendy
    markerscale=0.7,  # <-- Mniejsze kropki wewnątrz legendy
    loc="upper left",
    frameon=True,)

plt.tight_layout()

plt.savefig(folder / "wykres_formatow_2018_2026.png", dpi=300)
print(f"[SUCCESS] Wykres zapisany w: {folder / 'wykres_formatow_2018_2026.png'}")
plt.show()
