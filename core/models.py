

def required_columns(cls, ignore=['id']):
    columns = cls.__dict__['__table__'].columns
    required = [col.name for col in columns if not col.nullable and col.name not in ignore]
    return required


    