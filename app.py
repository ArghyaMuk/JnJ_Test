from flask import Flask, request, jsonify
from database import db, Book

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///books.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)

with app.app_context():
    db.create_all()


@app.route('/books', methods=['GET', 'POST', 'PUT', 'DELETE'])
def book_details():
    if request.method == 'GET':
        books = Book.query.all()
        return jsonify([book.to_dict() for book in books]), 200

    elif request.method == 'POST':
        data = request.get_json()
        new_book = Book(title=data['title'], author=data['author'])
        db.session.add(new_book)
        db.session.commit()
        return jsonify(new_book.to_dict()), 201

    elif request.method == 'PUT':
        data = request.get_json()
        book = Book.query.get(data['id'])
        if book:
            book.title = data['title']
            book.author = data['author']
            db.session.commit()
            return jsonify(book.to_dict()), 200
        else:
            return jsonify({'message': 'Book not found'}), 404

    elif request.method == 'DELETE':
        data = request.get_json()
        book = Book.query.get(data['id'])
        if book:
            db.session.delete(book)
            db.session.commit()
            return jsonify({'message': 'Book deleted'}), 200
        else:
            return jsonify({'message': 'Book not found'}), 404

    else:
        return jsonify({'message': 'Method not allowed'}), 405


if __name__ == '__main__':
    app.run(debug=True)