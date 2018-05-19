import json
import csv
import numpy as np
import pandas as pd
import unidecode
import random

# Valores, localidad, genero, edad, #month

total_total = 119530753
states = {}
states_keys = []
age_ranges = ['00-04','05-09','10-14','15-19','20-24','25-29',
    '30-34','35-39','40-44','45-49','50-54','55-59','60-64',
    '70-74','75']

df = pd.read_csv('report_12_01_2018_2.csv')
total_records = len(df)
state_count = df['fuerocomun_desapentidad'].value_counts()
state_codes = json.load(open('mexico_code_v3.json'))


for i in range(32):
    key = "%02d" % (i + 1)
    for g in ('f','m'):
        for age_range in age_ranges:
            states_keys.append(key)
            states[key+'-'+g+'-'+age_range] = 0

with open('01_poblacion/02-Tabla1.csv', 'r') as file:
    spanreader = csv.reader(file, delimiter=',')
    for row in spanreader:
        state_key = row[0][0:2]
        age_range = row[1].split(' ')[0]
        is_valor = row[2] == 'Valor'
        total = row[3].replace(',','')
        male = row[4].replace(',','')
        female = row[5].replace(',','')

        try:
            state_key = int(state_key)
        except Exception:
            continue
        state_key = str(state_key)

        if is_valor and (age_range in age_ranges):
            states[state_key+'-f-'+age_range] = float(female) * 100 / total_total
            states[state_key+'-m-'+age_range] = float(male) * 100 / total_total

keys = []
probability = []
for s in states:
    keys.append(s)
    probability.append(states[s]/100)
err = 1 - sum(probability)
keys.append("err")
probability.append(err)

count = 0
index = [
    'fuerocomun_desapentidad',
    'fuerocomun_desapfecha',
    'fuerocomun_edad',
    'fuerocomun_sexo'
]
df_norm = pd.DataFrame([], columns=index)
while True:
    result = np.random.choice(keys, p=probability)

    if result == "err":
        continue

    result = result.split("-")

    if result[1] == 'f':
        gender_n = 0
    else:
        gender_n = 1
    

    if result[2] == '75':
        result.append('81')

    df_norm = df_norm.append({
        'fuerocomun_desapentidad': state_codes[result[0]]['val'],
        'fuerocomun_desapfecha': random.randint(1,12),
        'fuerocomun_edad': random.randint(int(result[2]), int(result[3])),
        'fuerocomun_sexo': gender_n,
        'desaparecido': 0
    }, ignore_index=True)

    count += 1
    if count == 127500:
        break




df_norm.to_csv('data/false_data.csv')