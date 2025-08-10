from executables.acts import BaseAct
from declarable.ArgumentsTypes import ServiceInstanceArgument, JsonArgument

class UpdateServiceData(BaseAct):
    @classmethod
    def declare(cls):
        params = {}
        params["service"] = ServiceInstanceArgument({
            "assertion": {
                "not_null": True,
            }
        })
        params["data"] = JsonArgument({
            "assertion": {
                "not_null": True,
            }
        })

        return params

    async def execute(self, i = {}):
        service = i.get('service')
        data = i.get('data')

        assert service != None, 'invalid service'

        service.updateData(data)
        service.save()

        return True
