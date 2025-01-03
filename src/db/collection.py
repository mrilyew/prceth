from peewee import TextField, IntegerField, AutoField, BooleanField, TimestampField, JOIN
from resources.globals import consts, model_to_dict, time, operator, reduce, logger
from base import BaseModel
from relation import Relation
from entity import Entity

class Collection(BaseModel):
    self_name = 'collection'

    id = AutoField()
    name = TextField(index=True,default='...')
    description = TextField(index=True,null=True)
    order = IntegerField(null=True,default=0)
    author = TextField(null=True,default=consts['pc_fullname'])
    innertype = TextField(default='def',null=False)
    icon_hash = TextField(default='def',null=False)
    hidden = BooleanField(default=0)
    created_at = TimestampField(default=time.time())
    edited_at = TimestampField(null=True, default=0)
    
    @staticmethod
    def getAll():
        results = Collection.select().where(Collection.hidden == 0).order_by(Collection.order).dicts()
        result_entities = []

        for entity in results:
            result_entities.append(Collection(**entity))
        
        return result_entities
    
    @staticmethod
    def getAllCount():
        return Collection.select().where(Collection.hidden == 0).count()
    
    @staticmethod
    def get(id):
        try:
            return Collection.select().where(Collection.id == id).get()
        except:
            return None
    
    def takeInfo(self):
        return {
            "id": self.id,
            "name": self.name,
            "description": self.description,
            "order": self.order,
            "inner_type": self.innertype,
            "icon_hash": self.icon_hash,
            "created": self.created_at,
            "edited": self.edited_at,
            "count": self.getItemsCount(),
        }
    
    def switch(self, to_switch):
        f_order = self.order
        s_order = to_switch.order

        self.order = s_order
        to_switch.order = f_order

        self.save()
        to_switch.save()

    def __fetchItems(self, query = None, columns_search = []):
        items = (Relation
             .select(Relation, Collection, Entity)
             .where(Relation.parent_collection == self.id)
             .join(Collection, on=(Relation.child_collection == Collection.id), join_type=JOIN.LEFT_OUTER)
             .switch(Relation)
             .join(Entity, on=(Relation.child_entity == Entity.id), join_type=JOIN.LEFT_OUTER)
             .order_by(Relation.order)
             .where(Entity.hidden == 0))
        
        if query != None:
            query = query
            conditions = []

            if 'original_name' in columns_search:
                conditions.append(
                    (Entity.original_name.contains(query)) | 
                    (Collection.name.contains(query))
                )

            if 'display_name' in columns_search:
                conditions.append(
                    (Entity.display_name.contains(query))
                )

            if 'description' in columns_search:
                conditions.append(
                    (Collection.description.contains(query)) |
                    (Entity.description.contains(query))
                )

            if 'source' in columns_search:
                conditions.append(
                    (Entity.source.contains(query))
                )    

            if 'index_info' in columns_search:
                conditions.append(
                    (Entity.index_info.contains(query))
                )
            
            if 'saved_via' in columns_search:
                conditions.append(
                    (Entity.saved_via.contains(query))
                )   
                     
            if 'author' in columns_search:
                conditions.append(
                    (Entity.author.contains(query)) |
                    (Collection.author.contains(query))
                )
            
            if conditions:
                items = items.where(reduce(operator.or_, conditions))

        return items

    def getItems(self, page = None, query = None, columns_search = []):
        items = self.__fetchItems(query=query,columns_search=columns_search)
        if page != None:
            items = items.paginate(page, 10)
        
        results = []
        for relation in items:
            if relation.child_collection:
                results.append(Collection(**model_to_dict(relation.child_collection)))

            if relation.child_entity:
                results.append(Entity(**model_to_dict(relation.child_entity)))
        
        return results

    def getItemsCount(self, query = None, columns_search = []):
        items = self.__fetchItems(query=query,columns_search=columns_search)
        
        return items.count()
    
    def addItem(self, entity):
        if(self.hasItem(entity)):
            raise ValueError('Collection has that item')

        rel = Relation()
        rel.parent_collection = self.id
        if entity.__class__.__name__ == 'Collection':
            rel.child_collection = entity.id
        if entity.__class__.__name__ == 'Entity':
            rel.child_entity = entity.id

        rel.save()

    def removeItem(self, entity, delete_entity=True):
        if(not self.hasItem(entity)):
            raise ValueError("Error: entity does not belows to collection")

        rel = Relation.delete().where(Relation.parent_collection == self.id)
        if entity.__class__.__name__ == 'Collection':
            rel = rel.where(Relation.child_collection == entity.id)
        if entity.__class__.__name__ == 'Entity':
            rel = rel.where(Relation.child_entity == entity.id)

        rel.execute()
        if delete_entity == True:
            entity.delete()

    def hasItem(self, entity):
        rel = Relation.select().where(Relation.parent_collection == self.id)
        if entity.__class__.__name__ == 'Collection':
            rel = rel.where(Relation.child_collection == entity.id)
        if entity.__class__.__name__ == 'Entity':
            rel = rel.where(Relation.child_entity == entity.id)
        
        return rel.count() > 0
