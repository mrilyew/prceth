from executables.acts.Base.Base import BaseAct
from app.App import app, db_connection
from repositories.RepresentationsRepository import RepresentationsRepository
from declarable.ArgumentsTypes import StringArgument, ServiceInstanceArgument, JsonArgument
from resources.Descriptions import descriptions

class UpdateServiceData(BaseAct):
    category = 'Representations'
    docs = {
        "name": descriptions.get('__update_service_data'),
        "definition": descriptions.get('__updates_service_data_not_changes')
    }

    @classmethod
    def declare(cls):
        params = {}
        params["service"] = ServiceInstanceArgument({
            "docs": {
                "definition": descriptions.get('__service_id_where_updata_data')
            },
            "assertion": {
                "not_null": True,
            }
        })
        params["data"] = JsonArgument({
            "docs": {
                "definition": descriptions.get('__service_new_data')
            },
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

        return {
            'success': 1
        }
