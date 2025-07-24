from executables.acts import BaseAct
from db.Models.Content.ContentUnit import ContentUnit
from repositories.RepresentationsRepository import RepresentationsRepository
from declarable.ArgumentsTypes import StringArgument, CsvArgument
from db.LinkManager import link_manager
from db.DbFind import db_find
from app.App import logger

class RunRepresentation(BaseAct):
    category = 'Representations'
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
        params["link"] = CsvArgument({
            "base": "ContentUnit",
            "docs": {
                "name": 'run_representation_link_param_name',
            },
            "default": []
        })

        return params

    async def execute(self, i = {}):
        representation_name = i.get('representation')
        links = i.get('link')

        representationClass = RepresentationsRepository().getByName(representation_name)
        assert representationClass != None, "representation not found"
        assert representationClass.canBeExecuted() == True, "representation cannot be executed"

        if representationClass.isConfirmable() != None:
            args = representationClass.validate(i.copy())
            is_confirmed = int(i.get("confirm", "1")) == 1

            if is_confirmed == False:
                pre_execute = representationClass.PreExecute(representationClass)
                new_args_response = await pre_execute.execute(args)
                new_args = new_args_response.get("args")
                new_args_api = {}

                for new_arg in enumerate(new_args):
                    arg_name = new_arg[1]
                    arg = new_args.get(arg_name)

                    if arg_name in pre_execute.args_list:
                        continue

                    new_args_api[arg_name] = arg.out()

                return new_args_api

        __ents = await representationClass.extract(i)
        __all_items = []
        __link_to = ContentUnit.ids(links)

        for item in __ents:
            item.save(force_insert=True)

            for _item in __link_to:
                try:
                    link_manager.link(item, _item)
                except AssertionError as _e:
                    logger.logException(_e, section=logger.SECTION_LINKAGE)

            __all_items.append(item.api_structure())

        return {
            "items": __all_items
        }
