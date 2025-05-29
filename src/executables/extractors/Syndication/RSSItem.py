from resources.Globals import xmltodict, often_params, datetime
from executables.extractors.Base.Base import BaseExtractor

class RSSItem(BaseExtractor):
    name = 'RSSItem'
    category = 'Syndication'
    docs = {}
    hidden = True
    main_args = {
        "list": ["xml", "xml_parsed"],
        "type": "strict_or",
    }

    def declare():
        params = {}
        params["xml"] = often_params.get("xml_explain")
        params["xml_parsed"] = often_params.get("xml_parsed_explain")
        params["save_original_xml"] = often_params.get("save_original_xml")
        params["source"] = often_params.get("simple_source")

        return params

    async def run(self, args={}):
        # FFFFFFFUUUUUUUUUCCCCCCCCCKKKKKKKK

        xml_code = self.passed_params.get("xml")
        xml_dict = None

        if xml_code != None:
            xml_dict = xml_code
        else:
            xml_dict = self.passed_params.get("xml_parsed")

        xml_arr = None

        if type(xml_dict) == list:
            xml_arr = xml_dict
        else:
            xml_arr = [xml_dict]

        __LIST = []
        for __xml in xml_arr:
            internal_content = {
                "xml": __xml,
            }

            if self.passed_params.get("save_original_xml") == True:
                internal_content["original_xml"] = __xml

            __name = __xml.get("title")
            __date = datetime.strptime(__xml.get("pubDate"), "%a, %d %b %Y %H:%M:%S %z")

            ENTITY = self._entityFromJson({
                "source": self.passed_params.get("source", "api:xml"),
                "suggested_name": __name,
                "declared_created_at": __date.timestamp(),
                "internal_content": internal_content,
            })

            __LIST.append(ENTITY)

        return {
            "entities": __LIST
        }
