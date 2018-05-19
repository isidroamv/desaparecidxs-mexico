import pandas as pd
import json
import unidecode
import math
import numpy as np

#http://cedoc.inmujeres.gob.mx/documentos_download/100774.pdf


state_codes = json.load(open('mexico_code.json'))

def normalize_data(records):
    index = [
        'fuerocomun_desapentidad',
        'fuerocomun_desapfecha',
        'fuerocomun_edad',
        'fuerocomun_sexo'
    ]
    df_norm = pd.DataFrame([], columns=index)
    total_records = len(records)
    state_count = records['fuerocomun_desapentidad'].value_counts()
    
    records['fuerocomun_edad'] = pd.to_numeric(records['fuerocomun_edad'], errors='coerce')
    default_age = records['fuerocomun_edad'].mean(skipna=True)
    

    for record_key, record_val in records.iterrows():
        
        # State validation
        fuerocomun_desapentidad = 0
        for state_name, state_val in state_count.iteritems():
            if records.iloc[record_key]['fuerocomun_desapentidad'] in state_name:
                value = state_val * 100 / total_records
                fuerocomun_desapentidad = value
                break
        
        # get month
        date_splited = records.iloc[record_key]['fuerocomun_desapfecha'].split('/')
        try:
            fuerocomun_desapfecha = int(date_splited[1])
        except IndexError:
            fuerocomun_desapfecha = 5

        # get age
        if math.isnan(records.iloc[record_key]['fuerocomun_edad']):
            fuerocomun_edad = default_age
        else:
            fuerocomun_edad = records.iloc[record_key]['fuerocomun_edad']

        # Gender
        if records.iloc[record_key]['fuerocomun_sexo'] == "MUJER":
            fuerocomun_sexo = 0
        else:
            fuerocomun_sexo = 1

        df_norm = df_norm.append({
            'fuerocomun_desapentidad': fuerocomun_desapentidad,
            'fuerocomun_desapfecha': fuerocomun_desapfecha,
            'fuerocomun_edad': fuerocomun_edad,
            'fuerocomun_sexo': fuerocomun_sexo
        }, ignore_index=True)

    return df_norm

def normalize_gender(records):
    for key, name in records.iteritems():
        if name == "MUJER":
            records[key] = 0
        else:
            records[key] = 1
    return records


# edad, genero, mes, estatura, estado, 
df = pd.read_csv('report_12_01_2018_2.csv')
# df.loc[df.index[0], 'fuerocomun_desapentidad'] = '123'
# print(df.iloc[0]['fuerocomun_desapentidad'])
# exit()
df = normalize_data(df)
df['desaparecido'] = np.ones(len(df))
#df['fuerocomun_sexo'] = normalize_gender(df['fuerocomun_sexo'])
df.to_csv('data/true_data.csv')
print(df.head(10))

