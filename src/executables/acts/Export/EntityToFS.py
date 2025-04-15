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

        __export_folder_type = args.get("export_type", "full_stop_one_dir")
        __export_folder = args.get("dir", None)
        __export_save_json_to_dir = int(args.get("export_json", 1)) == 1
        __export_prefix = args.get("prefix", "iter")
        __iter = 1

        assert __export_folder != None, "dir not passed"

        for entity in Entity.get(entities_ids):
            entities.append(entity)
        
        assert len(entities) > 0, "no entities"

        match(__export_folder_type):
            case "simple_grouping":
                for LNK_ENTITY in entities:
                    for LINKED_ENTITY in LNK_ENTITY.getLinkedEntities():
                        if LINKED_ENTITY.self_name == "file":
                            continue

                        entities.append(LINKED_ENTITY)

                for EXP_ENTITY in entities: 
                    if EXP_ENTITY.file != None:
                        EXP_ENTITY.file.saveToDir(save_dir=__export_folder,move_type=1)
                
                    if __export_save_json_to_dir == 1:
                        EXP_ENTITY.saveInfoToJson(dir=__export_folder)
            case "full_stop" | "full_stop_unlink" | "full_stop_full_unlink" | "full_stop_one_dir":
                return_entities = []
                dir_path = Path(__export_folder)
                if dir_path.is_dir() == False:
                    dir_path.mkdir()
                
                for entity in entities:
                    entity_dir = Path(os.path.join(str(dir_path), str(entity.id)))
                    if __export_folder_type == "full_stop_one_dir":
                        entity_dir = Path(str(dir_path))
                    
                    linked_dir = Path(os.path.join(str(entity_dir), str(entity.id) + "_linked"))
                    if entity_dir.is_dir() == False:
                        entity_dir.mkdir()

                    if __export_folder_type == "full_stop_unlink" or __export_folder_type == "full_stop_full_unlink" or __export_folder_type == "full_stop_one_dir":
                        linked_dir = entity_dir
                    
                    __file = entity.file
                    if __file != None and type(__file) != list:
                        __prefix = ""
                        if __export_prefix == "id":
                            __prefix = f"{__file.id}_"
                        else:
                            __prefix = f"{__iter}."
                        
                        entity.file.saveToDir(save_dir=entity_dir,move_type=1,prefix=__prefix)
                        __iter += 1
                    
                    return_entities.append(entity)
                    if len(entity.getLinkedEntities()) > 0:
                        try:
                            linked_dir.mkdir()
                        except FileExistsError:
                            pass

                        for LINKED_ENTITY in entity.getLinkedEntities():
                            if LINKED_ENTITY.self_name != "entity":
                                continue

                            linked_entity_dir = Path(os.path.join(str(linked_dir), str(LINKED_ENTITY.id)))
                            if __export_folder_type == "full_stop_full_unlink" or __export_folder_type == "full_stop_one_dir":
                                linked_entity_dir = entity_dir
                            
                            try:
                                linked_entity_dir.mkdir()
                            except FileExistsError:
                                pass

                            return_entities.append(LINKED_ENTITY)
                            
                            ___file = LINKED_ENTITY.file
                            if ___file != None and type(___file) != list:
                                __prefix = ""
                                if __export_prefix == "id":
                                    __prefix = f"{__file.id}_"
                                else:
                                    __prefix = f"{__iter}."
                                
                                ___file.saveToDir(save_dir=linked_entity_dir,move_type=1,prefix=__prefix)
                                __iter += 1
                            if __export_save_json_to_dir:
                                LINKED_ENTITY.saveInfoToJson(dir=str(linked_entity_dir))

                            logger.log(f"_ Exported subentity {LINKED_ENTITY.id}", section="Export",name="success")
                    
                    logger.log(f"Exported entity {entity.id}", section="Export",name="success")
                    if __export_save_json_to_dir:
                        entity.saveInfoToJson(dir=str(entity_dir))
            
        return {
            "destination": __export_folder
        }
