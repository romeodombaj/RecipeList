from pony import orm

DB = orm.Database()

class Receipt(DB.Entity):
    id = orm.PrimaryKey(int, auto=True)
    receipt = orm.Required(str, unique=True)
    description = orm.Required(str)
    
DB.bind(provider="sqlite", filename="database.sqlite", create_db=True)
DB.generate_mapping(create_tables=True)


@orm.db_session

#-----------------------------------------------
#dohvaćanje jednog recepta
def get_receipt(receipt_to_get):
    try:
        with orm.db_session:
            result = Receipt.get(receipt=receipt_to_get).to_dict()
            response = {"response":"Success", "data":result}
            return response
    except Exception as e:
        return {"response":"Error","error":e}
    



#-----------------------------------------------
#dohvaćanje svih recepata
def get_receipts():
    try:
        with orm.db_session:
            result = orm.select(el for el in Receipt)[:]
            temp_list = []
    
            for el in result:
                temp_list.append(el.to_dict())

            response = {"response":"Success", "data":temp_list}
            
            return response
        
    except Exception as e:
        return {"response":"Error","error":str(e)}



#-----------------------------------------------
#dodavanje recepta
def add_receipt(item):
    try:
        with orm.db_session:
            Receipt(receipt=item["receipt"], description=item["description"])
            response = {"response":"Success"}
            return response
    except Exception as e:
        return {"response":"Error","error":e}



#-----------------------------------------------
# uređivanje recepta / PATCH



#-----------------------------------------------
# brisanje recepta

if __name__ == "__main__":
    #res=add_receipt("piletina", "ekstra")
    #print(res)
    res=get_receipts()
    print(res)