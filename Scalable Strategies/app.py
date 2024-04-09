from flask import Flask, jsonify, request

app = Flask(__name__)

books = []

@app.route('/', methods=["GET"])
def root():
    app.logger.debug(f"Server host: {request.host}")
    return f'Welcome to the API'


if __name__ == '__main__':
    app.run(debug=True)
