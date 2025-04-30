from peewee import TextField, IntegerField, AutoField, BooleanField, TimestampField, DeferredForeignKey, JOIN
from resources.Globals import BaseModel, consts, time, operator, json, os
from playhouse.shortcuts import model_to_dict
from functools import reduce

class Collection(BaseModel):
    self_name = 'collection'

    id = AutoField() # Auto increment id.
    name = TextField(index=True,default='...') # Name of collection.
    description = TextField(index=True,null=True) # Alt.
    order = IntegerField(null=True,default=0,index=True) # Order in main list.
    author = TextField(null=True,default=consts['pc_fullname']) # Author of collection.
    source = TextField(null=True) # Source of content (URL or path).
    frontend_data = TextField(null=True) # Info that will be used in frontend. Set by frontend.
    preview_id = TextField(null=True) # Id of entity that taken for traditional preview.
    tags = TextField(index=True,null=True) # Csv tags.
    flags = IntegerField(default=0) # Flags.
    unlisted = BooleanField(default=0)
    deleted = BooleanField(default=0)
    created_at = TimestampField(default=time.time())
    declared_created_at = TimestampField(null=True)
    edited_at = TimestampField(null=True)

    @staticmethod
    def getAll(query=None):
        __db_query = Collection.select().where(Collection.deleted == 0)
        if query != None:
            __db_query = __db_query.where(Collection.name.contains(query))
            __db_query = __db_query.where(Collection.description.contains(query))
        
        return __db_query.order_by(Collection.order)
    
    @staticmethod
    def getAllCount(query=None):
        __db_query = Collection.select().where(Collection.deleted == 0)
        if query != None:
            __db_query = __db_query.where(Collection.name.contains(query))
            __db_query = __db_query.where(Collection.description.contains(query))
        
        return __db_query.count()
    
    @staticmethod
    def get(id):
        try:
            return Collection.select().where(Collection.id == id).get()
        except:
            return None
    
    def getApiStructure(self):
        obj = {
            "id": self.id,
            "name": self.name,
            "description": self.description,
            "order": self.order,
            "frontend_data": self.frontend_data,
            "preview": self.preview_id,
            "count": self.getItemsCount(),
            "created": None,
            "edited": None,
        }
        try:
            obj["created"] = int(self.created_at.timestamp())
            obj["edited"] = int(self.edited_at.timestamp())
        except Exception:
            pass

        return obj
    
    def switch(self, to_switch):
        f_order = self.order
        s_order = to_switch.order

        self.order = s_order
        to_switch.order = f_order

        self.save()
        to_switch.save()

    def __fetchItems(self, query = None, columns_search = []):
        from db.Entity import Entity
        from db.Collection import Collection
        from db.Relation import Relation

        DeferredForeignKey.resolve(Entity)
        DeferredForeignKey.resolve(Collection)

        items = (Relation
        .select(Relation, Collection, Entity)
        .where(Relation.parent_collection_id == self.id)
        .join(Collection, on=(Relation.child_collection_id == Collection.id), join_type=JOIN.LEFT_OUTER)
        .switch(Relation)
        .join(Entity, on=(Relation.child_entity_id == Entity.id), join_type=JOIN.LEFT_OUTER)
        .order_by(Relation.order)
        .where(Entity.deleted == 0))
        
        if query != None:
            query = query
            conditions = [] # litwin

            for column in columns_search:
                match column:
                    case "original_name":
                        conditions.append(
                            (Entity.original_name.contains(query)) | 
                            (Collection.name.contains(query))
                        )
                    case "display_name":
                        conditions.append(
                            (Entity.display_name.contains(query))
                        )
                    case "description":
                        conditions.append(
                            (Collection.description.contains(query)) |
                            (Entity.description.contains(query))
                        )
                    case "source":
                        conditions.append(
                            (Entity.source.contains(query))
                        )
                    case "index":
                        conditions.append(
                            (Entity.index_content.contains(query))
                        )
                    case "saved":
                        conditions.append(
                            (Entity.extractor_name.contains(query))
                        )
                    case "author":
                        conditions.append(
                            (Entity.author.contains(query)) |
                            (Collection.author.contains(query))
                        )
            if conditions:
                items = items.where(reduce(operator.or_, conditions))

        return items

    def getItems(self, offset = 0, limit = 10, query = None, columns_search = []):
        from db.Entity import Entity

        items = self.__fetchItems(query=query,columns_search=columns_search)
        items = items.offset(offset)
        if limit != None:
            items = items.limit(limit)

        results = []
        for relation in items:
            if relation.child_collection_id:
                results.append(Collection(**model_to_dict(relation.child_collection_id)))

            if relation.child_entity_id:
                results.append(Entity(**model_to_dict(relation.child_entity_id)))
        
        return results
    
    '''def delete(self, delete_file=True):
        self.deleted = 1
        self.save()'''

    def getItemsCount(self, query = None, columns_search = []):
        items = self.__fetchItems(query=query,columns_search=columns_search)
        
        return items.count()

    def addItem(self, entity):
        from db.Relation import Relation

        if(self.hasItem(entity)):
            raise ValueError('Collection has that item')

        rel = Relation()
        rel.parent_collection_id = self.id
        if entity.__class__.__name__ == 'Collection':
            rel.child_collection_id = entity.id
        if entity.__class__.__name__ == 'Entity':
            rel.child_entity_id = entity.id

        rel.save()

    def removeItem(self, entity, delete_entity=True):
        from db.Relation import Relation

        if(not self.hasItem(entity)):
            raise ValueError("Error: entity does not belows to collection")

        rel = Relation.delete().where(Relation.parent_collection_id == self.id)
        if entity.__class__.__name__ == 'Collection':
            rel = rel.where(Relation.child_collection_id == entity.id)
        if entity.__class__.__name__ == 'Entity':
            rel = rel.where(Relation.child_entity_id == entity.id)

        rel.execute()
        if delete_entity == True:
            entity.delete()

    def hasItem(self, entity):
        from db.Relation import Relation

        rel = Relation.select().where(Relation.parent_collection_id == self.id)
        if entity.__class__.__name__ == 'Collection':
            rel = rel.where(Relation.child_collection_id == entity.id)
        if entity.__class__.__name__ == 'Entity':
            rel = rel.where(Relation.child_entity_id == entity.id)
        
        return rel.count() > 0

    @staticmethod
    def fromJson(json_input, passed_params):
        FINAL_COLLECTION = Collection()
        if json_input.get("display_name") == None:
            if json_input.get("suggested_name") == None:
                FINAL_COLLECTION.name = "N/A"
            else:
                FINAL_COLLECTION.name = json_input.get("suggested_name")
        else:
            FINAL_COLLECTION.name = json_input.get("display_name")
        
        if json_input.get("suggested_description") != None:
            FINAL_COLLECTION.description = json_input.get("suggested_description")
        else:
            FINAL_COLLECTION.description = passed_params.get("description")

        FINAL_COLLECTION.order = Collection.getAllCount()
        if FINAL_COLLECTION.get("source") != None:
            FINAL_COLLECTION.source = json_input.get("source")
        if json_input.get("declared_created_at") != None:
            FINAL_COLLECTION.declared_created_at = int(json_input.get("declared_created_at"))
        
        FINAL_COLLECTION.save()

        return FINAL_COLLECTION
    
    def saveInfoToJson(self, dir):
        stream = open(os.path.join(dir, f"collection_{self.id}.json"), "w")
        stream.write(json.dumps(self.getApiStructure(), indent=2))
        stream.close()
