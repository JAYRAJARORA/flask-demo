from flask import Flask, jsonify, request
from pymongo import MongoClient
from bson.objectid import ObjectId

app = Flask(__name__)

# Connect to MongoDB
client = MongoClient('mongodb://localhost:27017/')
db = client['library_system']  # Database name
books_collection = db.books  # Books collection
authors_collection = db.authors  # Authors collection

@app.route('/books', methods=['POST'])
def create_book():
    book = request.json
    book['author_id'] = ObjectId(book['author_id'])  # Ensure ObjectID format
    books_collection.insert_one(book)
    return jsonify({'message': 'Book created successfully'}), 201

@app.route('/books', methods=['GET'])
def get_books():
    books = list(books_collection.find())
    for book in books:
        book['_id'] = str(book['_id'])
        book['author_id'] = str(book['author_id'])
    return jsonify(books), 200

@app.route('/books/<id>', methods=['GET'])
def get_book(id):
    book = books_collection.find_one({'_id': ObjectId(id)})
    if book:
        book['_id'] = str(book['_id'])
        book['author_id'] = str(book['author_id'])
        return jsonify(book), 200
    else:
        return jsonify({'message': 'Book not found'}), 404

@app.route('/books/<id>', methods=['PUT'])
def update_book(id):
    updated_data = request.json
    result = books_collection.update_one({'_id': ObjectId(id)}, {'$set': updated_data})
    if result.matched_count:
        return jsonify({'message': 'Book updated successfully'}), 200
    else:
        return jsonify({'message': 'Book not found'}), 404

@app.route('/books/<id>', methods=['DELETE'])
def delete_book(id):
    result = books_collection.delete_one({'_id': ObjectId(id)})
    if result.deleted_count:
        return jsonify({'message': 'Book deleted successfully'}), 200
    else:
        return jsonify({'message': 'Book not found'}), 404

@app.route('/authors/book-count', methods=['GET'])
def authors_books_count():
    # Aggregation example: Count the number of books each author has written
    pipeline = [
        {"$group": {"_id": "$author_id", "count": {"$sum": 1}}},
        {"$sort": {"count": -1}},  # Optional: sort by count in descending order
    ]
    counts = list(books_collection.aggregate(pipeline))
    for count in counts:
        count['_id'] = str(count['_id'])  # Convert ObjectId to string
    return jsonify(counts), 200

@app.route('/books/author-details', methods=['GET'])
def books_authors_details():
    # Lookup example: Fetch books along with their author details
    pipeline = [
        {"$lookup": {
            "from": "authors",
            "localField": "author_id",
            "foreignField": "_id",
            "as": "author_details"
        }}, {"$project": { "author_id": 0 }}
    ]
    books = list(books_collection.aggregate(pipeline))
    for book in books:
        book['_id'] = str(book['_id'])
        if 'author_details' in book and book['author_details']:
            for author in book['author_details']:
                author['_id'] = str(author['_id'])

    print('-------------')
    print(books)
    print('------------')
    return jsonify(books), 200


@app.route('/authors', methods=['POST'])
def create_author():
    author = request.json
    authors_collection.insert_one(author)
    return jsonify({'message': 'Author created successfully'}), 201


if __name__ == '__main__':
    app.run(debug=True)
