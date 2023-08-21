from pony import orm
from pony.orm import *
from datetime import date, datetime

DB = orm.Database()

class Recipe(DB.Entity):
    id = orm.PrimaryKey(int, auto=True)
    recipe = orm.Required(str)
    image = orm.Required(str)
    ingredients = orm.Required(StrArray)
    category = orm.Required(str)
    description = orm.Required(str)
    create_date = orm.Required(datetime)
    edit_date = orm.Required(datetime)
    user = orm.Required(str)

class User(DB.Entity):
    id = orm.PrimaryKey(str)
    username = orm.Required(str, unique=True)
    saved_recipes = orm.Required(IntArray)



    
DB.bind(provider="sqlite", filename="database.sqlite", create_db=True)
DB.generate_mapping(create_tables=True)


@orm.db_session

#-----------------------------------------------
#dohvaćanje jednog recepta
def get_recipe(id):
    try:
        with orm.db_session:
            result = Recipe.get(id=id).to_dict()
            response = {"response":"Success", "data":result}    
            return response
    except Exception as e:
        print(e)
        return {"response":"Error","error":e}
    



#-----------------------------------------------
#dohvaćanje svih recepata
def get_recipes():
    try:
        with orm.db_session:
            result = orm.select(el for el in Recipe)[:]
            temp_list = []
    
            for el in result:
                temp_list.append(el.to_dict())

            response = {"response":"Success", "data":temp_list}
            
            return response
        
    except Exception as e:
        return {"response":"Error","error":str(e)}



#-----------------------------------------------
#dodavanje recepta
def add_recipe(recipe, user):
    try:
        with orm.db_session:

            if hasattr(recipe, "create_date") == False :
                tempDate = "2023-02-01"
            else:
                tempDate = recipe["create_date"]

            if recipe["image"] is None:
                tempImage = "https://img.taste.com.au/Ktdodg-f/taste/2016/11/whole-chickens-116421-1.jpg"
            else:
                tempImage = recipe["image"]
            

            Recipe(recipe=recipe["recipe"], image=tempImage, ingredients=recipe["ingredients"].split(","), category=recipe["category"], description=recipe["description"], create_date=tempDate, edit_date=datetime.now(), user=user)


            response = {"response":"Success"}
            return response
    except Exception as e:
        return {"response":"Error","error":e}



#-----------------------------------------------
# uređivanje recepta / PATCH
def edit_recipe(id, recipe):
    try:
        with orm.db_session:
            
            temp_recipe = Recipe.get(id=id)
            temp_recipe.recipe = recipe["recipe"]
            temp_recipe.image = recipe["image"]
            temp_recipe.ingredients = recipe["ingredients"].split(",")
            temp_recipe.category = recipe["category"]
            temp_recipe.description = recipe["description"]
            temp_recipe.edit_date = datetime.now()
            
            
            response = {"response": "Success"}
            return response
    except Exception as e:
        return {"response": "Error", "error": str(e)}


#-----------------------------------------------
# brisanje recepta
def delete_recipe(recipe):
    try:
        with orm.db_session:
            Recipe.get(id=recipe).delete()
            response = {"response": "Success"}
            return response
    except Exception as e:
        return {"response": "Error", "error": str(e)}
    

#dodavanje usera
def add_user(user):
    try:
        with orm.db_session:
            User(id=user["id"], username=user["username"], saved_recipes = [])

            response = {"response":"Success"}
            return response
    except Exception as e:
        return {"response":"Error","error":e}
    
def get_user(userID):
    try:
        with orm.db_session:
            result = User.get(id=userID).to_dict()
            response = {"response":"Success", "data":result}
            return response
    except Exception as e:
        return {"response":"Error","error":e}
    
def get_users():
    try:
        with orm.db_session:
            result = orm.select(el for el in User)[:]
            temp_list = []
    
            for el in result:
                temp_list.append(el.to_dict())

            response = {"response":"Success", "data":temp_list}
            
            return response
        
    except Exception as e:
        return {"response":"Error","error":str(e)}


#spremanje recepta
def save_recipe(userID, recipeID):
    try:
        with orm.db_session:
            print("saving the recipe")
            temp_recipe = User.get(id=userID)
            temp_recipe.id = temp_recipe.id
            temp_recipe.username = temp_recipe.username

            print (temp_recipe.username)

            if(int(recipeID) not in temp_recipe.saved_recipes):
                temp_recipe.saved_recipes.append(int(recipeID))

            response = {"response": "Success"}
            return response
    except Exception as e:
        return {"response": "Error", "error": str(e)}
    
#brisanje spremljenog recepta    
def unsave_recipe(userID, recipeID):
    try:
        with orm.db_session:
            
            temp_recipe = User.get(id=userID)
            temp_recipe.saved_recipes.remove(int(recipeID))
           
            response = {"response": "Success"}
            return response
    except Exception as e:
        return {"response": "Error", "error": str(e)}


#if __name__ == "__main__":
    #add_user({"id":"0001", "username":"user1"})
    #add_user({"id":"0002", "username":"user2"})
    #sv = save_recipe("0002", 2)
    #print(sv["response"])
    #sv = unsave_recipe("0001", 1)
    #print(sv["response"])
    #add_user({"id":"0001", "username":"user1"})
    #add_user({"id":"0002", "username":"user2"})

    #temp_recipe2 = {"recipe":"piletina", "image":"image", "ingredients":"ingredients", "category":"sda sd", "description":"sdasadsfdasdsgffdsdfsdfsadfs"}
    #res=add_recipe({"recipe":"Pohana piletina", "image":"https://podravkaiovariations.blob.core.windows.net/2a48c030-631f-11eb-8ddb-0242ac120068/v/f2b1f6a6-64bc-11eb-b6c2-0242ac130010/1024x768-f2b21802-64bc-11eb-a115-0242ac130010.webp", "ingredients":"1kg piletina, 20g brašna, žlica soli, 2jaja", "category":"piletina", "description":"Pileći file narežite na tanje šnicle,bez da ih batom rastanjujete,lagano ih posolite sa svake strane. U većoj zdjeli pomiješajte brašno,gustin,crvenu papriku,češnjak,Vegetu papar,jaje i jogurt,miješajte žicom dok god ne dobijete finu glatku smjesu bez grudica.Piletinu ravnomjerno uronite u smjesu,pokrijte posudu folijom i ostavite piletinu u hladnjaku najmanje 30 min,što duže odstoji tim bolje. Nakon što je odstajala,vilicom vadite komade pilećih prsa zajedno sa smjesom i uvaljajte u krušne mrvice.U tavi zagrijte ulje,stavljajte panirane komade piletine i pecite sa svake strane oko 5 min.dok ne dobije rumenu boju.Pečeno izvadite na kuhinjski papir da bi se ocijedio višak masnoće.", "create_date":"2023-02-05"}, "0001" )
    #res=add_recipe({"recipe":"Pohana piletina", "image":"https://podravkaiovariations.blob.core.windows.net/2a48c030-631f-11eb-8ddb-0242ac120068/v/f2b1f6a6-64bc-11eb-b6c2-0242ac130010/1024x768-f2b21802-64bc-11eb-a115-0242ac130010.webp", "ingredients":"1kg piletina, 20g brašna, žlica soli, 2jaja", "category":"piletina", "description":"Pileći file narežite na tanje šnicle,bez da ih batom rastanjujete,lagano ih posolite sa svake strane. U većoj zdjeli pomiješajte brašno,gustin,crvenu papriku,češnjak,Vegetu papar,jaje i jogurt,miješajte žicom dok god ne dobijete finu glatku smjesu bez grudica.Piletinu ravnomjerno uronite u smjesu,pokrijte posudu folijom i ostavite piletinu u hladnjaku najmanje 30 min,što duže odstoji tim bolje. Nakon što je odstajala,vilicom vadite komade pilećih prsa zajedno sa smjesom i uvaljajte u krušne mrvice.U tavi zagrijte ulje,stavljajte panirane komade piletine i pecite sa svake strane oko 5 min.dok ne dobije rumenu boju.Pečeno izvadite na kuhinjski papir da bi se ocijedio višak masnoće.", "create_date":"2023-02-06"}, "0002" )
    #res=add_recipe({"recipe":"Pečeni krumpir", "image":"https://recepti-api.index.hr/img/preview/large/recipe/15946d81-8987-4237-933f-bfed9fa33722/shutterstock_367257002.jpg", "ingredients":"1kg krumpir, 20g brašna, žlica soli,", "category":"krumpir", "description":"Operite krumpir, ali ga nemojte guliti. Narežite ga na kockice i ako imate vremena namočite krumpir u hladnoj vodi oko 1 sat. Time se uklanja škrob i dobiva se mekši krumpir. Ocijedite i po potrebi osušite krumpir. Potom ga začinite i dodajte maslinovo ulje.", "create_date":"2022-01-03"}, "0002" )
    #res=add_recipe({"recipe":"Pečena piletina", "image":"", "ingredients":"1kg piletina, 20g brašna, žlica soli, 2jaja", "category":"piletina", "description":"Pileći file narežite na tanje šnicle,bez da ih batom rastanjujete,lagano ih posolite sa svake strane. U većoj zdjeli pomiješajte brašno,gustin,crvenu papriku,češnjak,Vegetu papar,jaje i jogurt,miješajte žicom dok god ne dobijete finu glatku smjesu bez grudica.Piletinu ravnomjerno uronite u smjesu,pokrijte posudu folijom i ostavite piletinu u hladnjaku najmanje 30 min,što duže odstoji tim bolje. Nakon što je odstajala,vilicom vadite komade pilećih prsa zajedno sa smjesom i uvaljajte u krušne mrvice.U tavi zagrijte ulje,stavljajte panirane komade piletine i pecite sa svake strane oko 5 min.dok ne dobije rumenu boju.Pečeno izvadite na kuhinjski papir da bi se ocijedio višak masnoće.", "create_date":"2023-02-02"}, "0001" )
    
    #res=add_recipe({"recipe":"Piletina", "image":"https://podravkaiovariations.blob.core.windows.net/2a48c030-631f-11eb-8ddb-0242ac120068/v/f2b1f6a6-64bc-11eb-b6c2-0242ac130010/1024x768-f2b21802-64bc-11eb-a115-0242ac130010.webp", "ingredients":"1kg piletina, 20g brašna, žlica soli, 2jaja", "category":"piletina", "description":"Pileći file narežite na tanje šnicle,bez da ih batom rastanjujete,lagano ih posolite sa svake strane. U većoj zdjeli pomiješajte brašno,gustin,crvenu papriku,češnjak,Vegetu papar,jaje i jogurt,miješajte žicom dok god ne dobijete finu glatku smjesu bez grudica.Piletinu ravnomjerno uronite u smjesu,pokrijte posudu folijom i ostavite piletinu u hladnjaku najmanje 30 min,što duže odstoji tim bolje. Nakon što je odstajala,vilicom vadite komade pilećih prsa zajedno sa smjesom i uvaljajte u krušne mrvice.U tavi zagrijte ulje,stavljajte panirane komade piletine i pecite sa svake strane oko 5 min.dok ne dobije rumenu boju.Pečeno izvadite na kuhinjski papir da bi se ocijedio višak masnoće.", "create_date":"2023-02-02"}, "0001" )
    #print(res)
    #res=add_recipe({"recipe":"Sendvič", "image":"https://www.journal.hr/wp-content/uploads/2020/03/Sendvi%C4%8Di-novo.jpg", "ingredients:": "salama, sir, kruh", "create_date":"2023-03-06"}, "0002" )
    #res=add_recipe({"recipe":"Pohana piletina", "image":"https://podravkaiovariations.blob.core.windows.net/b0196df6-6386-11eb-b3b8-0242ac120039/v/f2b1f6a6-64bc-11eb-b6c2-0242ac130010/1600x1200-f2b21938-64bc-11eb-9498-0242ac130010.webp", "ingredients":"1kg piletina, 20g brašna, žlica soli, 2jaja", "category":"piletina", "description":"Pileći file narežite na tanje šnicle,bez da ih batom rastanjujete,lagano ih posolite sa svake strane. U većoj zdjeli pomiješajte brašno,gustin,crvenu papriku,češnjak,Vegetu papar,jaje i jogurt,miješajte žicom dok god ne dobijete finu glatku smjesu bez grudica.Piletinu ravnomjerno uronite u smjesu,pokrijte posudu folijom i ostavite piletinu u hladnjaku najmanje 30 min,što duže odstoji tim bolje. Nakon što je odstajala,vilicom vadite komade pilećih prsa zajedno sa smjesom i uvaljajte u krušne mrvice.U tavi zagrijte ulje,stavljajte panirane komade piletine i pecite sa svake strane oko 5 min.dok ne dobije rumenu boju.Pečeno izvadite na kuhinjski papir da bi se ocijedio višak masnoće.", "create_date":"2023-02-06"}, "0001" )
    #res=add_recipe({"recipe":"Pohana piletina", "image":"https://podravkaiovariations.blob.core.windows.net/2a48c030-631f-11eb-8ddb-0242ac120068/v/f2b1f6a6-64bc-11eb-b6c2-0242ac130010/1024x768-f2b21802-64bc-11eb-a115-0242ac130010.webp", "ingredients":"1kg piletina, 20g brašna, žlica soli, 2jaja", "category":"piletina", "description":"Pileći file narežite na tanje šnicle,bez da ih batom rastanjujete,lagano ih posolite sa svake strane. U većoj zdjeli pomiješajte brašno,gustin,crvenu papriku,češnjak,Vegetu papar,jaje i jogurt,miješajte žicom dok god ne dobijete finu glatku smjesu bez grudica.Piletinu ravnomjerno uronite u smjesu,pokrijte posudu folijom i ostavite piletinu u hladnjaku najmanje 30 min,što duže odstoji tim bolje. Nakon što je odstajala,vilicom vadite komade pilećih prsa zajedno sa smjesom i uvaljajte u krušne mrvice.U tavi zagrijte ulje,stavljajte panirane komade piletine i pecite sa svake strane oko 5 min.dok ne dobije rumenu boju.Pečeno izvadite na kuhinjski papir da bi se ocijedio višak masnoće.", "create_date":"2023-02-05"}, "0002" )

    #res=add_recipe({"recipe":"him", "image":"image", "ingredients":"piletina", "category":"piletina", "description":"sdasadsfdasdsgffdsdfsdfsadfs", "create_date" : "2022-02-03" })
    #res=add_recipe({"recipe":"bim", "image":"image", "ingredients":"piletina", "category":"piletina", "description":"sdasadsfdasdsgffdsdfsdfsadfs", "create_date" : "2022-02-03" })

    #res=add_recipe({"recipe":"em", "image":"image", "ingredients":"piletina", "category":"piletina", "description":"sdasadsfdasdsgffdsdfsdfsadfs", "create_date" : "2024-07-20" })
    #res=add_recipe({"recipe":"bum", "image":"image", "ingredients":"piletina", "category":"piletina", "description":"sdasadsfdasdsgffdsdfsdfsadfs", "create_date" : "2023-05-21" })

    #res=add_recipe({"recipe":"krumpir", "image":"image", "ingredients":"piletina", "category":"krumpir", "description":"sdasadsfdasdsgffdsdfsdfsadfs"})
    #res=add_recipe({"recipe":"grah", "image":"image", "ingredients":"piletina", "category":"grah", "description":"sdasadsfdasdsgffdsdfsdfsadfs"})
    #print(res)