from resources.Globals import config, VkApi, logger, consts, math, asyncio
from executables.extractors.Vk.VkTemplate import VkTemplate
from executables.extractors.Vk.VkPhoto import VkPhoto
from resources.Exceptions import NotFoundException

class VkIdentity(VkTemplate):
    name = 'VkIdentity'
    category = 'Vk'

    def declare():
        params = {}
        params["item_id"] = {
            "desc_key": "-",
            "type": "string",
        }
        params["download_avatar"] = {
            "desc_key": "-",
            "type": "bool",
            "default": True,
        }

        return params

    async def run(self, args):
        __vkapi = VkApi(token=self.passed_params.get("access_token"),endpoint=self.passed_params.get("api_url"))
        identities_id_string = self.passed_params.get("item_id")
        IDENTITIES_IDS = identities_id_string.split(",")

        user_ids = []
        group_ids = []

        for IDENTITY_ID in IDENTITIES_IDS:
            __id = int(IDENTITY_ID)
            if __id > 0:
                user_ids.append(__id)
            else:
                group_ids.append(abs(__id))

        logger.log(message=f"Got ids +{",".join(str(x) for x in user_ids)}, -{",".join(str(x) for x in group_ids)}")
        __users_response, __groups_response = [{}, {}]

        if len(user_ids) > 0:
            __users_response = await __vkapi.call("users.get", {"user_ids": ",".join(str(x) for x in user_ids), "fields": consts["vk.user_fields"]})
        if len(group_ids) > 0:
            __groups_response = await __vkapi.call("groups.getById", {"group_ids": ",".join(str(x) for x in group_ids), "fields": consts["vk.group_fields"]})
        
        users   = []
        groups  = []
        if __users_response != None:
            for user in __users_response:
                users.append(user)
        
        if type(__groups_response) != "dict":
            for club in __groups_response:
                groups.append(club)
        else:
            for club in __groups_response.get("groups"):
                groups.append(club)
        
        entities = []
        for user in users:
            ENTITY = self._entityFromJson({
                "source": f"vk:user{user.get("id")}",
                "internal_content": user,
            })
            entities.append(ENTITY)
        
        for group in groups:
            ENTITY = self._entityFromJson({
                "source": f"vk:group{group.get("id")}",
                "internal_content": group,
            })
            entities.append(ENTITY)
        
        return {
            "entities": entities
        }
