from flask import Flask, jsonify, make_response, render_template, url_for, redirect, request
from db_connector import *

app = Flask(__name__)

temp_storage = []


#dohvati sve recepte
@app.route("/")
def home():
        response = get_recipes()
        if response["response"] == "Success":
                return make_response(render_template("index.html", data=response["data"]), 200)

        else:
                return make_response(render_template("index.html"), 200)


#dohvati pojedinacni recept
@app.route("/recept")
def getData():
        response = {"message":"Hello World"}
        return make_response(render_template("index.html"))



#dodaj novi recept
@app.route("/dodaj", methods=["POST","GET"])
def add():
        if request.method == "POST":
                try:
                        temp = {}
                        for key, value in request.form.items():
                                if value == "":
                                        temp[key] = None
                                        print("Nonemone")
                                else:
                                        temp[key] = value
                except Exception as e:
                        response = {"response":str(e)}
                        return(make_response(jsonify(response), 400))
                
                response = add_recipe(temp)

                if response["response"] == "Success":
                        return home()        
                else:
                        return make_response(render_template("dodaj.html"), 400)        
        else:
                return make_response(render_template("dodaj.html"), 200)        


#uredi recept

@app.route("/edit/<id>", methods=["POST", "GET"])
def edit(id):
        if request.method == "POST":
                try:
                        temp = {}
                        for key, value in request.form.items():
                                if value == "":
                                        temp[key] = None
                                else:
                                        temp[key] = value
                except Exception as e:
                        response = {"response":str(e)}
                        return (make_response(jsonify(response), 400))
                
                response = edit_recipe(id, temp)

                if response["response"] == "Success":
                        return home()        
                else:
                        return make_response(render_template("uredi.html"), 400)        
        else:
                 response = get_recipe(id)

                 if response["response"] == "Success":
                        return make_response(render_template("uredi.html", data=response["data"]), 200)
                        

                 else:
                        return (make_response(jsonify(response), 400))


#izbriši recept
@app.route("/delete/<id>", methods=["POST", "GET"])
def delete(id):
        response = delete_recipe(id)

        if response["response"] == "Success":
                return home()
        else:
                return make_response(render_template("dodaj.html"))



# ako se aplikacija pokreće na lokalnoj mašini
# treba zakomentirati 1. #app.run() i odgomentirati 2.
# u slučaju da se aplikacija pokrece na subsistemu poput WSL
# ostavlja se 1. app.run()
if __name__ == "__main__":
        #1.
        app.run(host="0.0.0.0", port=8080)
        #2.
        #app.run(port=8080)