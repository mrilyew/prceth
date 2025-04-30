from resources.Globals import os, Path, asyncio
from executables.acts.Base import BaseAct
from db.Entity import Entity

class ExportEntity(BaseAct):
    name = 'ExportEntity'
    category = 'export'
    accepts = 'string'

    def declare():
        params = {}
        params["dir"] = {
            "desc_key": "-",
            "type": "string",
        }
        params["export_json"] = {
            "desc_key": "-",
            "type": "bool",
            "default": True,
        }
        params["dir_to_each_entity"] = {
            "desc_key": "-",
            "type": "bool",
            "default": True,
        }
        params["export_linked"] = {
            "desc_key": "-",
            "type": "bool",
            "default": False,
        }
        params["export_json"] = {
            "desc_key": "-",
            "type": "bool",
            "default": False,
        }
        params["prefix_type"] = {
            "desc_key": "-",
            "type": "array",
            "values": ["id", "order"],
            "default": "id"
        }

        return params

    async def execute(self, i: str, args = {}):
        entities_ids = i.split(",")
        entities = []

        __iterator = 0
        dir_to_each_entity = self.passed_params.get("dir_to_each_entity")
        prefix_type = self.passed_params.get("prefix_type")
        export_linked = self.passed_params.get("export_linked")
        export_folder = self.passed_params.get("dir", None)
        export_save_json_to_dir = self.passed_params.get("export_json", True)

        assert export_folder != None, "dir not passed"

        for entity in Entity.get(entities_ids):
            entities.append(entity)
        
        assert len(entities) > 0, "no entities"

        __tasks = []
        dir_path = Path(export_folder)
        if dir_path.is_dir() == False:
            dir_path.mkdir()
        
        for entity in entities:
            entity_dir = str(dir_path)
            if dir_to_each_entity == True:
                match(prefix_type):
                    case "id":
                        entity_dir = os.path.join(str(dir_path), str(entity.id))
                    case "order":
                        entity_dir = os.path.join(str(dir_path), str(__iterator))

            __task = asyncio.create_task(entity.export(Path(entity_dir), linked_params={
                "dir_to_each_entity": dir_to_each_entity,
                "export_linked": export_linked,
                "export_save_json_to_dir": export_save_json_to_dir,
            }))
            __tasks.append(__task)
            __iterator += 1
    
        await asyncio.gather(*__tasks, return_exceptions=False)

        return {
            "destination": export_folder
        }
