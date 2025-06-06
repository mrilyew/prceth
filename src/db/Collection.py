from peewee import fn, TextField, IntegerField, AutoField, BooleanField, TimestampField, DeferredForeignKey, JOIN
import time, operator, json, os
from resources.Consts import consts
from playhouse.shortcuts import model_to_dict
from functools import reduce
from db.BaseModel import BaseModel

class Collection(BaseModel):
    '''
    Model that represents collection of other entities. Refers to "Relation"
    '''
    self_name = 'collection'

    class Meta:
        table_name = 'collections'

    id = AutoField() # Auto increment id.
    name = TextField(index=True,default='...') # Name of collection.
    description = TextField(index=True,null=True) # Alt.
    order = IntegerField(null=True,default=0,index=True) # Order in main list.
    author = TextField(null=True,default=consts['pc_fullname']) # Author of collection.
    source = TextField(null=True) # Source of content (URL or path).
    frontend_data = TextField(null=True) # Info that will be used in frontend. Set by frontend.
    preview_id = TextField(null=True) # Id of ContentUnit that taken for traditional preview.
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
    
    def api_structure(self):
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

    def _fetchItems(self, query = None, columns_search = []):
        from db.ContentUnit import ContentUnit
        from db.Collection import Collection
        from db.Relation import Relation

        DeferredForeignKey.resolve(ContentUnit)
        DeferredForeignKey.resolve(Collection)

        items = (Relation
        .select(Relation, Collection, ContentUnit)
        .where(Relation.parent_collection_id == self.id)
        .join(Collection, on=(Relation.child_collection_id == Collection.id), join_type=JOIN.LEFT_OUTER)
        .switch(Relation)
        .join(ContentUnit, on=(Relation.child_ContentUnit_id == ContentUnit.id), join_type=JOIN.LEFT_OUTER)
        .order_by(Relation.order)
        .where(ContentUnit.deleted == 0))
        
        if query != None:
            query = query
            conditions = [] # litwin

            for column in columns_search:
                match column:
                    case "original_name":
                        conditions.append(
                            (ContentUnit.original_name.contains(query)) | 
                            (Collection.name.contains(query))
                        )
                    case "display_name":
                        conditions.append(
                            (ContentUnit.display_name.contains(query))
                        )
                    case "description":
                        conditions.append(
                            (Collection.description.contains(query)) |
                            (ContentUnit.description.contains(query))
                        )
                    case "source":
                        conditions.append(
                            (ContentUnit.source.contains(query))
                        )
                    case "index":
                        conditions.append(
                            (ContentUnit.index_content.contains(query))
                        )
                    case "saved":
                        conditions.append(
                            (ContentUnit.extractor_name.contains(query))
                        )
                    case "author":
                        conditions.append(
                            (ContentUnit.author.contains(query)) |
                            (Collection.author.contains(query))
                        )
            if conditions:
                items = items.where(reduce(operator.or_, conditions))

        return items

    def getItems(self, offset = 0, limit = 10, query = None, columns_search = [], order = None):
        from db.ContentUnit import ContentUnit

        items = self._fetchItems(query=query,columns_search=columns_search)
        items = items.offset(offset)
        if limit != None:
            items = items.limit(limit)

        if order == "rand":
            items = items.order_by(fn.Random())

        results = []
        for relation in items:
            if relation.child_collection_id:
                results.append(Collection(**model_to_dict(relation.child_collection_id)))

            if relation.child_ContentUnit_id:
                results.append(ContentUnit(**model_to_dict(relation.child_ContentUnit_id)))
        
        return results
    
    '''def delete(self, delete_file=True):
        self.deleted = 1
        self.save()'''

    def getItemsCount(self, query = None, columns_search = []):
        items = self._fetchItems(query=query,columns_search=columns_search)
        
        return items.count()

    def addItem(self, ContentUnit):
        from db.Relation import Relation

        if(self.hasItem(ContentUnit)):
            raise ValueError('Collection has that item')

        rel = Relation()
        rel.parent_collection_id = self.id
        if ContentUnit.__class__.__name__ == 'Collection':
            rel.child_collection_id = ContentUnit.id
        if ContentUnit.__class__.__name__ == 'ContentUnit':
            rel.child_ContentUnit_id = ContentUnit.id

        rel.save()

    def removeItem(self, ContentUnit, delete_ContentUnit=True):
        from db.Relation import Relation

        if(not self.hasItem(ContentUnit)):
            raise ValueError("Error: ContentUnit does not belows to collection")

        rel = Relation.delete().where(Relation.parent_collection_id == self.id)
        if ContentUnit.__class__.__name__ == 'Collection':
            rel = rel.where(Relation.child_collection_id == ContentUnit.id)
        if ContentUnit.__class__.__name__ == 'ContentUnit':
            rel = rel.where(Relation.child_ContentUnit_id == ContentUnit.id)

        rel.execute()
        if delete_ContentUnit == True:
            ContentUnit.delete()

    def hasItem(self, ContentUnit):
        from db.Relation import Relation

        rel = Relation.select().where(Relation.parent_collection_id == self.id)
        if ContentUnit.__class__.__name__ == 'Collection':
            rel = rel.where(Relation.child_collection_id == ContentUnit.id)
        if ContentUnit.__class__.__name__ == 'ContentUnit':
            rel = rel.where(Relation.child_ContentUnit_id == ContentUnit.id)
        
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
        stream.write(json.dumps(self.api_structure(), indent=2))
        stream.close()
