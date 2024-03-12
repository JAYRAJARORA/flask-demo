from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)

# Sample list of books (list of dictionaries)
books = [
    {'title': 'Book 1', 'author': 'Author 1', 'isbn': '1234567890'},
    {'title': 'Book 2', 'author': 'Author 2', 'isbn': '0987654321'}
]


@app.route('/')
def home():
    return render_template('home.html', books=books)


@app.route('/add_book', methods=['GET', 'POST'])
def add_book():
    if request.method == 'POST':
        title = request.form['title']
        author = request.form['author']
        isbn = request.form['isbn']
        # Create a new book dictionary
        new_book = {'title': title, 'author': author, 'isbn': isbn}
        # Add the new book to the list of books
        books.append(new_book)
        # Redirect to the home page after adding the book
        return redirect(url_for('home'))
    return render_template('add_book.html')


if __name__ == '__main__':
    app.run(debug=True)
