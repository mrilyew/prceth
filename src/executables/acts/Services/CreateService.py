from resources.Globals import ServicesRepository, logger, asyncio, consts, config, Path, utils, file_manager, json
from executables.acts.Base.Base import BaseAct
from db.Service import Service

class CreateService(BaseAct):
    name = 'CreateService'
    category = 'Services'
    docs = {}

    def declare():
        params = {}
        params["class_name"] = {
            "type": "string",
            "assertion": {
                "assert_not_null": True,
            }
        }
        params["display_name"] = {
            "type": "string",
        }
        params["interval"] = {
            "type": "int",
            "default": 60,
            "assertion": {
                "assert_not_null": True,
            }
        }

        return params

    async def execute(self, args={}):
        service_class_name = self.passed_params.get("class_name")
        service_class = (ServicesRepository()).getByName(service_class_name)

        assert service_class != None, "invalid service"

        new_service = Service()
        new_service.service_name = service_class.category + "." + service_class.name
        new_service.display_name = self.passed_params.get("display_name")
        new_service.data = "{}"
        new_service.interval = self.passed_params.get("interval")

        new_service.save()

        return new_service.getApiStructure()
