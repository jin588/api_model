import json
from flask import Flask, request, jsonify
import sqlite3
import os
from flask import Flask, jsonify
from flask_sqlalchemy import SQLAlchemy



os.chdir(os.path.dirname(__file__))

app = Flask(__name__)
app.config["DEBUG"] = True
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///books.db'
db = SQLAlchemy(app)

class Book(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(80), nullable=False)
    author = db.Column(db.String(80), nullable=False)
    publication_year = db.Column(db.Integer, nullable=False)

@app.route('/', methods=['GET'])
def welcome():
    return "Welcome to mi API conected to my books database"

# 0.Ruta para obtener todos los libros

@app.route('/books', methods=['GET'])
def get_all_books():
    books = Book.query.all()
    return jsonify([book.serialize for book in books])

# 1.Ruta para obtener el conteo de libros por autor ordenados de forma descendente

@app.route('/books/count', methods=['GET'])
def get_author_book_count():
    counts = db.session.query(Book.author, db.func.count(Book.id)).group_by(Book.author).all()
    return jsonify(counts)
# 2.Ruta para obtener los libros de un autor como argumento en la llamada

@app.route('/books/<author>', methods=['GET'])
def get_books_by_author(author):
    books = Book.query.filter_by(author=author).all()
    return jsonify([book.serialize for book in books])

# 3.Ruta para obtener los libros filtrados por título, publicación y autor
@app.route('/books/filter', methods=['GET'])
def get_filtered_books():
    title = request.args.get('title')
    author = request.args.get('author')
    publication_year = request.args.get('publication_year')
    query = db.session.query(Book)
    if title:
        query = query.filter(Book.title.contains(title))
    if author:
        query = query.filter(Book.author == author)
    if publication_year:
        query = query.filter(Book.publication_year == publication_year)
    books = query.all()
    return jsonify([book.serialize for book in books])

if __name__ == '__main__':
    app.run()