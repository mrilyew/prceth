from resources.Globals import asyncio, aiohttp, os, time, logger, Path, consts, config

class DownloadManager():
    def __init__(self, max_concurrent_downloads=3, speed_limit_kbps=None):
        self.queue = []
        self.max_concurrent_downloads = max_concurrent_downloads
        self.speed_limit_kbps = speed_limit_kbps
        self.semaphore = asyncio.Semaphore(self.max_concurrent_downloads)
        self.__headers = {
            "User-Agent": config.get("web.useragent")
        }
        self.__timeout = consts["net.global_timeout"]
    
    async def addDownload(self, end, dir):
        try:
            self.queue.append({
                "url": end, 
                "dir": dir,
                "pause_flag": asyncio.Event(),
                "task": None,
            })

            return await self.startDownload(self.queue[-1])
        except:
            return None

    async def startDownload(self, queue_element):
        if getattr(self, "__session", None) == None:
            timeout = aiohttp.ClientTimeout(total=self.__timeout)
            self.__session = aiohttp.ClientSession(timeout=timeout)

        async with self.__session as session:
            queue_element["task"] = await asyncio.create_task(self.download(session, queue_element))
            
            return queue_element["task"]
            #asyncio.run(self.download(session, queue_element))

    async def download(self, session, queue_element):
        DOWNLOAD_URL = queue_element.get("url")
        DOWNLOAD_DIR = queue_element.get("dir")

        async with self.semaphore:
            async with session.get(DOWNLOAD_URL, allow_redirects=True, headers=self.__headers) as response:
                logger.log(section="AsyncDownloadManager", name="message", message=f"Downloading {DOWNLOAD_URL} to {DOWNLOAD_DIR}")
                HTTP_REQUEST_STATUS = response.status

                #if HTTP_REQUEST_STATUS != 200:
                #    logger.log("AsyncDownloadManager", "error", f"Error when downloading file {DOWNLOAD_URL}")
                #    return None
                if HTTP_REQUEST_STATUS == 404 or HTTP_REQUEST_STATUS == 403:
                    raise FileNotFoundError('File not found')
                
                if Path(DOWNLOAD_DIR).is_file():
                    logger.log(section="AsyncDownloadManager", name="message", message=f"{DOWNLOAD_URL} already downloaded, didn't.")
                    return response

                start_time = time.time()
                queue_element["downloaded"] = 0
                queue_element["size"] = int(response.headers.get("Content-Length", 0))
                queue_element["start_time"] = start_time
                with open(DOWNLOAD_DIR, 'wb') as f:
                    async for chunk in response.content.iter_chunked(1024):
                        #await queue_element["pause_flag"].wait() TODO FIX !!!!!!!!!!!
                        f.write(chunk)

                        elapsed_time = time.time() - start_time
                        expected_time = len(chunk)
                        queue_element["downloaded"] += expected_time

                        #if consts["context"] == "cli":
                            #pfrint(f"Downloaded {queue_element["downloaded"]} from {queue_element["size"]}")
                        
                        if self.speed_limit_kbps:
                            expected_time = expected_time / (self.speed_limit_kbps * 1024)
                            if expected_time > elapsed_time:
                                await asyncio.sleep(expected_time - elapsed_time)
                
                logger.log(section="AsyncDownloadManager", name="success", message=f"Successfully downloaded file {DOWNLOAD_URL} to {DOWNLOAD_DIR}")
                return response
    
    def __findDownloadByURL(self, url):
        for item in self.queue:
            if item.get("url") == url:
                return item
            
        return None

    def pause(self, url):
        item = self.__findDownloadByURL(url)
        if item == None:
            return None
        
        item["pause_flag"].clear()

    def resume(self, url):
        item = self.__findDownloadByURL(url)
        if item == None:
            return None
        
        item["pause_flag"].set()

    def set_max_concurrent_downloads(self, value):
        self.max_concurrent_downloads = int(value)
        self.semaphore = asyncio.Semaphore(self.max_concurrent_downloads)

    def set_speed_limit_kbps(self, value):
        self.speed_limit_kbps = int(value)

download_manager = DownloadManager(max_concurrent_downloads=2, speed_limit_kbps=200)
