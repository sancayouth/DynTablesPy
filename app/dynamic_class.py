from extensions import db
from sqlalchemy.ext.automap import automap_base

classes = {}

def loadClass(name):
    name = name.lower()
    if name not in classes:
        db.Model.metadata.reflect(db.engine)
        Base = automap_base()
        Base.prepare(db.engine, reflect=True)
        classes[name] = Base.classes.get(name)
    return classes[name]
