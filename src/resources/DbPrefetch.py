from resources.Globals import db, config
from db.Collection import Collection
from db.Entity import Entity
from db.Relation import Relation
from db.Stat import Stat
from db.File import File
from db.Service import Service

# db connection is located at db/BaseModel.py string 4

def prefetch__db():
    db.connect()
    db.create_tables([Collection, Entity, Relation, Stat, File, Service], safe=True)
    db.close()
