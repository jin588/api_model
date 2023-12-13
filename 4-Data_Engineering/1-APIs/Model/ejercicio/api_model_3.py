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


@app.route('/v2/predict', methods=['GET'])
def predict():
    model = pickle.load(open('data/advertising_model','rb'))

    tv = request.args.get('tv', None)
    radio = request.args.get('radio', None)
    newspaper = request.args.get('newspaper', None)

    if tv is None or radio is None or newspaper is None:
        return "Faltan argumentos"
    else:
        prediction = model.predict([[int(tv),int(radio),int(newspaper)]])
        return "La predicción de ventas invirtiendo esa cantidad de dinero en TV, radio y periódico es: " + str(round(prediction[0],2)) + 'k €'

@app.route('/v2/ingest_data', methods=['POST'])
def ingest_data():
    tv = request.args.get('tv', None)
    radio = request.args.get('radio', None)
    newpaper = request.args.get('newpaper', None)
    sales = request.args.get('sales', None)
   
    connection = sqlite3.connect('ejercicio.db')
    cursor = connection.cursor()

    cursor.execute('''
        INSERT INTO Advertising (TV, radio, newpaper, sales)
        VALUES (?, ?, ?, ?)
    ''', (tv, radio, newpaper, sales))

    connection.commit()
    connection.close()

    return jsonify({'message': 'Datos guardados correctamente.'}), 201

@app.route('/v2/retrain', methods=['GET'])
def retrain_model():
    connection = sqlite3.connect('ejercicio.db')

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