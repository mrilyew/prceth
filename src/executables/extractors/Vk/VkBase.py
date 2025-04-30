from executables.extractors.Base.Base import BaseExtractor
from resources.Globals import env, consts

class VkBase(BaseExtractor):
    name = 'VkBase'
    category = 'template'
    
    def defineConsts(self):
        super().defineConsts()

        consts["vk.user_fields"] = ["first_name_gen", "first_name_acc", "last_name_gen", "last_name_acc", "first_name_ins", "last_name_ins", "first_name_abl", "last_name_abl", "about", "activities", "bdate", "blacklisted", "blacklisted_by_me", "books", "can_see_all_posts", "career", "city", "common_count", "connections", "contacts", "counters", "country", "cover", "crop_photo", "domain", "education", "email", "can_write_private_message", "exports", "employee_mark", "employee_working_state", "is_service_account", "educational_profile", "name", "type", "reposts_disabled", "followers_count", "friend_status", "games", "has_photo", "has_mobile", "has_mail", "house", "home_town", "interests", "is_subscribed", "is_no_index", "is_nft", "is_favorite", "is_friend", "is_followers_mode_on", "bdate_visibility", "is_dead", "image_status", "is_hidden_from_feed", "is_verified", "last_seen", "maiden_name", "movies", "music", "military", "nickname", "online", "online_info", "occupation", "owner_state", "personal", "photo_200", "photo_50", "photo_max", "photo_max_orig", "quotes", "relatives", "relation", "schools", "sex", "site", "status", "tv", "universities", "verified", "wall_default", "correct_counters", "telegram", "rating", "reg_date", "background", "custom_fields"]
        consts["vk.group_fields"] = ["activity", "addresses", "age_limits", "ban_info", "can_create_topic", "can_message", "can_post", "can_suggest", "can_see_all_posts", "can_upload_doc", "can_upload_story", "can_upload_video", "city", "contacts", "counters", "country", "cover", "crop_photo", "description", "fixed_post", "has_photo", "is_favorite", "is_hidden_from_feed", "is_subscribed", "is_messages_blocked", "links", "main_album_id", "main_section", "member_status", "members_count", "place", "photo_50", "photo_200", "photo_max", "photo_max_orig", "public_date_label", "site", "start_date", "finish_date", "status", "trending", "verified", "wall", "wiki_page", "background"]
    
    def declare():
        params = {}
        params["access_token"] = {
            "desc_key": "-",
            "type": "string",
            "default": env.get("vk.access_token", None),
            "assert": {
                "assert_not_null": True,
            },
        }
        params["api_url"] = {
            "desc_key": "-",
            "type": "string",
            "default": env.get("vk.api_url", "api.vk.com/method"),
            "assert": {
                "assert_not_null": True,
            },
        }
        params["vk_path"] = {
            "desc_key": "-",
            "type": "string",
            "default": env.get("vk.vk_path", "vk.com"),
            "assert": {
                "assert_not_null": True,
            },
        }

        return params

    def setArgs(self, args):
        super().setArgs(args)

    async def run(self, args):
        pass
    
    def describeSource(self, INPUT_ENTITY):
        return {"type": "vk", "data": {
            "source": f"https://{INPUT_ENTITY.getFormattedInfo().get('vk_path')}/" + INPUT_ENTITY.orig_source
        }}
