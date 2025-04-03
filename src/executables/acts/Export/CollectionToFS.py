from resources.Globals import consts, os, Path, datetime, utils, logger, file_manager, zipfile, json
from executables.acts.Base import BaseAct
from repositories.Acts import Acts
from db.Collection import Collection

class CollectionToFS(BaseAct):
    name = 'CollectionToFS'
    category = 'export'
    accepts = 'string'

    def execute(self, i: str, args):
        collection_ids = str(i).split(",")
        entities = []
        entity_ids = []
        collections = []
        for coll_id in collection_ids:
            collections.append(Collection.get(int(coll_id)))

        for coll in collections:
            for __entity in coll.getItems(limit=None):
                if __entity.self_name == "collection": # TODO
                    continue
                entities.append(__entity)
        for __entity in entities:
            entity_ids.append(str(__entity.id))
        
        fs_act = (Acts().getByName(act_name="Export.EntityToFS"))()
        export_res = fs_act.execute(i=",".join(entity_ids),args=args)

        DESTINATION_DIR = export_res.get("destination")
        for coll in collections:
            coll.saveInfoToJson(dir=DESTINATION_DIR)

        return {
            "destination": DESTINATION_DIR
        }
