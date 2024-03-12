from flask import Flask, jsonify, request
from flask_mysqldb import MySQL

app = Flask(__name__)

# MySQL configuration
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'Jayraj@123'
app.config['MYSQL_DB'] = 'bookstore'

# Initialize MySQL
mysql = MySQL(app)

# Create books table if not exists
with app.app_context():
    cur = mysql.connection.cursor()
    cur.execute("""
        CREATE TABLE IF NOT EXISTS books (
            id INT AUTO_INCREMENT PRIMARY KEY,
            title VARCHAR(255) NOT NULL,
            author VARCHAR(255) NOT NULL,
            isbn VARCHAR(255) NOT NULL
        )
    """)
    mysql.connection.commit()


@app.route('/api/books', methods=['GET'])
def get_books():
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM books")
    books = cur.fetchall()

    cur.close()
    return jsonify(books)


@app.route('/api/books', methods=['POST'])
def add_book():
    data = request.json
    title = data.get('title')
    author = data.get('author')
    isbn = data.get('isbn')
    if title and author and isbn:
        cur = mysql.connection.cursor()
        cur.execute("INSERT INTO books (title, author, isbn) VALUES (%s, %s, %s)", (title, author, isbn))
        mysql.connection.commit()
        cur.close()
        return jsonify({'message': 'Book added successfully'}), 201
    else:
        return jsonify({'error': 'Missing required fields'}), 400


@app.route('/api/books/<int:book_id>', methods=['GET'])
def get_book(book_id):
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM books WHERE id = %s", (book_id,))
    book = cur.fetchone()
    cur.close()
    if book:
        return jsonify(book)
    else:
        return jsonify({'error': 'Book not found'}), 404


if __name__ == '__main__':
    app.run(debug=True)
