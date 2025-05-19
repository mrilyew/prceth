from resources.Globals import config, ExtractorsRepository, ActsRepository, ServicesRepository, logger
from resources.Exceptions import NotPassedException, ExtractorException
from db.Collection import Collection

class Api():
    def __init__(self):
        self.ctx = "cli"
    def setOption(self, option_name, option_value):
        config.set(option_name, option_value)
        return True
    def getOption(self, option_name):
        return config.get(option_name)
    def resetOptions(self):
        return config.reset()
    def getAllOptions(self):
        return config.data
    async def uploadEntity(self, __INPUT_ARGS):
        if 'i' not in __INPUT_ARGS:
            raise NotPassedException('--i not passed')

        __extractor_input_name = __INPUT_ARGS.get("i") # Extractor that will be using for export
        collection_id = __INPUT_ARGS.get("collection_id", None) # Collection id to where entity will added
        __create_need_collection = int(__INPUT_ARGS.get("create_need_collection", "1"))
        __export_to_db = True
        __del_dir_on_fail = int(__INPUT_ARGS.get("del_dir", "1")) == 1 and __export_to_db == True
        __write_mode = __INPUT_ARGS.get("write_mode", "save_after_creation")
        if __write_mode not in ["save_after_creation", "save_after_end"]:
            __write_mode = "save_after_creation"

        INSTANCE_CLASS = (ExtractorsRepository()).getByName(extractor_name=__extractor_input_name)
        assert INSTANCE_CLASS != None, "Extractor not found"

        EXTRACTOR_INSTANCE = INSTANCE_CLASS(del_dir_on_fail=__del_dir_on_fail,write_mode=__write_mode)
        EXTRACTOR_INSTANCE.setArgs(__INPUT_ARGS)
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
            EXTRACTOR_RESULTS = await EXTRACTOR_INSTANCE.execute(__INPUT_ARGS)
            if EXTRACTOR_RESULTS == None:
                raise Exception("Nothing returned")
        except KeyboardInterrupt:
            pass
        except Exception as __ee:
            logger.log(message=f"Extractor {__extractor_input_name} returned error: {str(__ee)}",silent=True)
            raise __ee
        
        ENTITIES_COUNT = len(EXTRACTOR_RESULTS.get("entities"))
        if ENTITIES_COUNT < 1:
            raise ExtractorException("nothing exported")

        RETURN_ENTITIES = []
        for ENTITY in EXTRACTOR_RESULTS.get("entities"):
            RETURN_ENTITIES.append(ENTITY)
            for _ENTITY in ENTITY.getLinkedEntities():
                RETURN_ENTITIES.append(_ENTITY)
        
        await EXTRACTOR_INSTANCE.postRun(return_entities=RETURN_ENTITIES)

        # __export_folder will be run on frontend

        return RETURN_ENTITIES
    async def runAct(self, params):
        assert "i" in params, "i not passed"

        __act_name = params.get("i")
        __act_res = ActsRepository().getByName(act_name=__act_name)
        assert __act_res != None, "act not found"

        OUT_ACT = __act_res()
        OUT_ACT.setArgs(params)

        ACT_F = await OUT_ACT.execute(args=params)

        return {"results": ACT_F}
    def runService(self, params):
        if 'i' not in params:
            raise NotPassedException('--i not passed')

        service_name = params.get("i")
        if service_name == None:
            raise ValueError("--i is not passed")

        (ServicesRepository()).run(args=params,service_name=service_name)

        return True

api = Api()
