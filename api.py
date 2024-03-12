from flask import Flask, jsonify, request, redirect, url_for

app = Flask(__name__)

# Sample list of books (list of dictionaries)
books = [
    {'title': 'To Kill a Mockingbird', 'author': 'Harper Lee', 'isbn': '9780061120084'},
    {'title': '1984', 'author': 'George Orwell', 'isbn': '9780451524935'},
    {'title': 'The Great Gatsby', 'author': 'F. Scott Fitzgerald', 'isbn': '9780743273565'},
    {'title': 'The Catcher in the Rye', 'author': 'J.D. Salinger', 'isbn': '9780316769488'},
    {'title': 'Brave New World', 'author': 'Aldous Huxley', 'isbn': '9780060850524'},
    {'title': 'To Kill a Mockingbird', 'author': 'Harper Lee', 'isbn': '9780061120084'},
    {'title': 'The Lord of the Rings', 'author': 'J.R.R. Tolkien', 'isbn': '9780618645619'},
]


@app.route('/api/books', methods=['GET'])
def get_books():
    # Get query parameters for authors
    authors = request.args.getlist('author')
    if authors:
        # Filter books by authors if authors are specified
        result = [book for book in books if book['author'] in authors]
    else:
        # Return all books if no authors are specified
        result = books

    return jsonify(result)


@app.route('/api/books', methods=['POST'])
def add_book():
    data = request.json
    title = data.get('title')
    author = data.get('author')
    isbn = data.get('isbn')
    if title and author and isbn:
        new_book = {'title': title, 'author': author, 'isbn': isbn}
        books.append(new_book)
        return jsonify({'message': 'Book added successfully'}), 201
    else:
        return jsonify({'error': 'Missing required fields'}), 400


@app.route('/api/books/<isbn>', methods=['GET'])
def get_book(isbn):
    # Find the book with the specified ISBN
    book = None
    for b in books:
        if b['isbn'] == isbn:
            book = b
            break
    if book:
        return jsonify(book)
    else:
        return jsonify({'error': 'Book not found'}), 404


if __name__ == '__main__':
    app.run(debug=True)
