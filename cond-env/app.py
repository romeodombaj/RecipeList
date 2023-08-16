from flask import Flask, jsonify, make_response, render_template, url_for, redirect
from db_connector import get_receipt

app = Flask(__name__)

temp_storage = []

@app.route("/")
def home():
        response = get_receipt("krumpir")
        print(response)
        return make_response(render_template("index.html", data=response["data"]), 200)


@app.route("/get")
def getData():
        response = {"message":"Hello World"}
        return make_response(render_template("index.html"))


if __name__ == "__main__":
        app.run(port=8080)