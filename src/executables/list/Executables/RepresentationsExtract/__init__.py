from executables.acts import Act
from db.Models.Content.ContentUnit import ContentUnit
from executables.representations import Representation
from declarable.Arguments import StringArgument, CsvArgument, ContentUnitArgument
from db.LinkManager import LinkManager
from app.App import logger

keys = {
    "name": {
        "en_US": "Link to",
        "ru_RU": "Привязать к",
    }
}

class Implementation(Act):
    executable_cfg = {
        'free_args': True
    }

    @classmethod
    def declare(cls):
        params = {}
        params["representation"] = StringArgument({
            "assertion": {
                "not_null": True,
            }
        })
        params["link_after"] = CsvArgument({
            "orig": ContentUnitArgument({}),
            "docs": {
                "name": keys.get("name"),
            },
            "default": []
        })

        return params

    async def execute(self, i = {}):
        representation_name = i.get('representation')
        links = i.get('link')

        representation_class = Representation.findByName(representation_name)
        assert representation_class != None, "representation not found"
        assert representation_class.canBeExecuted() == True, "representation cannot be executed"

        if representation_class.isConfirmable() != None:
            args = representation_class.validate(i.copy())
            is_confirmed = int(i.get("confirm", "1")) == 1

            if is_confirmed == False:
                pre_execute = representation_class.PreExecute(representation_class)
                new_args_response = await pre_execute.execute(args)
                new_args = new_args_response.get("args")
                new_args_api = []

                for new_arg in enumerate(new_args):
                    arg_name = new_arg[1]
                    arg = new_args.get(arg_name)

                    if arg_name in pre_execute.args_list:
                        continue

                    new_object = arg.out()
                    new_object["name"] = arg_name

                    new_args_api.append(new_object)

                return {"tab": new_args_api}

        __ents = await representation_class.extract(i)
        __all_items = []
        __link_to = []

        if links != None and len(links) > 0:
            __link_to = ContentUnit.ids(links)

        for item in __ents:
            item.save()

            if __link_to != None and type(__link_to) == list:
                for _item in __link_to:
                    link_manager = LinkManager(item)

                    try:
                        link_manager.link(item, _item)
                    except AssertionError as _e:
                        logger.logException(_e, section=logger.SECTION_LINKAGE)

            __all_items.append(item.api_structure())

        return {
            "items": __all_items
        }
