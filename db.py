from flask import Flask, jsonify, request, make_response, session, redirect, url_for
from flask_mysqldb import MySQL

app = Flask(__name__)

# Secret key for session management
app.secret_key = 'your_secret_key'

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


@app.route('/api/login', methods=['POST'])
def login():
    app.logger.debug(request.json)
    if request.json.get('username') == 'admin' and request.json.get('password') == 'password':
        # Set a cookie to store user information
        response = make_response(jsonify({'message': 'Login successful'}), 200)
        response.set_cookie('username', 'admin')
        app.logger.debug(url_for('get_books'))
        return response
    else:
        return jsonify({'error': 'Invalid credentials'}), 401


@app.route('/api/logout', methods=['POST'])
def logout():
    # Clear the cookie
    response = make_response(jsonify({'message': 'Logout successful'}), 200)
    response.set_cookie('username', '', expires=0)
    return response


@app.route('/api/books', methods=['GET'])
def get_books():
    if 'username' not in request.cookies:
        return jsonify({'error': "Unauthorized Access"}), 401
    username = request.cookies.get('username')
    app.logger.debug(username)
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM books")
    books = cur.fetchall()

    cur.close()
    return jsonify(books)


@app.route('/api/books', methods=['POST'])
def add_book():
    if 'username' not in request.cookies:
        return jsonify({'error': "Unauthorized Access"}), 401
    username = request.cookies.get('username')
    app.logger.debug(username)
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
    if 'username' not in request.cookies:
        return jsonify({'error': "Unauthorized Access"}), 401
    username = request.cookies.get('username')
    app.logger.debug(username)
    if not session.get('logged_in'):
        return jsonify({'error': 'Unauthorized access'}), 401
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM books WHERE id = %s", (book_id,))
    book = cur.fetchone()
    cur.close()
    if book:
        return jsonify(book)
    else:
        return jsonify({'error': 'Book not found'}), 404


@app.route('/api/add-to-cart', methods=['GET'])
def add_to_cart():
    data = request.args
    book_id = data.get('book_id')
    quantity = int(data.get('quantity', 1))
    if book_id:
        # Initialize cart if not exists
        if 'cart' not in session:
            session['cart'] = {}
        app.logger.debug(book_id)
        app.logger.debug(type(book_id))
        app.logger.debug(session)
        # Add book to cart
        if book_id in session['cart']:
            session['cart'][book_id] += quantity
        else:
            session['cart'][book_id] = quantity
        app.logger.debug(session['cart'][book_id])

        return jsonify({'message': 'Book added to cart successfully'}), 200
    else:
        return jsonify({'error': 'Missing book_id parameter'}), 400


@app.route('/api/cart', methods=['GET'])
def view_cart():
    cart = session.get('cart', {})
    cart_info = []

    if cart:
        # Fetch book details from database
        cur = mysql.connection.cursor()
        for book_id, quantity in cart.items():
            cur.execute("SELECT * FROM books WHERE id = %s", (book_id,))
            book = cur.fetchone()
            if book:
                cart_info.append({'id': int(book_id), 'title': book[1], 'author': book[2], 'isbn': book[3], 'quantity': quantity})
        cur.close()

    return jsonify(cart_info), 200


if __name__ == '__main__':
    app.run(debug=True)
