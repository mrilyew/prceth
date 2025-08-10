from executables.acts import BaseAct
from declarable.ArgumentsTypes import StringArgument, CsvArgument, BooleanArgument, LimitedArgument
from db.Models.Content.ContentUnit import ContentUnit
from pathlib import Path
from app.App import logger
import os

class CopyToDirectory(BaseAct):
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
        params["export_linked"] = BooleanArgument({
            'default': True
        })
        params["save_json"] = BooleanArgument({
            'default': False
        })
        params["export_type"] = LimitedArgument({
            'default': 'to_same_dir',
            'values': ['to_same_dir', 'to_dir_with_id']
        })
        params["prefix"] = LimitedArgument({
            'default': 'id_timestamp',
            'values': ['id', 'id_timestamp', 'order']
        })

        return params

    async def execute(self, i = {}):
        dir_path = Path(i.get('dir'))
        fake_items = i.get('items')
        items = []

        assert dir_path.is_dir(), 'it is not a dir'
        assert len(fake_items) > 0, 'no items to export'

        if dir_path.exists() == False:
            dir_path.mkdir()

        for _item in fake_items:
            if '-' in _item:
                spl_i = _item.split("-")
                for _ri in list(range(int(spl_i[0]), int(spl_i[1]))):
                    items.append('su'+_ri)
        
            if '*' in _item:
                linked = ContentUnit.get(int(_item)).linked_units()
                for lnk in linked:
                    items.append(lnk.id)

            items.append(_item)

        is_async = True
        is_do_export_linked = i.get('export_linked')
        export_type = i.get('export_type')
        prefix_type = i.get('prefix')
        save_json = i.get('save_json')

        items_to_export = ContentUnit.ids(items)
        _iterator = 0

        # i fukin hate this act
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
                case 'id_timestamp':
                    prefix = str(item.id) + '_' + str(item.created_at.timestamp())
                case 'order':
                    prefix = _iterator
                    _iterator += 1

            try:
                await item.export(dir_path=dir_to_export, file_prefix=str(prefix) + '_', save_json=save_json,export_linked=is_do_export_linked)
            except Exception as e:
                logger.logException(e, section='Export!Copy')

        return {
            'count': _iterator,
            'destination': str(dir_path)
        }
