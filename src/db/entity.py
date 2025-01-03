from resources.globals import consts, time, operator, reduce, Path
from peewee import TextField, BigIntegerField, AutoField, BooleanField, TimestampField
from resources.globals import BaseModel

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
