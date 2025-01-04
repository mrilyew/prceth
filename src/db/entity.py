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
    source = TextField(null=True) # Source of content
    filesize = BigIntegerField(default=0)
    index_content = TextField(null=True) # Content for search
    json_info = TextField(index=True,null=True)
    frontend_data = TextField(null=True)
    extractor_name = TextField(null=True,default='base')
    preview = TextField(null=True)
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

    def getApiStructure(self):
        return {
            "id": self.id,
            "format": self.format,
            "original_name": self.original_name,
            "display_name": self.display_name,
            "description": self.description,
            "filesize": self.filesize,
            "index_content": self.index_content,
            "json_info": self.json_info,
            "frontend_data": self.frontend_data,
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
    def fetchItems(query = None, columns_search = []):
        items = Entity.select().where(Entity.hidden == 0)
        conditions = []

        for column in columns_search:
            match column:
                case "original_name":
                    conditions.append((Entity.original_name.contains(query)))
                case "display_name":
                    conditions.append((Entity.display_name.contains(query)))
                case "description":
                    conditions.append((Entity.description.contains(query)))
                case "source":
                    conditions.append((Entity.source.contains(query)))
                case "index":
                    conditions.append((Entity.index_content.contains(query)))
                case "saved":
                    conditions.append((Entity.extractor_name.contains(query)))
                case "author":
                    conditions.append((Entity.author.contains(query)))
        
        if conditions:
            items = items.where(reduce(operator.or_, conditions))

        return items
    
    @staticmethod
    def get(id):
        try:
            return Entity.select().where(Entity.id == id).where(Entity.hidden == 0).get()
        except:
            return None
