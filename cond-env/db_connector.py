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
def get_recipe(recipe_to_get):
    try:
        with orm.db_session:
            result = Recipe.get(recipe=recipe_to_get).to_dict()
            response = {"response":"Success", "data":result}
            return response
    except Exception as e:
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
            Recipe(recipe=recipe["recipe"], image=recipe["image"], ingredients=recipe["ingredients"], category=recipe["category"], description=recipe["description"], create_date=datetime.now(), edit_date=datetime.now())
            response = {"response":"Success"}
            print(response)
            return response
    except Exception as e:
        return {"response":"Error","error":e}



#-----------------------------------------------
# uređivanje recepta / PATCH
def edit_recipe(recipe):
    try:
        with orm.db_session:
            temp_recipe = Recipe.get(id=recipe).delete()
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


if __name__ == "__main__":
    temp_recipe2 = {"recipe":"piletina", "image":"image", "ingredients":"ingredients", "category":"sda sd", "description":"sdasadsfdasdsgffdsdfsdfsadfs"}
    #res=add_recipe(temp_recipe2)
    #print(res)
    #res=get_recipes()
    #print(res)