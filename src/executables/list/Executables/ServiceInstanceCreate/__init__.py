from executables.acts import Act
from executables.services import Service
from db.Models.Instances.ServiceInstance import ServiceInstance
from declarable.Arguments import StringArgument, IntArgument

class Implementation(Act):
    executable_cfg = {
        'free_args': True
    }

    @classmethod
    def declare(cls):
        params = {}
        params["class"] = StringArgument({
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
        display_name = i.get('display_name')
        interval = i.get('interval')
        service_class_name = i.get('class')

        service_class = Service.findByName(service_class_name)

        assert service_class != None, "invalid service"

        new_service = ServiceInstance()
        new_service.service_name = service_class.full_name()
        new_service.display_name = display_name
        new_service.data = "{}"

        if interval != None:
            new_service.interval = interval

        new_service.save()

        return new_service.api_structure()
