from resources.Globals import storage, utils, consts, logger, DeclarableArgs, file_manager
from db.Entity import Entity

class Executable:
    name = 'base'
    category = 'template'
    passed_params = {}
    temp_dir_prefix = None
    params = {}
    after_save_actions = {}
    temp_dirs = []
    entities_buffer = []
    manual_params = False
    need_preview = False
    already_declared = False
    write_mode = 2
    docs = {
        "description": {
            "name": {
                "en": "Executable root"
            },
            "definition": {
                "en": "Executable root description"
            }
        }
    }

    def declare():
        params = {}

        return params

    def recursiveDeclare(self):
        if getattr(self, "already_declared", False) == True:
            return None

        for __sub_class in self.__class__.__mro__:
            if hasattr(__sub_class, "declare") == False:
                continue

            new_params = __sub_class.declare()
            self.params.update(new_params)

        self.already_declared = True

    def setArgs(self, args):
        self.params = {}

        # Catching params from parent executables
        self.recursiveDeclare()

        MAX_OUTPUT_CHECK_PARAMS = self.params
        if MAX_OUTPUT_CHECK_PARAMS == None:
            return

        decl = DeclarableArgs(MAX_OUTPUT_CHECK_PARAMS, args)
        self.passed_params.update(decl.dict())

        if self.manual_params == True:
            self.passed_params.update(args)

    def describe(self):
        return {
            "id": self.name,
            "category": self.category,
            "hidden": getattr(self, "hidden", False),
            "params": getattr(self, "params", {})
        }

    def allocateTemp(self):
        _dir = storage.makeTemporaryCollectionDir(self.temp_dir_prefix)
        self.temp_dirs.append(_dir)

        return _dir

    def removeAllocatedTemp(self, dir_name):
        try:
            file_manager.rmdir(dir_name)
        except Exception:
            logger.logException(dir_name, "Extractor", silent=False)

    def mainTempDir(self):
        _dir = consts.get("tmp")

        return _dir

    async def _execute_sub(self, extractor, extractor_params, array_link):
        try:
            extractor.setArgs(extractor_params)
            executed = await extractor.execute({})
            for ___item in executed.get("entities"):
                array_link.append(___item)
        except Exception as ___e:
            logger.logException(input_exception=___e,section="Extractor",silent=False)
            pass

    # TODO убрать?
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
                __entity.preview = utils.dump_json(thumb_result)

        self.entities_buffer.append(__entity)
        if self.write_mode == 2:
            __entity.save()
            logger.log(f"Saved entity {str(__entity.id)} 👍",section="EntitySaveMechanism",name="success")

        try:
            __entity.file.moveTempDir()
        except:
            pass

        if self.after_save_actions.get("collections", None) != None:
            for coll in self.after_save_actions.get("collections"):
                if coll == None:
                    continue

                try:
                    coll.addItem(__entity)
                except:
                    pass

        return __entity

    def _collectionFromJson(self, json_data):
        from db.Collection import Collection

        return Collection.fromJson(json_data, self.passed_params)
