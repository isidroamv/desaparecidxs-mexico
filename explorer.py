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
is_from_jalisco = df['fuerocomun_desapentidad'].str.contains("JALISCO")


def group_by_height(d):

    height_data = {}
    for val_key in d.iteritems():
        height = str(val_key[0])
        value = val_key[1]
        key = height[0:3]
        height_data[key] = height_data.get(key, 0) + value

    label = []
    values = []
    for key, value in height_data.items():
        label.append(key)
        values.append(value)
    
    return label, values

fd = df[is_feamale]['fuerocomun_estatura'].value_counts()
md = df[is_male]['fuerocomun_estatura'].value_counts()

flabel, fvalues = group_by_height(fd)
mlabel, mvalues = group_by_height(md)

# Generate Chart
colors = ['#3366cc','#dc3912','#ff9900','#109618','#990099',
 '#0099c6','#dd4477','#66aa00','#b82e2e','#316395',
 '#3366cc','#994499','#22aa99','#aaaa11','#6633cc',
 '#e67300','#8b0707','#651067','#329262','#5574a6',
 '#3b3eac','#b77322','#16d620','#b91383','#f4359e',
 '#9c5935','#a9c413','#2a778d','#668d1c','#bea413',
 '#0c5922','#743411']

# Female
fig1, ax1 = plt.subplots()
plt.title('Estatura de Mujeres desaparecidas en México')
ax1.pie(fvalues, labels=flabel, autopct='%1.1f%%', shadow=True, startangle=90, colors=colors)
ax1.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.
plt.show()

# Male
fig1, ax1 = plt.subplots()
plt.title('Estatura de Hombres desaparecidos en México')
ax1.pie(mvalues, labels=mlabel, autopct='%1.1f%%', shadow=True, startangle=90, colors=colors)
ax1.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.
plt.show()