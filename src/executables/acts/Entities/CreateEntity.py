from resources.Globals import os, logger, asyncio, consts, config, Path, utils, ExtractorsRepository, json, often_params
from executables.acts.Base.Base import BaseAct
from db.Collection import Collection

class CreateEntity(BaseAct):
    name = 'CreateEntity'
    category = 'Entities'
    docs = {
        "description": {
            "name": {
                "ru": "Создать запись",
                "en": "Create entity"
            },
            "definition": {
                "ru": "Создаёт запись из переданного экстрактора (параметр \"i\")",
                "en": "Creates new entity via provided extractor (\"i\" arg)"
            }
        },
        "returns": {
            "end": True,
            "type": "list",
        }
    }
    manual_params = True

    def declare():
        params = {}
        params["e"] = {
            "type": "string",
            "assertion": {
                "assert_not_null": True
            }
        }
        params["return_raw"] = often_params.get("return_raw")

        return params

    async def execute(self, args={}):
        __extractor_input_name = self.passed_params.get("e") # Extractor that will be using for export
        assert __extractor_input_name != None, "e not passed"

        collection_id = self.passed_params.get("collection_id", None) # Collection id to where entity will added
        __create_need_collection = int(self.passed_params.get("create_need_collection", "1"))
        __export_to_db = True
        __del_dir_on_fail = int(self.passed_params.get("del_dir", "1")) == 1 and __export_to_db == True
        __write_mode = self.passed_params.get("write_mode", "save_after_creation")
        if __write_mode not in ["save_after_creation", "save_after_end"]:
            __write_mode = "save_after_creation"

        INSTANCE_CLASS = (ExtractorsRepository()).getByName(extractor_name=__extractor_input_name)

        assert INSTANCE_CLASS != None, "Extractor not found"

        EXTRACTOR_INSTANCE = INSTANCE_CLASS(del_dir_on_fail=__del_dir_on_fail,write_mode=__write_mode)
        EXTRACTOR_INSTANCE.setArgs(args)
        EXTRACTOR_RESULTS = None
        EXTRACTOR_COLLECTIONS = []

        if EXTRACTOR_INSTANCE.isCreatesCollection() and __create_need_collection == 1:
            __new_coll = EXTRACTOR_INSTANCE._collection()
            EXTRACTOR_COLLECTIONS.append(EXTRACTOR_INSTANCE._collectionFromJson(__new_coll))

        __coll = None
        if collection_id != None:
            __coll = Collection.get(collection_id)
            if __coll == None:
                logger.log(section="EntitySaveMechanism", name="error", message="Collection not found, not adding.")
            else:
                EXTRACTOR_COLLECTIONS.append(__coll)

        EXTRACTOR_INSTANCE.setPostActions({
            "collections": EXTRACTOR_COLLECTIONS
        })

        try:
            EXTRACTOR_RESULTS = await EXTRACTOR_INSTANCE.execute(args)
            assert EXTRACTOR_RESULTS != None, "Nothing returned"
        except KeyboardInterrupt:
            pass
        except Exception as __ee:
            logger.log(message=f"Extractor {__extractor_input_name} returned error: {str(__ee)}",silent=True)
            raise __ee

        ENTITIES_COUNT = len(EXTRACTOR_RESULTS.get("entities"))
        assert ENTITIES_COUNT > 0, "nothing exported"

        RETURN_ENTITIES = []
        for ENTITY in EXTRACTOR_RESULTS.get("entities"):
            RETURN_ENTITIES.append(ENTITY)
            for _ENTITY in ENTITY.getLinkedEntities():
                RETURN_ENTITIES.append(_ENTITY)

        await EXTRACTOR_INSTANCE.postRun(return_entities=RETURN_ENTITIES)

        # __export_folder will be run on frontend

        __RETURN_ENTITIES = []
        for RETURN_ENTITY in RETURN_ENTITIES:
            if self.passed_params.get("return_raw") == True:
                __RETURN_ENTITIES.append(RETURN_ENTITY)
            else:
                __RETURN_ENTITIES.append(RETURN_ENTITY.getApiStructure())

        return __RETURN_ENTITIES
