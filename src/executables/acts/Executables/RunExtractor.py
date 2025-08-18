from db.Models.Content.ContentUnit import ContentUnit
from executables.acts import BaseAct
from repositories.ExtractorsRepository import ExtractorsRepository
from declarable.ArgumentsTypes import StringArgument, ContentUnitArgument, CsvArgument
from db.LinkManager import LinkManager
from app.App import logger
import asyncio

class RunExtractor(BaseAct):
    executable_cfg = {
        'free_args': True
    }

    @classmethod
    def declare(cls):
        params = {}
        params["extractor"] = StringArgument({
            "assertion": {
                "not_null": True
            }
        })
        params["link_after"] = CsvArgument({
            "orig": ContentUnitArgument({}),
            "docs": {
                "name": "acts.run.link.name",
            },
            'default': [],
        })

        return params

    async def execute(self, i = {}):
        extractor_name = i.get('extractor') # Extractor that will be using for export
        append_ids = i.get('link_after')
        extractor_class = (ExtractorsRepository()).getByName(extractor_name)
        results = []
        out = []

        assert extractor_class != None, 'Extractor not found'
        assert extractor_class.canBeExecuted(), 'Extractor is abstract'

        relations = ContentUnit.ids(append_ids)
        extractor = extractor_class()

        for _rel in relations:
            if _rel.is_collection == True:
                extractor.link_after_add(_rel)

        extractor.subscribe(results)

        def __onerror(exc):
            logger.logException(exc, section=logger.SECTION_EXTRACTORS)

        extractor.add_hook("error", __onerror)

        try:
            await extractor.safeExecute(i)

            assert results != None, "Nothing returned"
        except KeyboardInterrupt:
            pass
        except Exception as __ee:
            if extractor != None:
                print(getattr(extractor, "trigger_hooks", None))
                await extractor.trigger_hooks("error", __ee)

            raise __ee

        assert len(results) > 0, "nothing exported"

        for item in results:
            if item.is_saved() == False:
                item.save(force_insert=True)

            for ext in extractor.link_after:
                if ext.is_saved() == False:
                    ext.save(force_insert=True)

                try:
                    link_manager = LinkManager(ext)
                    link_manager.link(item)
                except AssertionError as _e:
                    logger.logException(_e, section=logger.SECTION_LINKAGE)

            out.append(item.api_structure())

        return {
            "items": out
        }
