from resources.Globals import VkApi, utils, logger
from executables.extractors.Vk.VkTemplate import VkTemplate
from resources.Exceptions import NotFoundException

# Downloads document from vk.com using api.
class VkPoll(VkTemplate):
    name = 'VkPoll'
    category = 'Vk'
    hidden = True

    def declare():
        params = {}
        params["item_id"] = {
            "desc_key": "vk_poll_desc",
            "type": "string",
        }
        params["__json_info"] = {
            "desc_key": "-",
            "type": "object",
            "assertion": {
                "assert_link": "item_id"
            }
        }

        return params
    
    async def __recieveById(self, item_ids):
        __vkapi = VkApi(token=self.passed_params.get("access_token"),endpoint=self.passed_params.get("api_url"))
        spl = item_ids[0].split("_")

        return await __vkapi.call("polls.getById", {"owner_id": spl[0], "poll_id": spl[1], "extended": 1})
    
    async def run(self, args):
        __item_ids = self.passed_params.get("item_id")
        item_ids = __item_ids.split(",")
        items = None

        if self.passed_params.get("__json_info") == None:
            try:
                item_resp = await self.__recieveById(item_ids)
                if item_resp != None:
                    items = [item_resp]
            except:
                items = None
        else:
            try:
                items = self.passed_params.get("__json_info")
                if type(items) == dict:
                    items = [items]
            except:
                items = None

        if items == None or len(items) < 1:
            raise NotFoundException("poll not found")
        
        __entities_list = []
        for poll in items:
            poll["site"] = self.passed_params.get("vk_path")

            # TODO: background downloader
            __ITEM_ID  = f"{poll.get('owner_id')}_{poll.get('id')}"
            __SOURCE   = f"vk:poll{__ITEM_ID}"

            logger.log(message=f"Recieved poll {__ITEM_ID}",section="VkAttachments",name="message")
        
            ENTITY = self._entityFromJson({
                "source": __SOURCE,
                "internal_content": poll,
                "unlisted": self.passed_params.get("unlisted") == 1,
                "declared_created_at": poll.get("date"),
                "suggested_name": poll.get("question"),
            })
            __entities_list.append(ENTITY)

        return {
            "entities": __entities_list
        }
