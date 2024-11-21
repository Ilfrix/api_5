from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow

# Инициализация приложения
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///books.db'  # Используем SQLite для простоты
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Инициализация базы данных и сериализатора
db = SQLAlchemy(app)
ma = Marshmallow(app)

# Модель книги
class Book(db.Model):
    id = db.Column(db.String, primary_key=True)
    title = db.Column(db.String, nullable=False)
    author = db.Column(db.String, nullable=False)
    # published_date = db.Column(db.String, nullable=False)
    price = db.Column(db.Float, nullable=False)

    def __init__(self, id, title, author, price):
        self.id = id
        self.title = title
        self.author = author
        # self.published_date = published_date
        self.price = price

# Схема для сериализации книги
class BookSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Book

# Инициализация базы данных
with app.app_context():
    db.create_all()

# Эндпоинты API
@app.route('/books', methods=['GET'])
def get_books():
    books = Book.query.all()
    book_schema = BookSchema(many=True)
    return jsonify(book_schema.dump(books))

@app.route('/books', methods=['POST'])
def add_book():
    data = request.json
    new_book = Book(**data)
    db.session.add(new_book)
    db.session.commit()
    book_schema = BookSchema()
    return jsonify(book_schema.dump(new_book)), 201

@app.route('/books/<string:book_id>', methods=['GET'])
def get_book(book_id):
    book = Book.query.get(book_id)
    if book is None:
        return jsonify({"message": "Книга не найдена"}), 404
    book_schema = BookSchema()
    return jsonify(book_schema.dump(book))

@app.route('/books/<string:book_id>', methods=['PUT'])
def update_book(book_id):
    book = Book.query.get(book_id)
    if book is None:
        return jsonify({"message": "Книга не найдена"}), 404

    data = request.json
    for key, value in data.items():
        setattr(book, key, value)

    db.session.commit()
    book_schema = BookSchema()
    return jsonify(book_schema.dump(book))

@app.route('/books/<string:book_id>', methods=['DELETE'])
def delete_book(book_id):
    book = Book.query.get(book_id)
    if book is None:
        return jsonify({"message": "Книга не найдена"}), 404

    db.session.delete(book)
    db.session.commit()
    return '', 204

# Запуск приложения
if __name__ == '__main__':
    app.run(debug=True)
