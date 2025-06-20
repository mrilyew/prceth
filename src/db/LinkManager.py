from db.Models.Content.StorageUnit import StorageUnit
from db.Models.Content.ContentUnit import ContentUnit
from db.Models.Relations.ContentUnitRelation import ContentUnitRelation
from app.App import logger

class LinkManager:
    @staticmethod
    def link(parent: ContentUnit, child, revision: bool = False)->bool:
        assert parent != None and child != None, 'Not found item to link'

        _link = ContentUnitRelation()
        _link.parent = parent.uuid
        _link.child_type = child.__class__.__name__
        _link.child = child.uuid

        if revision == True:
            _link.is_revision = 1

        _link.save()

        logger.log(message=f"Linked {parent.short_name}_{parent.uuid}<->{child.short_name}_{child.uuid}", section='DB', kind = logger.KIND_SUCCESS)

        return True

    @staticmethod
    def unlink(parent, child, revision: bool = False)->bool:
        assert parent != None and child != None, 'Not found item to unlink'

        _link = ContentUnitRelation().select().where(ContentUnitRelation.parent == parent.uuid).where(ContentUnitRelation.child == child.uuid).where(ContentUnitRelation.child_type == child.__class__.__name__)
        if revision == True:
            _link = _link.where(ContentUnitRelation.is_revision == 1)

        if _link == None:
            return True

        _link.delete()

        logger.log(message=f"Unlinked {parent.short_name}_{parent.uuid}<->{child.short_name}_{child.uuid}", section='DB', kind = logger.KIND_SUCCESS)

    # Better not to use
    @staticmethod
    def linksListId(parent, by_class = None, revision: bool = False):
        selection = LinkManager._linksSelection(parent, by_class, revision)
        ids = []
        for unit in selection:
            ids.append(unit.child)

        return ids

    @staticmethod
    def linksList(parent, by_class = None, revision: bool = False):
        selection = LinkManager._linksSelection(parent, by_class, revision)

        c_s = []
        s_s = []

        for sel in selection:
            if sel.child_type == 'ContentUnit':
                c_s.append(sel.child)
            else:
                s_s.append(sel.child)

        c_s_units = ContentUnit.select().where(ContentUnit.uuid << c_s)
        s_s_units = StorageUnit.select().where(StorageUnit.uuid << s_s)

        ret = []
        for unit in c_s_units:
            ret.append(unit)
        for unit in s_s_units:
            ret.append(unit)

        return ret

    @staticmethod
    def _linksSelection(parent, by_class = None, revision: bool = False):
        _links = ContentUnitRelation().select().where(ContentUnitRelation.parent == parent.uuid)
        if by_class != None:
            _links = _links.where(ContentUnitRelation.child_type == by_class.self_name)

        if revision == True:
            _links = _links.where(ContentUnitRelation.is_revision == 1)

        return _links

link_manager = LinkManager()
