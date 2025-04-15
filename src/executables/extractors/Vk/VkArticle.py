from resources.Globals import VkApi, logger
from executables.extractors.Vk.VkTemplate import VkTemplate
from resources.Exceptions import NotFoundException

class VkArticle(VkTemplate):
    name = 'VkArticle'
    category = 'Vk'

    def declare():
        params = {}
        params["item_id"] = {
            "desc_key": "-",
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
        return await __vkapi.call("articles.getByLink", {"links": ",".join(item_ids), "extended": 1})
    
    async def run(self, args):
        __article_response = None
        __item_ids = self.passed_params.get("item_id")
        item_ids = __item_ids.split(",")
        if self.passed_params.get("__json_info") == None:
            try:
                __article_response = await self.__recieveById(item_ids)
                if __article_response.get("items") != None:
                    __article_response = __article_response.get("items")
            except:
                pass
        else:
            try:
                __article_response = self.passed_params.get("__json_info")
                if type(__article_response) == dict:
                    __article_response = [__article_response]
            except:
                __article_response = None

        if __article_response == None or len(__article_response) < 1:
            raise NotFoundException("article not found")
        
        __entities_list = []
        for article in __article_response:
            article["site"] = self.passed_params.get("vk_path")
            __SOURCE  = f"url:{article.get("url")}"
            __TITLE = article.get("title")
            __PUBLICATION = article.get("published_date")

            logger.log(message=f"Recieved article {article.get("url")}",section="VkAttachments",name="message")

            ENTITY = self._entityFromJson({
                "source": __SOURCE,
                "internal_content": article,
                "suggested_name": __TITLE,
                "file": None,
                "unlisted": self.passed_params.get("unlisted") == 1,
                "declared_created_at": __PUBLICATION,
            })
            __entities_list.append(ENTITY)

        return {
            "entities": __entities_list
        }
