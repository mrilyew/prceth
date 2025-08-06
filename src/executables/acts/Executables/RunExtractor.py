from db.Models.Content.ContentUnit import ContentUnit
from executables.acts import BaseAct
from repositories.ExtractorsRepository import ExtractorsRepository
from declarable.ArgumentsTypes import StringArgument, ContentUnitArgument, CsvArgument
from db.LinkManager import link_manager
from app.App import logger

class RunExtractor(BaseAct):
    category = 'Executables'
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
        params["link"] = CsvArgument({
            "orig": ContentUnitArgument({}),
            "docs": {
                "name": 'run_representation_link_param_name',
            },
            'default': [],
        })

        return params

    async def execute(self, i = {}):
        extractor_name = i.get('extractor') # Extractor that will be using for export
        append_ids = i.get('link')
        extractor_class = (ExtractorsRepository()).getByName(extractor_name)
        results = []
        out = []

        assert extractor_class != None, 'Extractor not found'
        assert extractor_class.canBeExecuted(), 'Extractor is abstract'

        relations = ContentUnit.ids(append_ids)
        extractor = extractor_class()

        for _rel in relations:
            if _rel.is_collection == True:
                extractor.add_after.append(_rel)

        extractor.link(results)

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
                await extractor.trigger_hooks("error", __ee)

            raise __ee

        assert len(results) > 0, "nothing exported"

        for __res in results:
            __res.save(force_insert=True)

            for ext in extractor.add_after:
                if ext.is_saved() == False:
                    ext.save(force_insert=True)

                if ext != None:
                    try:
                        link_manager.link(ext, __res)
                    except AssertionError as _e:
                        logger.logException(_e, section=logger.SECTION_LINKAGE)

            out.append(__res.api_structure())

        return out
