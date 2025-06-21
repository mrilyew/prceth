from db.Models.Content.ContentUnit import ContentUnit
from executables.acts.Base.Base import BaseAct
from repositories.ExtractorsRepository import ExtractorsRepository
from declarable.ArgumentsTypes import StringArgument, BooleanArgument, CsvArgument
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
        params["return_raw"] = BooleanArgument({
            'type': 'bool',
            'default': False,
            'assertion': {
                'not_null': True
            }
        })
        params["append_ids"] = CsvArgument({
            'default': [],
            'assertion': {
                'not_null': True
            }
        })

        return params

    async def execute(self, i = {}):
        extractor_name = i.get('extractor') # Extractor that will be using for export

        assert extractor_name != None, 'extractor not passed'

        append_ids = i.get('append_ids', None)
        colls_list = ContentUnit.ids(append_ids)

        extractor_class = (ExtractorsRepository()).getByName(extractor_name)

        assert extractor_class != None, 'Extractor not found'
        assert extractor_class.canBeExecuted(), 'Extractor is abstract'

        extractor = extractor_class()
        for _col in colls_list:
            if _col.is_collection == True:
                pass

            extractor.add_after.append(_col)

        results = []
        out = []

        extractor.link(results)

        try:
            await extractor.safeExecute(i)

            assert results != None, "Nothing returned"
        except KeyboardInterrupt:
            pass
        except Exception as __ee:
            logger.logException(__ee, section=logger.SECTION_EXTRACTORS)

            raise __ee

        assert len(results) > 0, "nothing exported"

        for __res in results:
            __res.save(force_insert=True)

            for ext in extractor.add_after:
                if ext.is_saved() == False:
                    ext.save(force_insert=True)

                if ext != None:
                    link_manager.link(ext, __res)

            if i.get("return_raw") == True:
                out.append(__res)
            else:
                out.append(__res.api_structure())

        return out
