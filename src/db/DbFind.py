from db.Models.Content.ContentUnit import ContentUnit
from db.Models.Content.StorageUnit import StorageUnit

class DbFind:
    @staticmethod
    def fromStringDifferentTypes(i):
        els = []
        out = []
        if type(i) == str:
            els = i.split(',')
        else:
            els = i

        for el in els:
            interm_out = None
            el_type, el_id = el.split('_')

            match(el_type):
                case 'cu' | 'contentunit':
                    interm_out = ContentUnit.select().where(ContentUnit.uuid == el_id).first()
                case 'su' | 'storageunit' | 'stouni':
                    interm_out = StorageUnit.select().where(StorageUnit.uuid == el_id).first()

            out.append(interm_out)

        return out

db_find = DbFind()
