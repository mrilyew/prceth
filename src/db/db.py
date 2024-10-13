from peewee import *
from resources.globals import consts, model_to_dict, _, time, operator, reduce
from pathlib import Path

db = SqliteDatabase('storage/main.db')

class BaseModel(Model):
    class Meta:
        database = db

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
            "name": self.getCorrectName(),
            "description": self.getCorrectDescription(),
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
    
    def getCorrectName(self):
        current_name = self.name
        if current_name.startswith('_'):
            return _(current_name[1:])
        else:
            return current_name    
    
    def getCorrectDescription(self):
        current_desc = self.description

        if(current_desc == None):
            return '...'
        
        if current_desc.startswith('_'):
            return _(current_desc[1:])
        else:
            return current_desc
    
class Entity(BaseModel):
    self_name = 'entity'
    
    id = AutoField()
    format = TextField(null=True)
    original_name = TextField(default='N/A',null=False)
    display_name = TextField(index=True,default='N/A')
    description = TextField(index=True,null=True)
    source = TextField(null=True)
    filesize = BigIntegerField(default=0)
    cached_content = TextField(null=True)
    index_info = TextField(index=True,null=True)
    color = TextField(null=True,default='fff')
    saved_via = TextField(null=True,default='base')
    pinned = BooleanField(default=0)
    hidden = BooleanField(default=0)
    author = TextField(null=True,default=consts['pc_fullname'])
    created_at = TimestampField(default=time.time())
    edited_at = TimestampField(null=True, default=0)

    def deleteFile(self):
        Path(self.getPath()).unlink()
    
    def delete(self, delete_file=True):
        if delete_file == True:
            self.deleteFile()

        self.hidden = 1
        self.save()

    def takeInfo(self):
        return {
            "id": self.id,
            "format": self.format,
            "original_name": self.original_name,
            "display_name": self.display_name,
            "description": self.description,
            "filesize": self.filesize,
            "cached_content": self.cached_content,
            "index_info": self.index_info,
            "color": self.color,
            "pinned": self.pinned,
            "created": self.created_at,
            "edited": self.edited_at,
            "author": self.author,
            "path": self.getPath(),
        }
    
    def getPath(self):
        storage = consts['cwd'] + '\\storage'
        collection_path = storage + '\\collections\\' + str(self.id)
        entity_path = collection_path + '\\' + str(self.id) + '.' + str(self.format)

        return entity_path
    
    def getDirPath(self, need_check = True):
        storage_path = consts['cwd'] + '\\storage'
        collection_path = storage_path + '\\collections\\' + str(self.id)
        coll_path = Path(collection_path)

        if need_check == True and coll_path.exists() == False:
            coll_path.mkdir(parents=True, exist_ok=True)

        return collection_path
    
    @staticmethod
    def search(page=None, query = None, columns_search = []):
        items = Entity.select().where(Entity.hidden == 0)
        conditions = []

        if 'original_name' in columns_search:
            conditions.append(
                (Entity.original_name ** f'%{query}%')
            )

        if 'display_name' in columns_search:
            conditions.append(
                (Entity.display_name ** f'%{query}%')
            )

        if 'description' in columns_search:
            conditions.append(
                (Entity.description ** f'%{query}%')
            )

        if 'source' in columns_search:
            conditions.append(
                (Entity.source ** f'%{query}%')
            )    

        if 'index_info' in columns_search:
            conditions.append(
                (Entity.index_info ** f'%{query}%')
            )
        
        if 'saved_via' in columns_search:
            conditions.append(
                (Entity.saved_via ** f'%{query}%')
            )   
                    
        if 'author' in columns_search:
            conditions.append(
                (Entity.author ** f'%{query}%')
            )
        
        if conditions:
            items = items.where(reduce(operator.or_, conditions))
        
        if page != None:
            items = items.paginate(page, 10)
        
        results = []
        for item in items:
            results.append(item)
        
        return results
    
    @staticmethod
    def get(id):
        try:
            return Entity.select().where(Entity.id == id).get()
        except:
            return None

class Relation(BaseModel):
    parent_collection = BigIntegerField(null=True)
    child_collection = ForeignKeyField(null=True,backref='child_relations',model=Collection)
    child_entity = ForeignKeyField(null=True,backref='relations',model=Entity)
    order = AutoField()

class Stat(BaseModel):
    id = AutoField()
    name = TextField(default='Untitled')
    type = TextField(default='default')
    linked_id = BigIntegerField(default=0)
    timestamp = TimestampField(default=time.time())
'''
class Tag(BaseModel):
    id = AutoField()
    name = TextField(default='')
    color = TextField(default='')

class TagRelation(BaseModel):
    entity = ForeignKeyField(null=True,backref='entity',model=Entity)
    tag = ForeignKeyField(null=True,backref='tag',model=Tag)
    order = AutoField()
'''

db.connect()
db.create_tables([Collection, Entity, Relation, Stat], safe=True)
if Collection.select().count() == 0:
    i = Collection.getAllCount()
    Collection.create(name='_collections.saved_gifs',description='_collections.saved_gifs_description',innertype='gallery',icon_hash='gifs_icon',order=i)
    Collection.create(name='_collections.saved_images',description='_collections.saved_images_description',innertype='gallery',icon_hash='gallery_icon',order=i+1)
    Collection.create(name='_collections.videos',description='_collections.videos_description',innertype='videoslist',icon_hash='videos_icon',order=i+2)
    Collection.create(name='_collections.notes',description='_collections.notes_description',innertype='noteslist',icon_hash='notes_icon',order=i+3)
    Collection.create(name='_collections.saved_pages',description='_collections.saved_pages_description',innertype='websites_list',icon_hash='web_icon',order=i+4)
    Collection.create(name='_collections.saved_links',description='_collections.saved_links_description',innertype='links_list',icon_hash='links_list',order=i+5)
    Collection.create(name='_collections.audios',description='_collections.audios_description',innertype='audios_list',icon_hash='audio_icon',order=i+6)

db.close()
