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
        params["__json_info"] = {
            "desc_key": "-",
            "type": "object",
            "hidden": True,
            "assertion": {
                "assert_link": "item_id"
            }
        }

        return params

    async def run(self, args):
        __vkapi = VkApi(token=self.passed_params.get("access_token"),endpoint=self.passed_params.get("api_url"))
        identities_id_string = self.passed_params.get("item_id", "")
        IDENTITIES_IDS = identities_id_string.split(",")
        users   = []
        groups  = []
        __users_response, __groups_response = [{}, {}]

        if self.passed_params.get("__json_info") == None:
            user_ids = []
            group_ids = []

            for IDENTITY_ID in IDENTITIES_IDS:
                __id = int(IDENTITY_ID)
                if __id > 0:
                    user_ids.append(__id)
                else:
                    group_ids.append(abs(__id))

            logger.log(message=f"Got ids +{",".join(str(x) for x in user_ids)}, -{",".join(str(x) for x in group_ids)}")

            if len(user_ids) > 0:
                __users_response = await __vkapi.call("users.get", {"user_ids": ",".join(str(x) for x in user_ids), "fields": ",".join(consts["vk.user_fields"])})
            if len(group_ids) > 0:
                __groups_response = await __vkapi.call("groups.getById", {"group_ids": ",".join(str(x) for x in group_ids), "fields": ",".join(consts["vk.group_fields"])})
        else:
            __users_response = self.passed_params.get("__json_info").get("users", [])
            __groups_response = self.passed_params.get("__json_info").get("groups", [])
        
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
            NAME = f"@vk_user: {user.get("first_name")} {user.get("last_name")}"
            ENTITY = self._entityFromJson({
                "source": f"vk:user{user.get("id")}",
                "internal_content": user,
                "suggested_name": NAME,
                "declared_created_at": user.get("reg_date", None),
            })
            entities.append(ENTITY)
        
        for group in groups:
            # TODO: get history
            NAME = f"@vk_club: {group.get("name")}"

            ENTITY = self._entityFromJson({
                "source": f"vk:group{group.get("id")}",
                "internal_content": group,
                "suggested_name": NAME,
            })
            entities.append(ENTITY)
        
        return {
            "entities": entities
        }
