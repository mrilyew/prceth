from resources.Globals import db
from db.Collection import Collection
from db.Entity import Entity
from db.Relation import Relation
from db.Stat import Stat
from db.File import File

def prefetch__db():
    db.connect()
    db.create_tables([Collection, Entity, Relation, Stat, File], safe=True)
    db.close()
