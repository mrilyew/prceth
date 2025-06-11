from db.ContentUnit import ContentUnit
from executables.acts.Base.Base import BaseAct
from repositories.ServicesRepository import ServicesRepository
from db.ServiceInstance import ServiceInstance
from declarable.ArgumentsTypes import StringArgument, IntArgument

class NewService(BaseAct):
    category = 'Executables'
    executable_cfg = {
        'free_args': True
    }

    def declare():
        params = {}
        params["class_name"] = StringArgument({
            "assertion": {
                "not_null": True,
            }
        })
        params["display_name"] = StringArgument({})
        params["interval"] = IntArgument({
            "default": 60,
            "assertion": {
                "not_null": True,
            }
        })

        return params

    async def execute(self, i = {}):
        service_class_name = i.get('class_name')
        service_class = (ServicesRepository()).getByName(service_class_name)

        assert service_class != None, "invalid service"

        new_service = ServiceInstance()
        new_service.service_name = service_class.full_name()
        new_service.display_name = i.get('display_name')
        new_service.data = "{}"

        if i.get('interval') != None:
            new_service.interval = i.get('interval')

        new_service.save()

        return new_service.api_structure()
