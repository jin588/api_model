from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
import os
import pickle
from sklearn.linear_model import LinearRegression

dir_path = os.path.dirname(os.path.realpath(__file__))

app = Flask(__name__)
app.config['DEBUG'] = True
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///advertising.db'
db = SQLAlchemy(app)

class Sales(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    tv = db.Column(db.Float, nullable=False)
    radio = db.Column(db.Float, nullable=False)
    newspaper = db.Column(db.Float, nullable=False)
    sales = db.Column(db.Float, nullable=False)

@app.route("/", methods=['GET'])
def hello():
    return "API advertising"

@app.route('/v2/predict', methods=['GET'])
def predict():
    model = pickle.load(open(os.path.join(dir_path,"data","advertising_model"),'rb'))

    tv = request.args.get('tv', None)
    radio = request.args.get('radio', None)
    newspaper = request.args.get('newspaper', None)

    if tv is None or radio is None or newspaper is None:
        return "Missing args, the input values are needed to predict"
    else:
        prediction = model.predict([[float(tv),float(radio),float(newspaper)]])
        return "The prediction of sales investing that amount of money in TV, radio and newspaper is: " + str(round(prediction[0],2)) + 'k €'

@app.route('/v2/ingest_data', methods=['POST'])
def ingest_data():
    model = pickle.load(open(os.path.join(dir_path,"data","advertising_model"),'rb'))
    data = request.get_json()
    new_sale = Sales(tv=data['tv'], radio=data['radio'], newspaper=data['newspaper'], sales=data['sales'])
    db.session.add(new_sale)
    db.session.commit()
    return jsonify({'message': 'New data ingested successfully'})

@app.route('/v2/retrain', methods=['GET'])
def retrain():
    data = Sales.query.all()
    X = [[d.tv, d.radio, d.newspaper] for d in data]
    y = [d.sales for d in data]

    model = LinearRegression()
    model.fit(X, y)

    pickle.dump(model, open('data/advertising_model','wb'))

    return jsonify({'message': 'Model retrained successfully'})

if __name__ == '__main__':
    app.run()