from app.App import env
from executables.representations import Representation
from declarable.ArgumentsTypes import StringArgument, ObjectArgument, BooleanArgument
from utils.MainUtils import list_conversation
from submodules.Uncanon.WebServices.VkApi import VkApi
from resources.Exceptions import AbstractClassException
from resources.Consts import consts

class BaseVk(Representation):
    category = 'WebServices_Vk'
    executable_cfg = {
        "list": ["ids", "object"],
        "type": "or",
    }

    def define():
        consts["vk.user_fields"] = ["first_name_gen", "first_name_acc", "last_name_gen", "last_name_acc", "first_name_ins", "last_name_ins", "first_name_abl", "last_name_abl", "about", "activities", "bdate", "blacklisted", "blacklisted_by_me", "books", "can_see_all_posts", "career", "city", "common_count", "connections", "contacts", "counters", "country", "cover", "crop_photo", "domain", "education", "email", "can_write_private_message", "exports", "employee_mark", "employee_working_state", "is_service_account", "educational_profile", "name", "type", "reposts_disabled", "followers_count", "friend_status", "games", "has_photo", "has_mobile", "has_mail", "house", "home_town", "interests", "is_subscribed", "is_no_index", "is_nft", "is_favorite", "is_friend", "is_followers_mode_on", "bdate_visibility", "is_dead", "image_status", "is_hidden_from_feed", "is_verified", "last_seen", "maiden_name", "movies", "music", "military", "nickname", "online", "online_info", "occupation", "owner_state", "personal", "photo_200", "photo_50", "photo_max", "photo_max_orig", "quotes", "relatives", "relation", "schools", "sex", "site", "status", "tv", "universities", "verified", "wall_default", "correct_counters", "telegram", "rating", "reg_date", "background", "custom_fields"]
        consts["vk.group_fields"] = ["activity", "addresses", "age_limits", "ban_info", "can_create_topic", "can_message", "can_post", "can_suggest", "can_see_all_posts", "can_upload_doc", "can_upload_story", "can_upload_video", "city", "contacts", "counters", "country", "cover", "crop_photo", "description", "fixed_post", "has_photo", "is_favorite", "is_hidden_from_feed", "is_subscribed", "is_messages_blocked", "links", "main_album_id", "main_section", "member_status", "members_count", "place", "photo_50", "photo_200", "photo_max", "photo_max_orig", "public_date_label", "site", "start_date", "finish_date", "status", "trending", "verified", "wall", "wiki_page", "background"]
        consts["vk.min_group_fields"] = ["activity","photo_100","photo_id","cover","photo_200","photo_50","is_member","is_closed","description","members_count","is_subscribed"]
        consts["vk.min_user_fields"] = ["photo_50","online","photo_id","photo_max","last_seen", "cover"]

    @classmethod
    def declareVk(cls):
        params = {}
        params["api_token"] = StringArgument({
            "sensitive": True,
            "default": env.get("vk.access_token", None),
            "env_property": "vk.access_token",
        })
        params["api_url"] = StringArgument({
            "env_property": "vk.api_url",
            "default": env.get("vk.api_url", "api.vk.com/method"),
            "assertion": {
                "not_null": True,
            },
        })
        params["vk_path"] = StringArgument({
            "env_property": "vk.api_url",
            "default": env.get("vk.vk_path", "vk.com"),
            "assertion": {
                "not_null": True,
            },
        })

        return params

    @classmethod
    def declare(cls):
        params = {}
        params.update(cls.declareVk())
        params["execute_at_once"] = BooleanArgument({
            "default": True,
            "assertion": {
                "not_null": True,
            },
        })

        return params

    def _find_owner(id, profiles, groups):
        '''
        Gets owner by id from "profiles" and "groups" arrays.
        '''
        search_array = profiles
        if id < 0:
            search_array = groups

        if search_array == None:
            return None

        for item in search_array:
            if item.get('id') == abs(int(id)):
                return item

        return None

    def _insertVkLink(item, vk_path):
        item['site'] = vk_path

    @classmethod
    def _insertOwner(cls, item, column_name, profiles, groups):
        item[column_name.replace('_id', '')] = cls._find_owner(item.get(column_name), profiles, groups)

    class Extractor(Representation.ExtractStrategy):
        def preExecute(self, i = {}):
            self.vkapi = VkApi(token=i.get("api_token"),endpoint=i.get("api_url"))

class BaseVkItemId(BaseVk):
    @classmethod
    def declare(cls):
        params = {}
        params["ids"] = StringArgument({})
        params["object"] = ObjectArgument({
            "hidden": True,
        })

        return params

    class Extractor(BaseVk.Extractor):
        def extractWheel(self, i = {}):
            if i.get('object') != None:
                return 'extractByObject'
            elif 'ids' in i:
                return 'extractById'

        async def __response(self, i = {}):
            raise AbstractClassException('not implemented at this class')

        async def extractById(self, i = {}):
            resp = await self.__response(i)
            i['object'] = resp

            return await self.extractByObject(i)

        async def extractByObject(self, i = {}):
            objects = i.get("object")
            items = []

            if type(objects) == list:
                items = objects
            else:
                if 'items' in objects:
                    items = objects.get('items')

                    if 'profiles' in objects:
                        self.buffer['profiles'] = objects.get("profiles")
                        self.buffer['groups'] = objects.get("groups")
                else:
                    items = list_conversation(objects)

            return await self.gatherList(items, self.item, i.get('execute_at_once') == True)
