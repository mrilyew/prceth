from db.Models.Content.ContentUnit import ContentUnit
from db.Models.Content.StorageUnit import StorageUnit
from utils.MainUtils import dump_json, parse_json

class DbInsert():
    @staticmethod
    def contentFromJson(json_input):
        out = ContentUnit()

        content = json_input.get("content")
        if content != None:
            out.content = dump_json(content)

        if json_input.get("unlisted", None) == True:
            out.unlisted = 1

        out.extractor = json_input.get("extractor")
        out.representation = json_input.get("representation")

        if json_input.get("display_name") != None:
            out.display_name = json_input.get('display_name')
        else:
            if json_input.get("name") == None:
                if json_input.get("file") == None:
                    out.display_name = "N/A"
            else:
                out.display_name = json_input.get('name')

        if json_input.get("description") != None:
            out.description = json_input.get('description')
        if json_input.get("source") != None:
            out.set_source(json_input.get('source'))
        if json_input.get("declared_created_at") != None:
            if getattr(json_input.get("declared_created_at"), 'timestamp', None) != None:
                out.declared_created_at = int(json_input.get("declared_created_at").timestamp())
            else:
                out.declared_created_at = int(json_input.get("declared_created_at"))

        # out.indexation_content_string = json.dumps(json_values_to_string(content), ensure_ascii=False).replace('None', '').replace('  ', ' ').replace('\n', ' ').replace(" ", "")

        if json_input.get('is_collection', False) == True:
            out.is_collection = True

        if json_input.get('make_thumbnail', False) == True:
            thmb = out.make_thumbnail({}, json_input.get('representation_class', None))
            if thmb != None:
                fnl = []
                for t in thmb:
                    fnl.append(t.data)

                out.thumbnail = dump_json(fnl)

        # Not saving cuz it may be sifted in future
        if json_input.get('save_model', False) == True:
            out.save(force_insert=True)

        if json_input.get("links") != None:
            for item in json_input.get("links"):
                out.link_queue.append(item)

        return out

    @staticmethod
    def storageUnit():
        return StorageUnit()

db_insert = DbInsert()
