from flask import Flask, request, jsonify
from flask_mysqldb import MySQL
import redis
import json

app = Flask(__name__)

# MySQL configurations
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'Jayraj@123'
app.config['MYSQL_DB'] = 'flask_app'
app.config['MYSQL_HOST'] = 'localhost'
mysql = MySQL(app)

# Redis configurations
redis_cache = redis.StrictRedis(host='localhost', port=6379, db=0, decode_responses=True)

@app.route('/items', methods=['GET'])
def get_items():
    # Attempt to load all item IDs from Redis set
    item_ids = redis_cache.smembers("item_ids")
    
    if item_ids:
        # Cache hit, load each item details from hash map
        items = []
        for item_id in item_ids:
            item_data = redis_cache.hgetall(f"item:{item_id}")
            items.append(item_data)
        app.logger.debug("Coming from the cache")
        return jsonify(items), 200
    
    # Cache miss, query the database
    cur = mysql.connection.cursor()
    cur.execute("SELECT id, name, description FROM items")
    rows = cur.fetchall()
    cur.close()
    
    items = []
    for row in rows:
        # Convert each item to a dictionary
        item_id, name, description = row
        item_data = {'id': item_id, 'name': name, 'description': description}
        items.append(item_data)
        
        # Cache each item in a hash map and store their IDs in a set
        redis_cache.hset(f"item:{item_id}", mapping=item_data)
        redis_cache.sadd("item_ids", item_id)
        
    return jsonify(items), 200

@app.route('/items', methods=['POST'])
def add_item():
    name = request.json['name']
    description = request.json['description']
    cur = mysql.connection.cursor()
    cur.execute("INSERT INTO items (name, description) VALUES (%s, %s)", (name, description))
    item_id = cur.lastrowid  # Get the ID of the newly added item
    mysql.connection.commit()
    cur.close()
    
    # Add new item to cache
    redis_cache.hset(f"item:{item_id}", mapping={'id': item_id, 'name': name, 'description': description})
    redis_cache.sadd("item_ids", item_id)
    
    return jsonify({'message': 'Item added successfully!'}), 201

@app.route('/items/<int:id>', methods=['PUT'])
def update_item(id):
    name = request.json['name']
    description = request.json['description']
    cur = mysql.connection.cursor()
    cur.execute("UPDATE items SET name = %s, description = %s WHERE id = %s", (name, description, id))
    mysql.connection.commit()
    cur.close()
    
    # Update item in cache
    redis_cache.hset(f"item:{id}", mapping={'id': id, 'name': name, 'description': description})
    
    return jsonify({'message': 'Item updated successfully!'}), 200

@app.route('/items/<int:id>', methods=['DELETE'])
def delete_item(id):
    cur = mysql.connection.cursor()
    cur.execute("DELETE FROM items WHERE id = %s", [id])
    mysql.connection.commit()
    cur.close()
    
    # Remove item from cache
    redis_cache.delete(f"item:{id}")
    redis_cache.srem("item_ids", id)
    
    return jsonify({'message': 'Item deleted successfully!'}), 200

if __name__ == '__main__':
    app.run(debug=True)
