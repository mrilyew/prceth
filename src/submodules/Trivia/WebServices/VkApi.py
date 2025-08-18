from app.App import logger
import aiohttp

class VkApiException(Exception):
    def __init__(self, message):
        super().__init__(message)

class VkApi():
    def __init__(self, token, endpoint = "api.vk.com/method"):
        self.__token = token
        self.__endpoint = endpoint

    async def call(self, method, params):
        params["access_token"] = self.__token
        params["v"] = 5.221
        __end_url = f"https://{self.__endpoint}/{method}?"
        __save_end_url = f"https://{self.__endpoint}/{method}?"
        for param in params.items():
            __end_url += f"&{param[0]}={param[1]}"
            if param[0] != "access_token":
                __save_end_url += f"&{param[0]}={param[1]}"
            else:
                __save_end_url += f"&access_token=X"
        
        __response = None
        async with aiohttp.ClientSession() as session:
            async with session.get(__end_url) as response:
                __response = await response.json()

        logger.log(f"Called VK API {__save_end_url}", section="Submodules.Trivia!VkApi")

        if __response.get("response") == None:
            if __response.get("error"):
                raise VkApiException(message=__response.get("error").get("error_msg"))
            else:
                raise VkApiException(message=__response.get("error_msg"))

        return __response.get("response")
