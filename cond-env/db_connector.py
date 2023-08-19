from pony import orm
from datetime import date, datetime

DB = orm.Database()

class Recipe(DB.Entity):
    id = orm.PrimaryKey(int, auto=True)
    recipe = orm.Required(str)
    image = orm.Required(str)
    ingredients = orm.Required(str)
    category = orm.Required(str)
    description = orm.Required(str)
    create_date = orm.Required(datetime)
    edit_date = orm.Required(datetime)

    
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
def add_recipe(recipe):
    try:
        with orm.db_session:
            if(recipe["create_date"]):
                Recipe(recipe=recipe["recipe"], image=recipe["image"], ingredients=recipe["ingredients"], category=recipe["category"], description=recipe["description"], create_date=recipe["create_date"], edit_date=datetime.now())
            else:
                Recipe(recipe=recipe["recipe"], image=recipe["image"], ingredients=recipe["ingredients"], category=recipe["category"], description=recipe["description"], create_date=datetime.now(), edit_date=datetime.now())
            
            response = {"response":"Success"}
            print(response)
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
            temp_recipe.ingredients = recipe["ingredients"]
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


#if __name__ == "__main__":

    #temp_recipe2 = {"recipe":"piletina", "image":"image", "ingredients":"ingredients", "category":"sda sd", "description":"sdasadsfdasdsgffdsdfsdfsadfs"}
    #res=add_recipe({"recipe":"čum", "image":"image", "ingredients":"piletina", "category":"piletina", "description":"sdasadsfdasdsgffdsdfsdfsadfs", "create_date" : "2023-02-05" })
    #res=add_recipe({"recipe":"him", "image":"image", "ingredients":"piletina", "category":"piletina", "description":"sdasadsfdasdsgffdsdfsdfsadfs", "create_date" : "2022-02-03" })
    #res=add_recipe({"recipe":"bim", "image":"image", "ingredients":"piletina", "category":"piletina", "description":"sdasadsfdasdsgffdsdfsdfsadfs", "create_date" : "2022-02-03" })

    #res=add_recipe({"recipe":"em", "image":"image", "ingredients":"piletina", "category":"piletina", "description":"sdasadsfdasdsgffdsdfsdfsadfs", "create_date" : "2024-07-20" })
    #res=add_recipe({"recipe":"bum", "image":"image", "ingredients":"piletina", "category":"piletina", "description":"sdasadsfdasdsgffdsdfsdfsadfs", "create_date" : "2023-05-21" })

    #res=add_recipe({"recipe":"krumpir", "image":"image", "ingredients":"piletina", "category":"krumpir", "description":"sdasadsfdasdsgffdsdfsdfsadfs"})
    #res=add_recipe({"recipe":"grah", "image":"image", "ingredients":"piletina", "category":"grah", "description":"sdasadsfdasdsgffdsdfsdfsadfs"})
    #print(res)