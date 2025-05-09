import pandas as pd
import glob
import os

file_list = glob.glob('datasets/data-in/*.xls')

output_folder = 'datasets/data-out'
os.makedirs(output_folder, exist_ok=True)
output_path = os.path.join(output_folder, 'superenalotto_unito.csv')

# Lista per accumulare i dataframe
df_list = []

for file in file_list:
    # Trova la riga con intestazioni
    temp_df = pd.read_excel(file, engine='xlrd')
    header_row = None
    for i, row in enumerate(temp_df.iloc[:, 0]):
        if 'Data' in str(row):
            header_row = i
            break

    # Ricarica saltando le righe inutili
    df = pd.read_excel(file, skiprows=header_row + 1, engine='xlrd', names=[
        'Data', 'Giorno', 'N1', 'N2', 'N3', 'N4', 'N5', 'N6', 'Jolly', 'Superstar'
    ])
    df = df.dropna(subset=['Data'])
    df = df[df['Data'] != 'Data']
    df[['N1', 'N2', 'N3', 'N4', 'N5', 'N6', 'Jolly', 'Superstar']] = df[['N1', 'N2', 'N3', 'N4', 'N5', 'N6', 'Jolly', 'Superstar']].apply(pd.to_numeric, errors='coerce')
    df['Data'] = pd.to_datetime(df['Data'], errors='coerce')
    
    df_list.append(df)

# Unisci tutti i dataframe
df_total = pd.concat(df_list, ignore_index=True)

#print(df_total.head())

# salva
df_total.to_csv(output_path, index=False)
print(f"File salvato in: {output_path}")