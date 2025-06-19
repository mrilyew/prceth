from executables.acts.Base.Base import BaseAct
from declarable.ArgumentsTypes import StringArgument, CsvArgument, LimitedArgument
from db.Models.Content.StorageUnit import StorageUnit
from pathlib import Path
from app.App import logger
import os

class CopyStorageUnitsToDirectory(BaseAct):
    category = 'Metamorphosis'

    @classmethod
    def declare(cls):
        params = {}
        params["dir"] = StringArgument({
            'assertion': {
                'not_null': True
            }
        })
        params["items"] = CsvArgument({
            'assertion': {
                'not_null': True
            }
        })
        params["export_type"] = LimitedArgument({
            'default': 'to_same_dir',
            'values': ['to_same_dir', 'to_dir_with_id']
        })
        params["prefix"] = LimitedArgument({
            'default': 'id',
            'values': ['id', 'order']
        })

        return params

    async def execute(self, i = {}):
        dir_path = Path(i.get('dir'))
        items = i.get('items')

        assert dir_path.is_dir(), 'it is not a dir'
        if dir_path.exists() == False:
            dir_path.mkdir()

        export_type = i.get('export_type')
        prefix_type = i.get('prefix')
        save_json = i.get('save_json')

        items_to_export = StorageUnit.ids(items)
        _iterator = 0

        for item in items_to_export:
            dir_to_export = ""
            prefix = ""
            if export_type == 'to_same_dir':
                dir_to_export = dir_path
            elif export_type == 'to_dir_with_id':
                dir_to_export = os.path.join(dir_path, item.id)

            match(prefix_type):
                case 'id':
                    prefix = item.id
                case 'order':
                    prefix = _iterator
                    _iterator += 1

            try:
                await item.export(dir_path=dir_to_export, file_prefix=str(prefix) + '_')
            except Exception as e:
                logger.logException(e, section='Export!CopyStorageUnits')

        return {
            'count': _iterator,
            'destination': str(dir_path)
        }
