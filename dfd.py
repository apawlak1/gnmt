import pandas as pd

# 1. Wczytanie pliku CSV
file_path = "C:\Users\strze\Desktop\SKOROWIDZE\NMT2019_AMS.csv"
df = pd.read_csv(file_path)

# 2. Filtrowanie wierszy, gdzie kolumna 'format' ma wartość 'ASCII NMT'
filtered_df = df[df["format"] == "ASCII NMT"]

# 3. Wyświetlenie wybranych kolumn (np. id, godlo, format, url_do_pobrania)
cols_to_show = ["id", "godlo", "format", "url_do_pobrania"]
print(filtered_df[cols_to_show])

# 4. (Opcjonalnie) Zapis wyfiltrowanych danych do nowego pliku CSV
filtered_df.to_csv("NMT_ASCII_filtered.csv", index=False)
print(f"\nZnaleziono {len(filtered_df)} wierszy.")