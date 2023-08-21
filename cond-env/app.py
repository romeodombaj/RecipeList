from flask import Flask, jsonify, make_response, render_template, url_for, redirect, request
from db_connector import *
from datetime import date, datetime
import time

app = Flask(__name__)




#dohvati sve recepte
@app.route("/")
def home(user=""):
        temp="0001"
        response = get_recipes()
        print(response["response"])
        if response["response"] == "Success":
                try:
                        if user != "":
                                temp = user
                        else:
                                temp = request.cookies.get("currentUser")
                        resp = make_response(render_template("index.html", data=response["data"], currentUser=temp), 200)

                except Exception as e:
                        resp = make_response(render_template("index.html", data=response["data"], currentUser="0001"), 200)
                        temp = ""

                if user != "":
                        resp.set_cookie('currentUser', user)
                elif temp == "":
                        resp.set_cookie('currentUser', "0001")

                
                return resp
        else:
                return make_response(render_template("index.html"), 200)


#dohvati pojedinacni recept
@app.route("/recipe/<id>", methods=["POST", "GET"])
def recipe(id):
        response = get_recipe(id)
        if response["response"] == "Success":
                currentUser = request.cookies.get("currentUser")
                user = get_user(currentUser)
                saved = ""

                print(user["data"])

                if int(response["data"]["id"]) in user["data"]["saved_recipes"]:
                        saved = True
                        print("saved")
                else:
                        saved = False
                        print("unsaved")

                if request.method == "POST":
                        print(request.form["save"])
                        if request.form["save"] == "False":
                                res = save_recipe(currentUser, id)
                                saved=True

                        else:
                                unsave_recipe(currentUser, id)
                                saved=False
                        
                        return make_response(render_template("recipe.html", data=response["data"], currentUser=currentUser, saved=saved), 200)

                else:
                        return make_response(render_template("recipe.html", data=response["data"], currentUser=currentUser, saved=saved), 200)

        

        else:
                return make_response(render_template("index.html"), 200)



#dodaj novi recept
@app.route("/dodaj", methods=["POST","GET"])
def add():
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
                        return(make_response(jsonify(response), 400))

                tempU = request.cookies.get("currentUser")
                print(tempU)

                if(tempU is None):
                        tempU = "0001"
                
                response = add_recipe(temp, tempU)

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
                     response["data"]["ingredients"] = ",".join(response["data"]["ingredients"])
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


#statistika
@app.route("/statistics", methods=["POST", "GET"])
def statistics():
        response = get_recipes()
        resp_users = get_users()
        if response["response"] and resp_users["response"] == "Success":
                #podaci za 1. graf / br kreiranih recepata po datumu
                datumi = [str(x["create_date"].date()) for x in response["data"]]
                datumi.sort(key=lambda x: time.mktime(time.strptime(x,"%Y-%m-%d")))
                recept_datum = {i: datumi.count(i) for i in datumi}

                #podaci za 2. graf broj recepata po kategoriji
                kategorije = [str(x["category"]) for x in response["data"]]
                recept_kategorija = {i: kategorije.count(i) for i in kategorije}
        
                #podaci za 3. graf / br spremljenih recepata po korisniku
                users_data = {
                        "usernames":[],
                        "num_recipes":[]
                }
                print(resp_users["data"])
                
                for x in resp_users["data"]:
                        #users_data.append ({"username": x["username"], "number_of_saved": len(x["saved_recipes"])})
                        users_data["usernames"].append(x["username"])
                        users_data["num_recipes"].append(len(x["saved_recipes"]))

                return make_response(render_template("statistika.html",  recept_datum=recept_datum, recept_kategorija=recept_kategorija, recept_korisnik=users_data), 200)
        else:
                return home()


#odabir korisnika
@app.route("/user_select/", methods=["POST", "GET"])
def user_select():
        
        if request.method == "POST":
                if request.form["submit_user"] == "user1":
                        currentUser = "0001"
                else:
                        currentUser = "0002"
                print(currentUser)


                return home(currentUser)
        else:
                return make_response(render_template("korisnik.html"), 400)


#recepti specifičnog korisnika
@app.route("/user_recipes/", methods=["GET"])
def user_recipes():
        response = get_recipes()
        if response["response"] == "Success":
                temp_list = []
                currentUser = request.cookies.get("currentUser")
                for x in response["data"]:
                        if x["user"] == currentUser:
                                temp_list.append(x)

                return make_response(render_template("recepti_korisnika.html", data=temp_list, currentUser=currentUser), 200)
        else:
                return home()

#spremljeni recepti specfičnog korisnika
@app.route("/saved_recipes/", methods=["GET"])
def saved_recipes():
        response = get_recipes()
        if response["response"] == "Success":
                temp_list = []
                currentUser = request.cookies.get("currentUser")
                user_saved_recipes = get_user(currentUser)["data"]["saved_recipes"]
                print(user_saved_recipes)
                for x in response["data"]:
                        for y in user_saved_recipes:
                                if y == x["id"]:
                                        temp_list.append(x)

                return make_response(render_template("spremljeni_recepti.html", data=temp_list, currentUser=currentUser), 200)
        else:
                return home()        

       

# ako se aplikacija pokreće na lokalnoj mašini
# treba zakomentirati 1. #app.run() i odgomentirati 2.
# u slučaju da se aplikacija pokrece na subsistemu poput WSL
# ostavlja se 1. app.run()
if __name__ == "__main__":
        #1.
        app.run(host="0.0.0.0", port=8080)
        #2.
        #app.run(port=8080)