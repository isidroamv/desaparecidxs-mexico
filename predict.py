from sklearn.externals import joblib
clf = joblib.load('app/pickle.pkl') 
Z = clf.predict_proba([[13.646671118724775, 1, 22, 1]])
print('Z', Z)