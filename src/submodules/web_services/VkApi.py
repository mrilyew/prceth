from resources.Globals import consts, logger, aiohttp, asyncio

class VkApiException(Exception):
    def __init__(self, message):
        super().__init__(message)

class VkApi():
    def __init__(self, token, endpoint = "api.vk.com/method"):
        self.__token = token
        self.__endpoint = endpoint

        consts["vk_secret_useragent"] = ""

    async def call(self, method, params):
        params["access_token"] = self.__token
        params["v"] = 5.221
        __end_url = f"https://{self.__endpoint}/{method}?"
        for param in params.items():
            __end_url += f"&{param[0]}={param[1]}"
        
        __response = None
        async with aiohttp.ClientSession() as session:
            async with session.get(__end_url) as response:
                __response = await response.json()
        
        logger.log(f"Called VK API {__end_url}", section="VkApi")
        
        if __response.get("response") == None:
            raise VkApiException(message=__response.get("error").get("error_msg"))
        
        return __response.get("response")
