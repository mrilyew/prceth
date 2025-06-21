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

        logger.log(message=f"Linked {parent.short_name}_{parent.uuid}<->{child.short_name}_{child.uuid}", section=logger.SECTION_LINKAGE, kind = logger.KIND_SUCCESS)

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

        logger.log(message=f"Unlinked {parent.short_name}_{parent.uuid}<->{child.short_name}_{child.uuid}", section=logger.SECTION_LINKAGE, kind = logger.KIND_SUCCESS)

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

    @classmethod
    def injectLinksToJson(cls, json_input, linked_list, recurse_level = 0):
        if isinstance(json_input, dict):
            return {key: cls.injectLinksToJson(value, linked_list) for key, value in json_input.items()}
        elif isinstance(json_input, list):
            return [cls.injectLinksToJson(item, linked_list) for item in json_input]
        elif isinstance(json_input, str):
            try:
                if "__$|cu_" in json_input:
                    got_id = json_input.replace("__$|cu_", "")
                    for linked in linked_list:
                        if linked.uuid == got_id and linked.self_name == "ContentUnit":
                            return linked.formatted_data(recursive=True,recurse_level=recurse_level+1)
                        else:
                            return json_input
                elif "__$|su_" in json_input:
                    got_id = json_input.replace("__$|su_", "")
                    for linked in linked_list:
                        if linked.uuid == got_id and linked.self_name == "StorageUnit":
                            return linked.formatted_data(recursive=True,recurse_level=recurse_level+1)
                        else:
                            return json_input
                else:
                    return json_input
            except Exception as __e:
                return json_input
        else:
            return json_input

    @classmethod
    def injectLinksToJsonFromInstance(cls, i, recurse_level = 0):
        return cls.injectLinksToJson(i.json_content, cls.linksList(i), recurse_level)

link_manager = LinkManager()
