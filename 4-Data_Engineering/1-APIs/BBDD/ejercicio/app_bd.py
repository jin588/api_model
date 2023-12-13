# import json
from flask import Flask, request, jsonify
# import sqlite3
import os

os.chdir(os.path.dirname(__file__))

app = Flask(__name__)
app.config["DEBUG"] = True

@app.route('/', methods=['GET'])
def welcome():
    return "Welcome to mi API conected to my books database"

# 0.Ruta para obtener todos los libros


# 1.Ruta para obtener el conteo de libros por autor ordenados de forma descendente


# 2.Ruta para obtener los libros de un autor como argumento en la llamada


# 3.Ruta para obtener los libros filtrados por título, publicación y autor

app.run()