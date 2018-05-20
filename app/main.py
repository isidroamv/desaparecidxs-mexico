import os
import json
import datetime
from sklearn.externals import joblib
from flask import Flask, render_template, request, send_from_directory, request

clf = joblib.load('app/pickle.pkl') 

cwd = os.getcwd()
app = Flask(__name__, static_url_path='')
 
@app.route('/')
def index(user=None):
    user = user or 'Shalabh'
    return render_template('desaparecidos.html', user=user)

@app.route('/', methods=['POST'])
def result():
    age = request.form['age']
    gender = request.form['gender']
    date = request.form['date']
    state_index = request.form['state']
    
    with open(cwd+'/app/states.json') as f:
        states = json.loads(f.read())

    state_val = states[state_index]['val']
    gender = int(gender)
    age = int(age)
    month = int(date.split('-')[1])

    Z = clf.predict_proba([[state_val, month, age, gender]])
    print("Z", Z[0][1])
    predict = Z[0][1]

    if predict > 0.65:
        message = "La probabilidad que seas desaparecido es alta"
        level = 6
    elif predict > 0.5:
        message = "La probabilidad que seas desaparecido es media alta"
        level = 5
    elif predict > 0.4:
        message = "La probabilidad que seas desaparecido es media"
        level = 4
    elif predict > 0.3:
        message = "La probabilidad que seas desaparecido es media baja"
        level = 3
    elif predict >= 0.1:
        message = "La probabilidad que seas desaparecido es baja"
        level = 2
    elif predict < 0.1:
        message = "La probalidad que seas desaparecido es muy baja"
        level = 1

    return render_template('desaparecidos.html', predict=predict, message=message, level=level)

@app.route('/static/<path:path>')
def send_static(path):
    return send_from_directory('static', path)


if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)