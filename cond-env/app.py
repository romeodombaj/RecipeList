from flask import Flask, jsonify, make_response, render_template, url_for, redirect
from db_connector import *

app = Flask(__name__)

temp_storage = []


#dohvati sve recepte
@app.route("/")
def home():
        response = get_receipts()
        print(response)
        return make_response(render_template("index.html", data=response["data"]), 200)



#dohvati pojedinacni recept
@app.route("/recept")
def getData():
        response = {"message":"Hello World"}
        return make_response(render_template("index.html"))


#dodaj novi recept

#uredi recept

#izbriši recept


# ako se aplikacija pokreće na lokalnoj mašini
# treba zakomentirati 1. #app.run() i odgomentirati 2.
# u slučaju da se aplikacija pokrece na subsistemu poput WSL
# ostavlja se 1. app.run()
if __name__ == "__main__":
        #1.
        app.run(host="0.0.0.0", port=8080)
        #2.
        #app.run(port=8080)