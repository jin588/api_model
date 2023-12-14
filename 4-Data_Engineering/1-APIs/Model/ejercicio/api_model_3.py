import pandas as pd
import sqlite3
import os
import pickle
from flask import Flask, request, jsonify

os.chdir(os.path.dirname(__file__))

app = Flask(__name__)
app.config['DEBUG'] = True

@app.route("/", methods=['GET'])
def hello():
    return "Bienvenido a mi API del modelo advertising"

@app.route('/predict', methods=['GET'])
def predict():
    model = pickle.load(open('data/advertising_model','rb'))

    data = request.get_json().get('data', None)

    if data is None:
        return "Faltan argumentos"
    else:
        tv, radio, newspaper = data[0]
        prediction = model.predict([[float(tv),float(radio),float(newspaper)]])
        return jsonify({"prediction": str(round(prediction[0],2)) + 'k €'})
    
@app.route('/ingest', methods=['POST'])
def ingest_data():
    tv = request.args.get('tv', 0)
    radio = request.args.get('radio', 0)
    newpaper = request.args.get('newpaper', 0)
    sales = request.args.get('sales', 0)
   
    connection = sqlite3.connect('ejercicio4.db')
    cursor = connection.cursor()

    cursor.execute('''
        INSERT INTO Advertising (TV, radio, newpaper, sales)
        VALUES (?, ?, ?, ?)
    ''', (tv, radio, newpaper, sales))

    connection.commit()
    connection.close()

    return jsonify({'message': 'Datos ingresados correctamente'}), 200

@app.route('/retrain', methods=['POST'])
def retrain_model():
    connection = sqlite3.connect('ejercicio4.db')

    query = 'SELECT TV, radio, newpaper, sales FROM Advertising'
    data = pd.read_sql_query(query, connection)
    connection.close()

    X = data[['TV', 'radio', 'newpaper']]
    y = data['sales']

    model = pickle.load(open('data/advertising_model','rb'))
    new_model = model.fit(X, y)

    # Guardar el nuevo modelo
    pickle.dump(new_model, open('data/advertising_model', 'wb'))

    return jsonify({'message': 'Modelo reentrenado correctamente.'}), 200

app.run()