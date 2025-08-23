from db.Models.Content.StorageUnit import StorageUnit
from db.Models.Content.ContentUnit import ContentUnit
from db.Models.Relations.ContentUnitRelation import ContentUnitRelation
from app.App import logger
from resources.Exceptions import AlreadyLinkedException
import traceback

class LinkManager:
    ever_linked = []

    def __init__(self, parent):
        self.parent = parent

    def __check_if_already_linked_somewhere(self, child):
        for linked_id in self.ever_linked:
            print(self.ever_linked)
            if f"{child.short_name}_{child.uuid}" == linked_id:
                raise AlreadyLinkedException(f"{child.short_name}_{child.uuid} already linked somewhere")

    def link(self, child, revision: bool = False)->bool:
        for frame in traceback.extract_stack():
            print(f"{frame.filename}, {frame.lineno}, {frame.name}, {frame.line}")

        assert self.parent != None and child != None, 'Not found item to link'
        assert self.parent.uuid != None and child.uuid != None, "Can't link: Items probaly not saved"
        assert self.parent.uuid != child.uuid, "Can't link to themselves"

        self.__check_if_already_linked_somewhere(child)

        _link = ContentUnitRelation()
        _link.parent = self.parent.uuid
        _link.child_type = child.__class__.__name__
        _link.child = child.uuid

        if revision == True:
            _link.is_revision = 1

        _link.save()

        # We could to append the actual entity,
        # but i think it will take up a lot of memory so just appending ids

        self.ever_linked.append(f"{child.short_name}_{child.uuid}")

        logger.log(message=f"Linked {self.parent.short_name}_{self.parent.uuid}<->{child.short_name}_{child.uuid}", section=logger.SECTION_LINKAGE, kind = logger.KIND_SUCCESS)

        return True

    def unlink(self, child, revision: bool = False)->bool:
        assert self.parent != None and child != None, 'Not found item to unlink'

        _link = ContentUnitRelation().select().where(ContentUnitRelation.parent == self.parent.uuid).where(ContentUnitRelation.child == child.uuid).where(ContentUnitRelation.child_type == child.__class__.__name__)
        if revision == True:
            _link = _link.where(ContentUnitRelation.is_revision == 1)

        if _link == None:
            return True

        _link.delete()

        logger.log(message=f"Unlinked {self.parent.short_name}_{self.parent.uuid}<->{child.short_name}_{child.uuid}", section=logger.SECTION_LINKAGE, kind = logger.KIND_SUCCESS)

    # Better not to use
    def linksListId(self, by_class = None, revision: bool = False):
        selection = self._linksSelection(by_class, revision)
        ids = []
        for unit in selection:
            ids.append(unit.child)

        return ids

    def linksList(self, by_class = None, revision: bool = False):
        selection = self._linksSelection(by_class, revision)

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

    def _linksSelection(self, by_class = None, revision: bool = False):
        _links = ContentUnitRelation().select().where(ContentUnitRelation.parent == self.parent.uuid)
        if by_class != None:
            _links = _links.where(ContentUnitRelation.child_type == by_class.self_name)

        if revision == True:
            _links = _links.where(ContentUnitRelation.is_revision == 1)
        elif revision == False:
            _links = _links.where(ContentUnitRelation.is_revision == 0)

        return _links

    def injectLinksToJson(self, to_check, linked_list, recurse_level = 0):
        if isinstance(to_check, dict):
            return {key: self.injectLinksToJson(value, linked_list) for key, value in to_check.items()}
        elif isinstance(to_check, list):
            return [self.injectLinksToJson(item, linked_list) for item in to_check]
        elif isinstance(to_check, str):
            try:
                if to_check.startswith("__$|cu_"):
                    got_id = to_check.replace("__$|cu_", "")
                    got_id = int(got_id)

                    for linked in linked_list:
                        if linked.uuid == got_id and linked.self_name == "ContentUnit":
                            return linked.data_with_linked_replacements(recursive=True,recurse_level=recurse_level+1)

                    return to_check
                elif to_check.startswith("__$|su_"):
                    got_id = to_check.replace("__$|su_", "")
                    got_id = int(got_id)
                    for linked in linked_list:
                        if linked.uuid == got_id and linked.self_name == "StorageUnit":
                            return linked.data_with_linked_replacements(recursive=True,recurse_level=recurse_level+1)

                    return to_check
                else:
                    return to_check
            except Exception as __e:
                logger.logException(__e, section="Linkage")
                return to_check
        else:
            return to_check

    def injectLinksToJsonFromInstance(self, recurse_level = 0):
        return self.injectLinksToJson(self.parent.content_json, self.linksList(), recurse_level)
