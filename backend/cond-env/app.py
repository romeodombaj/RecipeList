from flask import Flask, jsonify, make_response

app = Flask(__name__)

temp_storage = []

@app.route("/")
def home():
        response = {"message":"Hello World"}
        return make_response(jsonify(response), 200)

if __name__ == "__main__":
        app.run(port=8080)