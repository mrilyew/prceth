from executables.services.Base.Base import BaseService
from resources.Descriptions import descriptions
from app.App import logger
from db.ContentUnit import ContentUnit

class BaseDeclaredAtDependent(BaseService):
    category = 'Base'
    pass_params = {}
    add_after = None
    colls_list = []

    def declare():
        params = {}
        params["append_ids"] = {
            'type': 'csv',
            'default': [],
        }
        params["date_offset"] = {
            "docs": {
                "definition": descriptions.get('__data_offset_service')
            },
            "type": "string",
            "assertion": {
                "not_null": True,
            },
        }

        return params

    async def execute(self, i = {}):
        append_ids = self.config.get('append_ids', [])

        if self.add_after == None:
            self.add_after = []
            colls_list = ContentUnit.ids(append_ids)

            for col in colls_list:
                self.add_after.append(col)

        linked_dict = []

        extractor_instance = self.regular_extractor()
        extractor_instance.link(linked_dict)

        await extractor_instance.safeExecute(self.pass_params)

        logger.log(message=f"Got total {len(linked_dict)} items",kind='message',section='RegularDeclaredAtChecker')

        list_items = []
        check_dates = []

        date_offset = int(self.config.get("date_offset", 0))

        for item in linked_dict:
            item_created = int(item.declared_created_at)

            if item_created > date_offset:
                item.save()

                list_items.append(item)

                check_dates.append(int(item_created))

        logger.log(message=f"Totally {len(list_items)} new items",kind='success',section='RegularDeclaredAtChecker')

        if len(list_items) > 0:
            new_offset = max(check_dates)

            logger.log(message=f"Changed date offset {date_offset}->{new_offset}",kind='message',section='RegularDeclaredAtChecker')

            self.config['date_offset'] = new_offset
            self.service_object.updateData(self.config)
            self.service_object.save()

        for item in list_items:
            for ext in self.add_after:
                if ext != None:
                    ext.addLink(item)
