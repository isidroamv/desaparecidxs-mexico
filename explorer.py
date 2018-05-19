import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.gridspec import GridSpec
import matplotlib.pyplot as plt
import numpy as np
import json
import unidecode


#http://cedoc.inmujeres.gob.mx/documentos_download/100774.pdf

df = pd.read_csv('report_12_01_2018_2.csv')

# Convert types
df['fuerocomun_edad'] = pd.to_numeric(df['fuerocomun_edad'], errors='signed')
df['fuerocomun_estatura'] = pd.to_numeric(df['fuerocomun_estatura'], errors='signed')

# Boolean form
is_greaterto20 = df['fuerocomun_edad'] > 19
is_lowerto30 = df['fuerocomun_edad'] < 30
is_custom = (df['fuerocomun_edad'] > 45)
is_feamale = df['fuerocomun_sexo'] == 'MUJER'
is_male = df['fuerocomun_sexo'] == 'HOMBRE'
is_slim = df['fuerocomun_complexion'] == 'Robusta'
is_incomplete = df['identificado'] == 'incompleto'
is_from_jalisco = df['fuerocomun_desapfecha'].str.contains("/2012")

df['fuerocomun_desapfecha'] = pd.to_datetime(df['fuerocomun_desapfecha'], format='%d/%m/%Y', utc=True, errors='coerce')

df = df[is_from_jalisco]
# Count records by year
keys = {}
labels = []
for i in range(12):
    key = "%02d" % (i + 1)
    labels.append(key)
    keys[key] = 0


weekday_list = {}
for i in range(7):
    weekday_list[str(i)] = 0
for el in df['fuerocomun_desapfecha']:
    weekday = el.weekday()
    if type(weekday) is int:
        weekday_list[str(weekday)] += 1

print("weekday", weekday_list)
exit()

sum_total = len(df)
print("total", sum_total)

values = []
values2 = []
for k in keys:
    kdformat = '/'+k+'/'
    df_filtered = df['fuerocomun_desapfecha'].str.contains(kdformat)
    #print(df[df_filtered]['fuerocomun_desapfecha'])
    df_filtered2 = df['fuerocomun_desapfecha'].str.contains('2015') 
    total = len(df[df_filtered])
    values.append(total)
    values2.append(total * 100 / sum_total)
    print("len", k, total * 100 / sum_total)

# Generate Chart
colors = ['#3366cc','#dc3912','#ff9900','#109618','#990099',
 '#0099c6','#dd4477','#66aa00','#b82e2e','#316395',
 '#3366cc','#994499','#22aa99','#aaaa11','#6633cc',
 '#e67300','#8b0707','#651067','#329262','#5574a6',
 '#3b3eac','#b77322','#16d620','#b91383','#f4359e',
 '#9c5935','#a9c413','#2a778d','#668d1c','#bea413',
 '#0c5922','#743411']
months = ["Enero", "Febrero", "Marzo", "Abril", "Mayo", "Junio", "Julio",
    "Julio", "Agosto", "Septiembre", "Noviembre", "Diciembre"]

 # Show Chart
plt.scatter(labels, values, values, c=colors, alpha=0.4)
plt.grid(color='#D3D3D3', linestyle='-', linewidth=1)
plt.xticks(labels)
plt.title("Desaparecidos por mes")
for i, txt in enumerate(months):
    plt.annotate(str(txt), (labels[i], values[i]))

plt.show()