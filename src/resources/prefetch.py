from resources.globals import db
from db.collection import Collection
from db.entity import Entity
from db.relation import Relation
from db.stat import Stat

def prefetch__db():
    db.connect()
    db.create_tables([Collection, Entity, Relation, Stat], safe=True)
    db.close()
