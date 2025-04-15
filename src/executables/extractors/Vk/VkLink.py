from resources.Globals import Path, download_manager, logger, os
from executables.extractors.Vk.VkTemplate import VkTemplate
from resources.Exceptions import NotFoundException

class VkLink(VkTemplate):
    name = 'VkLink'
    category = 'Vk'
    hidden = True

    def declare():
        params = {}
        params["__json_info"] = {
            "desc_key": "-",
            "type": "object",
            "assertion": {
                "assert_not_null": True
            }
        }
        params["download_file"] = {
            "desc_key": "-",
            "type": "bool",
            "default": True
        }

        return params
        
    async def run(self, args):
        __json = self.passed_params.get("__json_info")
        if __json == None:
            raise NotFoundException("link not found")
        
        __json["site"] = self.passed_params.get("vk_path")

        logger.log(message=f"Recieved attached link",section="VkAttachments",name="message")

        ENTITY = self._entityFromJson({
            "internal_content": __json,
            "source": f"url:{__json.get("url")}",
            "unlisted": self.passed_params.get("unlisted") == 1,
            "suggested_name": f"Vk Attached link",
        })

        return {
            "entities": [ENTITY]
        }
