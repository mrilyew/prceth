from db.Models.Content.ContentUnit import ContentUnit
from db.Models.Content.StorageUnit import StorageUnit
from utils.MainUtils import dump_json
import json

class DbInsert():
    @staticmethod
    def contentFromJson(json_input, representation_class = None, thumbnail_params = {})->ContentUnit:
        display_name = json_input.get("display_name", json_input.get('name'))
        description = json_input.get('description')
        source = json_input.get('source')
        extractor_name = json_input.get("extractor")
        declared_created_at = json_input.get("declared_created_at")
        representation_class_name = None

        if representation_class != None:
            representation_class_name = representation_class.full_name()

        is_unlisted = json_input.get("unlisted", False)
        is_collection = json_input.get("is_collection", False)
        is_save = json_input.get('save_model', False)
        is_make_thumbnail = json_input.get('make_thumbnail', True)

        content = json_input.get("content")
        links_list = json_input.get("links")
        link_main = json_input.get("link_main") # index of main link

        # Making out
        out = ContentUnit()

        if content != None:
            out.content = dump_json(content)

        out.extractor = extractor_name
        out.representation = representation_class_name

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

        if is_unlisted == True:
            out.unlisted = 1

        # we can't link items be4 getting its id
        if links_list != None:
            for item in links_list:
                out.link_queue.append(item)

            if link_main != None:
                _l = links_list[int(link_main)]

                if _l != None:
                    out.storage_unit = _l.uuid

        # making thumbnail
        if is_make_thumbnail == True:
            if getattr(representation_class, "Thumbnail", None) != None:
                thumb_class = representation_class.Thumbnail(representation_class)
                thumb_out = thumb_class.create(out, thumbnail_params)

                out.set_thumbnail(thumb_out)

        # Not saving cuz it may be sifted in future
        if is_save == True:
            out.save(force_insert=True)

        return out

    @staticmethod
    def storageUnit():
        return StorageUnit()

db_insert = DbInsert()
