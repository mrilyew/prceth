from resources.Globals import storage, utils, consts, logger, DeclarableArgs, file_manager, config
from db.Entity import Entity

class Executable:
    name = 'base'
    category = 'base'
    passed_params = {}
    temp_dir_prefix = None
    params = {}
    after_save_actions = {}
    temp_dirs = []
    entities_buffer = []
    manual_params = False
    need_preview = False
    already_declared = False
    write_mode = "save_after_creation"
    docs = {
        "description": {
            "name": {
                "en": "No name passed"
            },
            "definition": {
                "en": "No description passed"
            }
        }
    }
    main_args = {}

    @classmethod
    def isRunnable(cls):
        '''
        Is this Executable can be runned or it's technical
        '''
        return cls.category.lower() not in ["template", "base"] and getattr(cls, "hidden", False) == False

    def declare():
        params = {}

        return params

    def recursiveDeclare(self):
        ignore_list = self.main_args.get('ignore', [])

        if getattr(self, "already_declared", False) == True:
            return None

        for __sub_class in self.__class__.__mro__:
            if hasattr(__sub_class, "declare") == False:
                continue

            final_params = {}
            new_params = __sub_class.declare()
            for i, name in enumerate(new_params):
                if name in ignore_list:
                    continue

                final_params[name] = new_params.get(name)

            self.params.update(final_params)

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

    def setPostActions(self, after_save_actions):
        self.after_save_actions = after_save_actions

    def manual(self):
        manual = {}
        __docs = getattr(self, "docs")
        __params = getattr(self, "params")
        __meta = __docs.get("description")

        manual["description"] = __meta
        manual["files"] = getattr(self, "file_containment", {})
        manual["params"] = __params
    
        return manual

    def describe(self):
        rt = {
            "id": self.name,
            "category": self.category,
            "hidden": getattr(self, "hidden", False),
        }
        rt["meta"] = self.manual()

        return rt

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
    
    def fork(self, extractor_name_or_class, args = None):
        from resources.Globals import ExtractorsRepository

        _ext = None
        if type(extractor_name_or_class) == str:
            _ext = (ExtractorsRepository()).getByName(extractor_name_or_class)
        else:
            _ext = extractor_name_or_class

        if _ext == None:
            return None

        ext = _ext(write_mode=self.write_mode,need_preview=self.need_preview)
        if args != None:
            ext.setArgs(args)

        ext.setPostActions(self.after_save_actions)

        return ext

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
        if self.write_mode == "save_after_creation":
            self._entityPostRun(__entity)

        return __entity

    def _collectionFromJson(self, json_data):
        from db.Collection import Collection

        return Collection.fromJson(json_data, self.passed_params)

    def _entityPostRun(self, entity):
        entity.save()
        try:
            entity.file.moveTempDir()
        except:
            pass

        if self.after_save_actions.get("collections", None) != None:
            for coll in self.after_save_actions.get("collections"):
                if coll == None:
                    continue

                try:
                    coll.addItem(entity)
                except:
                    pass

        logger.log(f"Saved entity {str(entity.id)} 👍",section="EntitySaveMechanism",name="success")

    async def postRun(self, return_entities):
        if self.write_mode == "save_after_end":
            try:
                ___ln = len(self.entities_buffer)
                __msg = f"Saving total {str(___ln)} entities;"
                if ___ln > 100:
                    __msg += " do not turn off your computer."
                
                logger.log(__msg,section="EntitySaveMechanism",name="success")
            except Exception as _x:
                print("PostRun:" + str(_x))
                pass

            for unsaved_entity in self.entities_buffer:
                self._entityPostRun(unsaved_entity)
