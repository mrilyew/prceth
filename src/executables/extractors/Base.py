from resources.Globals import storage, os, utils, file_manager, json, logger
from db.Entity import Entity
from executables.Executable import Executable

class BaseExtractor(Executable):
    name = 'base'
    unsaved_entities = []

    def __init__(self, temp_dir=None, del_dir_on_fail=True, need_preview=True, write_mode=2):
        self.passed_params = {}
        #if temp_dir != None:
            #self.temp_dir_prefix = temp_dir
        self.temp_dir_prefix = None

        self.temp_dirs = []
        self.del_dir_on_fail = del_dir_on_fail
        self.need_preview = need_preview
        self.write_mode = int(write_mode)
        self.defineConsts()

    def defineConsts(self):
        pass

    def declare():
        params = {}
        params["display_name"] = {
            "name": "display_name",
            "type": "string",
            "default": None,
        }
        params["description"] = {
            "name": "description",
            "type": "string",
            "default": None,
        }
        params["unlisted"] = {
            "name": "unlisted",
            "type": "bool",
            "default": False,
        }
        params["make_preview"] = {
            "name": "make_preview",
            "type": "bool",
            "default": True,
        }

        return params
    
    def onFail(self):
        if self.del_dir_on_fail == True:
            for t_dir in self.temp_dirs:
                try:
                    file_manager.rmdir(t_dir)
                except Exception:
                    logger.logException(t_dir, "Extractor", noConsole=False)
    
    def _fileFromJson(self, json_data, _temp_dir = None):
        from db.File import File

        if _temp_dir == None:
            _temp_dir = self.temp_dirs[-1]

        return File.fromJson(json_data, _temp_dir)
    
    def _entityFromJson(self, json_data, make_preview = True):
        json_data["extractor_name"] = self.name
        __entity = Entity.fromJson(json_data, self.passed_params)
        # rewrite TODO
        if make_preview == True:
            thumb_result = self.thumbnail(entity=__entity,args=json_data)
            if thumb_result != None:
                __entity.preview = json.dumps(thumb_result)

        self.unsaved_entities.append(__entity)
        if self.write_mode == 2:
            __entity.save()
            logger.log(f"Saved entity {str(__entity.id)} 👍",section="EntitySaveMechanism",name="success")
        
        return __entity
    
    def _collectionFromJson(self, json_data):
        from db.Collection import Collection

        return Collection.fromJson(json_data, self.passed_params)
        
    async def run(self, args):
        pass
    
    async def postRun(self, return_entities):
        if self.write_mode == 1:
            try:
                ___ln = len(self.unsaved_entities)
                __msg = f"Saving total {str(___ln)} entities;"
                if ___ln > 100:
                    __msg += " do not turn off your computer."
                
                logger.log(__msg,section="EntitySaveMechanism",name="success")
            except Exception as _x:
                print(_x)
                pass

            for unsaved_entity in self.unsaved_entities:
                unsaved_entity.save()

                try:
                    logger.log(f"Saved entity {str(unsaved_entity.id)} 👍",section="EntitySaveMechanism",name="success")
                except Exception as _x:
                    print(_x)
                    pass

        for MOVE_ENTITY in return_entities:        
            if MOVE_ENTITY.self_name == "entity" and MOVE_ENTITY.file != None:
                try:
                    MOVE_ENTITY.file.moveTempDir()
                except:
                    pass
    
    # Typical preview
    def thumbnail(self, entity, args={}, temp_dir = None):
        if self.need_preview == False:
            return None
        
        from resources.Globals import ThumbnailsRepository
        __FILE = entity.file
        if __FILE == None:
            return None
        
        ext = __FILE.extension
        if args.get("preview_file"):
            ext = utils.get_ext(args.get("preview_file"))
        
        thumb = (ThumbnailsRepository()).getByFormat(ext)
        if thumb == None:
            return None
        
        if temp_dir == None:
            temp_dir = __FILE.temp_dir
        
        #thumb_class = thumb(save_dir=__FILE.getDirPath())
        thumb_class = thumb(save_dir=temp_dir)
        return thumb_class.run(file=__FILE,params=args)
    
    async def fastGetEntity(self, params, args):
        from db.File import File

        RETURN_ENTITIES = []
        self.setArgs(params)
        EXTRACTOR_RESULTS = await self.execute({})
        for ENTITY in EXTRACTOR_RESULTS.get("entities"):
            ENTITY.save()
            RETURN_ENTITIES.append(ENTITY)
            #if ENTITY.file != None:
            #    ENTITY.file.moveTempDir()

        return RETURN_ENTITIES

    def describeSource(self, INPUT_ENTITY):
        return {"type": "none", "data": {
            "source": None
        }}

    async def execute(self, args):
        EXTRACTOR_RESULTS = None

        try:
            EXTRACTOR_RESULTS = await self.run(args=args)
        except Exception as x:
            logger.logException(x, section="Exctractors")
            self.onFail()

            raise x

        return EXTRACTOR_RESULTS

    async def _execute_sub(self, extractor, final_array_link):
        try:
            executed = await extractor.execute({})
            for ___item in executed.get("entities"):
                final_array_link.append(___item)
        except Exception as ___e:
            logger.logException(input_exception=___e,section="Extractor",noConsole=False)
            pass

