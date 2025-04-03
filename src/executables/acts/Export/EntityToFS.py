from resources.Globals import consts, os, Path, datetime, utils, logger, file_manager, zipfile, json
from executables.acts.Base import BaseAct
from db.Entity import Entity

class EntityToFS(BaseAct):
    name = 'EntityToFS'
    category = 'export'
    accepts = 'string'

    def execute(self, i: str, args):
        entities_ids = i.split(",")
        entities = []
        LINKED_ENTITY = []

        __export_folder_type = args.get("export_type", "grouping")
        __export_folder = args.get("dir", None)
        __export_save_json_to_dir = int(args.get("export_json", 1))
        __append_entity_id_to_start = True

        assert __export_folder != None, "dir not passed"

        for entity in Entity.get(entities_ids):
            entities.append(entity)
        
        for EXP_ENTITY in entities:
            match(__export_folder_type):
                case "simple_grouping":
                    for LINKED_ENTITY in EXP_ENTITY.getLinkedEntities():
                        entities.append(LINKED_ENTITY)
                    
                    if EXP_ENTITY.file != None:
                        EXP_ENTITY.file.saveToDir(use_upload_name=True,save_dir=__export_folder,move_type=1,append_entity_id_to_start=__append_entity_id_to_start==1)
                
                    if __export_save_json_to_dir == 1:
                        EXP_ENTITY.saveInfoToJson(dir=__export_folder)
                case "grouping":
                    RETURN_ENTITIES = EXP_ENTITY.fullStop(move_dir=__export_folder,save_to_json=__export_save_json_to_dir==1)
            '''case _: # "rename"
                for ENTITY in entities:
                    for LINKED_ENTITY in ENTITY.getLinkedEntities():
                        RETURN_ENTITIES.append(LINKED_ENTITY)
                
                if EXP_ENTITY.file != None:
                    EXP_ENTITY.file.saveToDir(use_upload_name=True,save_dir=__export_folder,move_type=0,append_entity_id_to_start=__append_entity_id_to_start==1)

                if __export_save_json_to_dir == 1:
                    EXP_ENTITY.saveInfoToJson(dir=__export_folder)'''
        
        return {
            "destination": __export_folder
        }
