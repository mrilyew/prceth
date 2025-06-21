from db.Models.Content.ContentUnit import ContentUnit
from db.Models.Content.StorageUnit import StorageUnit
from utils.MainUtils import dump_json

class DbInsert():
    @staticmethod
    def contentFromJson(json_input):
        out = ContentUnit()

        display_name = json_input.get("display_name", json_input.get('name'))
        description = json_input.get('description')
        source = json_input.get('source')
        extractor_name = json_input.get("extractor")
        representation_name = json_input.get("representation")
        declared_created_at = json_input.get("declared_created_at")

        is_unlisted = json_input.get("unlisted", False)
        is_collection = json_input.get("is_collection", False)
        is_save = json_input.get('save_model', False)
        is_make_thumbnail = json_input.get('make_thumbnail', True)

        content = json_input.get("content")
        links_list = json_input.get("links")
        links_main = json_input.get("links_main")

        if content != None:
            out.content = dump_json(content)

        if is_unlisted == True:
            out.unlisted = 1

        out.extractor = extractor_name
        out.representation = representation_name

        if display_name != None:
            out.display_name = display_name
        else:
            out.display_name = "N/A"

        if description != None:
            out.description = description
        if source != None:
            out.set_source(source)
        if declared_created_at != None:
            if getattr(declared_created_at, 'timestamp', None) != None:
                out.declared_created_at = int(declared_created_at.timestamp())
            else:
                out.declared_created_at = int(declared_created_at)

        # out.indexation_content_string = json.dumps(json_values_to_string(content), ensure_ascii=False).replace('None', '').replace('  ', ' ').replace('\n', ' ').replace(" ", "")

        if is_collection == True:
            out.is_collection = True

        '''
        if is_make_thumbnail == True:
            thmb = out.make_thumbnail({}, json_input.get('representation_class', None))
            if thmb != None:
                fnl = []
                for t in thmb:
                    fnl.append(t.data)

                out.thumbnail = dump_json(fnl)
        '''

        if links_list != None and links_main != None:
            _l = links_list[int(links_main)]
            out.storage_unit = _l.uuid

        # Not saving cuz it may be sifted in future
        if is_save == True:
            out.save(force_insert=True)

        if links_list != None:
            for item in links_list:
                out.link_queue.append(item)

        return out

    @staticmethod
    def storageUnit():
        return StorageUnit()

db_insert = DbInsert()
