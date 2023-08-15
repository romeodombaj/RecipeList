from pony import orm

DB = orm.Database()

class Receipt(DB.Entity):
    id = orm.PrimaryKey(int, auto=True)
    receipt = orm.Required(str, unique=True)
    description = orm.Required(str)
    price = orm.Optional(float)

DB.bind(provider="sqlite", filename="database.sqlite", create_db=True)
DB.generate_mapping(create_tables=True)