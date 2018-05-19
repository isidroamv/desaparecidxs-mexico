import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn import linear_model
from sklearn.externals import joblib
import pickle

a = pd.read_csv('data/false_data.csv')
b = pd.read_csv('data/true_data.csv')
df = a.append(b)

print("df", len(df))
df = df.sample(frac=1).reset_index(drop=True)

#['fuerocomun_desapentidad' 'fuerocomun_desapfecha' 'fuerocomun_edad' 'fuerocomun_sexo' 'desaparecido']
Y = (df['desaparecido'] == 1.).as_matrix()
X = df.drop(['Unnamed: 0', 'desaparecido'], axis=1).as_matrix()

h = .02  # step size in the mesh

logreg = linear_model.LogisticRegression(C=1e5)
logreg.fit(X, Y)
# TODO:
# obtener el valor que representa el porcentaje, multiplicarlo por 100 y 
# dividirlo entre la cantidad de habitantantes por estado
Z = logreg.predict_proba([[13.646671118724775, 1, 22, 0]])
joblib.dump(logreg, 'data/pickle.pkl')
exit()

# we create an instance of Neighbours Classifier and fit the data.
Z = logreg.predict_proba(b.drop(['Unnamed: 0', 'desaparecido'], axis=1).as_matrix())
Z = logreg.predict(b.drop(['Unnamed: 0', 'desaparecido'], axis=1).as_matrix())
fi = (b[Z]['fuerocomun_sexo'] == 0.).as_matrix()
print("d", b[Z])