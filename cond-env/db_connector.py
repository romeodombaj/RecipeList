from pony import orm

DB = orm.Database()

class Receipt(DB.Entity):
    id = orm.PrimaryKey(int, auto=True)
    receipt = orm.Required(str, unique=True)
    description = orm.Required(str)
    price = orm.Optional(float)

DB.bind(provider="sqlite", filename="database.sqlite", create_db=True)
DB.generate_mapping(create_tables=True)


@orm.db_session
def add_receipt(receipt, description, price=None):
    try:
        with orm.db_session:
            Receipt(receipt=receipt, description=description, price=price)
            response = {"response":"Success"}
            return response
    except Exception as e:
        return {"response":"Error","error":e}
        

def get_receipt(receipt_to_get):
    try:
        with orm.db_session:
            result = Receipt.get(receipt=receipt_to_get).to_dict()
            response = {"response":"Success", "data":result}
            print(response)
            return response
    except Exception as e:
        return {"response":"Error","error":e}
    
def get_receipts(receipt_to_get):
    try:
        with orm.db_session:
            result = Receipt.get(receipt=receipt_to_get).to_dict()
            response = {"response":"Success", "data":result}
            print(response)
            return response
    except Exception as e:
        return {"response":"Error","error":e}




if __name__ == "__main__":
    #res= add_receipt("krumpir", "jako pečeni krumpir u pećnici")
    #print(res)
    res=get_receipt("krumpir")
    print(res)