from resources.Globals import storage, os, utils, file_manager, json, logger
from db.Entity import Entity

class BaseExtractor:
    name = 'base'
    category = 'template'
    params = {}
    passed_params = {}
    manual_params = False

    def __init__(self, temp_dir=None, del_dir_on_fail=True,need_preview=True):
        self.passed_params = {}
        #if temp_dir != None:
            #self.temp_dir_prefix = temp_dir
        self.temp_dir_prefix = None

        self.temp_dirs = []
        self.del_dir_on_fail = del_dir_on_fail
        self.need_preview = need_preview
    
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
    
    def setArgs(self, args):
        self.params = {}

        # Catching params from parent extractors
        for __sub_class in self.__class__.__mro__:
            if hasattr(__sub_class, "declare") == False:
                continue

            new_params = __sub_class.declare()
            self.params.update(new_params)
        
        MAX_OUTPUT_CHECK_PARAMS = self.params
        self.passed_params["make_preview"] = int(args.get("make_preview", 1))
        if MAX_OUTPUT_CHECK_PARAMS == None:
            return
        
        for index, param_name in enumerate(MAX_OUTPUT_CHECK_PARAMS):
            param_object = MAX_OUTPUT_CHECK_PARAMS.get(param_name)
            __value = args.get(param_name, param_object.get("default"))
            if __value != None:
                match(param_object.get("type")):
                    case "int":
                        __value = int(__value)
                    case "float":
                        __value = float(__value)
                    case "array":
                        __allowed = param_object.get("values")
                        assert __value in __allowed, "not valid value"

                        __value = param_object.get("default")
                    case "string":
                        if param_object.get("maxlength") != None:
                            __value = utils.proc_strtr(str(__value), int(param_object.get("maxlength")), multipoint=False)
                        else:
                            __value = str(__value)
                    case "object":
                        if type(__value) in ["dict", "array"] == False:
                            if param_object.get("default") != None:
                                __value = param_object.get("default")
                            else:
                                __value = None
                    case "bool":
                        __value = int(__value) == 1
                    case _:
                        break
                
                self.passed_params[param_name] = __value
            else:
                if param_object.get("default") != None:
                    self.passed_params[param_name] = param_object.get("default")

            if param_object.get("assertion") != None:
                __assertion = param_object.get("assertion")
                
                if __assertion.get("assert_not_null") == True:
                    assert __value != None, f"{param_name} not passed"

                if __assertion.get("assert_link") != None:
                    new_param_name = __assertion.get("assert_link")
                    new_param_object = MAX_OUTPUT_CHECK_PARAMS.get(new_param_name)

                    assert __value != None or args.get(new_param_name, new_param_object.get("default")) != None, f"{new_param_name} or {param_name} not passed"
        
        if self.manual_params == True:
            self.passed_params.update(args)

    def onFail(self):
        if self.del_dir_on_fail == True:
            for t_dir in self.temp_dirs:
                file_manager.rmdir(t_dir)
    
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
                __entity.save()

        return __entity
    
    def _collectionFromJson(self, json_data):
        from db.Collection import Collection

        return Collection.fromJson(json_data, self.passed_params)
        
    async def run(self, args):
        pass
    
    async def postRun(self, return_entities):
        for MOVE_ENTITY in return_entities:
            if MOVE_ENTITY.self_name == "entity" and MOVE_ENTITY.file != None:
                MOVE_ENTITY.file.moveTempDir()
    
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
            RETURN_ENTITIES.append(ENTITY)
            #if ENTITY.file != None:
            #    ENTITY.file.moveTempDir()
        
        await self.postRun(return_entities=RETURN_ENTITIES)
        return RETURN_ENTITIES
            
    def describe(self):
        return {
            "id": self.name,
            "category": self.category,
            "hidden": getattr(self, "hidden", False),
            "params": getattr(self, "params", {})
        }

    def describeSource(self, INPUT_ENTITY):
        return {"type": "none", "data": {
            "source": None
        }}

    def allocateTemp(self):
        _dir = storage.makeTemporaryCollectionDir(self.temp_dir_prefix)
        self.temp_dirs.append(_dir)

        return _dir

    async def execute(self, args):
        EXTRACTOR_RESULTS = None

        try:
            EXTRACTOR_RESULTS = await self.run(args=args)
        except Exception as x:
            logger.logException(x, section="Exctractors")
            self.onFail()

            raise x

        return EXTRACTOR_RESULTS
