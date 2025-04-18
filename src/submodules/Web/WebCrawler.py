from resources.Globals import os, utils, consts, logger, Path, zipfile, wget, time, requests, assets_cache_storage, file_manager, config, HTMLFormatter, download_manager, FakeUserAgent
from resources.Exceptions import NotInstalledException
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from urllib.parse import urljoin
import re

class Crawler():
    def __makeDirs(self):
        if self.p_download_resources == 1:
            os.makedirs(os.path.join(self.save_dir, "assets"), exist_ok=True)
            os.makedirs(os.path.join(self.save_dir, "css"), exist_ok=True)
            os.makedirs(os.path.join(self.save_dir, "scripts"), exist_ok=True)

    def __init__(self, save_dir, args):
        self.args = args
        self.tabs = []
        self.save_dir = save_dir
        self.downloaded_assets = []

        self.p_scroll_cycles = int(self.args.get("scroll_cycles", 10))
        self.p_scroll_timeout = int(self.args.get("scroll_timeout", 0))
        self.p_download_resources_js = int(self.args.get("download_resources_js", 0))
        self.p_download_resources = int(self.args.get("download_resources", 1))
        self.p_download_img = 1
        self.p_download_resources_from_css = int(self.args.get("download_resources_from_css", 1))
        self.p_fullsize_page_screenshot = int(self.args.get("fullsize_page_screenshot", 0))
        self.p_fullsize_page_screenshot_value = int(self.args.get("fullsize_page_screenshot_value", 1900))
        self.p_scroll_screenshot_px = int(self.args.get("screenshot_scroll", 0))
        self.p_implicitly_wait = int(self.args.get("implicitly_wait", 5))
        self.p_print_html_to_console = int(self.args.get("print_html_to_console", 0))

        self.__makeDirs()

    def __del__(self):
        self.driver.quit()
    
    # didnt tested on other platforms
    def checkWebDriver(self):
        consts["__tmp_chrome_platform"] = utils.getChromishPlatform()

        self.__chrome_path = consts["binary"] +"\\chrome" # Main dir
        self.__webdriver_dir = f"{self.__chrome_path}\\chromedriver"
        self.__webdriver = f"{self.__webdriver_dir}\\chromedriver.exe"
        self.__chrome_headless_dir = f"{self.__chrome_path}\\chrome-headless-shell"
        self.__chrome_headless = f"{self.__chrome_headless_dir}\\chrome-headless-shell.exe"
        if consts["__tmp_chrome_platform"].find("win") == -1:
            self.__webdriver = f"{self.__webdriver_dir}\\chromedriver"
            self.__chrome_headless = f"{self.__chrome_headless_dir}\\chrome-headless-shell"
        
        if Path(self.__webdriver_dir).is_dir() == False:
            return False
        
        return True

    # 12.02.2025
    async def downloadChrome(self):
        ____channel = "Stable"
        CHROME_ENDPOINT_WEBDRIVER = "https://googlechromelabs.github.io/chrome-for-testing/last-known-good-versions-with-downloads.json"
        __CHROME_ENDPOINT_TMP = requests.get(CHROME_ENDPOINT_WEBDRIVER)
        __CHROME_ENDPOINT_TMP_JSON = __CHROME_ENDPOINT_TMP.json()
        ___downloads = __CHROME_ENDPOINT_TMP_JSON["channels"][____channel]["downloads"]
        ___chromedriver = ___downloads["chromedriver"]
        ___chromedriver_headless = ___downloads["chrome-headless-shell"]
        __chromedriver_url = ""
        __chromedriver_headless_url = ""

        for ____down in ___chromedriver:
            if ____down["platform"] == consts["__tmp_chrome_platform"]:
                __chromedriver_url = ____down["url"]
                break

        for ____down in ___chromedriver_headless:
            if ____down["platform"] == consts["__tmp_chrome_platform"]:
                __chromedriver_headless_url = ____down["url"]
                break
        
        # TODO rewrite to asyncio
        # Downloading chromedriver.

        __download_path_chrome = os.path.join(consts["binary"], "chrome", "chromedriver.zip")
        __download_path_head = os.path.join(consts["binary"], "chrome", "chrome-headless.zip")

        logger.log(section="Extractors|Crawling",name="message",message=f"Downloading chromedriver ({__download_path_chrome}) and chrome headless ({__download_path_head})")
        
        __latest_driver_zip = await download_manager.addDownload(__chromedriver_url, __download_path_chrome)
        with zipfile.ZipFile(__download_path_chrome, "r") as zip_ref: # Unzipping
            zip_ref.extractall(os.path.join(consts["binary"], "chrome"))

        os.remove(__download_path_chrome) # Removing original file
        Path(f"{consts["binary"]}/chrome/chromedriver-{consts["__tmp_chrome_platform"]}").rename(self.__webdriver_dir)

        # Downloading headless chrome
        __latest_driver_head_zip = await download_manager.addDownload(__chromedriver_headless_url, __download_path_head)
        with zipfile.ZipFile(__download_path_head, "r") as zip_ref:
            zip_ref.extractall(os.path.join(consts["binary"], "chrome"))

        os.remove(__download_path_head)
        Path(f"{consts["binary"]}/chrome/chrome-headless-shell-{consts["__tmp_chrome_platform"]}").rename(self.__chrome_headless_dir)
    
    def startChrome(self):
        ua = FakeUserAgent(platforms='desktop',min_version=120.0,os='Linux')
        user_agent = ua.random

        _options = webdriver.ChromeOptions()
        _options.binary_location = self.__chrome_headless
        _options.add_argument('--start-maximized')
        _options.add_argument('--start-fullscreen')
        _options.add_argument('--headless')
        _options.add_argument('--no-sandbox')
        _options.add_argument('--window-size=1920,1200')
        _options.add_argument(f'--user-agent={user_agent}')

        #consts["__chrome_service"] = ChromeService(executable_path=self.__webdriver,chrome_options=_options,log_path='NUL')
        #consts["__chrome_executable"] = webdriver.Chrome(service=self.service,options=_options)
        
        self.service = ChromeService(executable_path=self.__webdriver,chrome_options=_options,log_path='NUL')
        self.driver  = webdriver.Chrome(service=self.service,options=_options)

        logger.log(section="Extractors|Crawling",name="message",message="Started Google Chrome")
    
    def openURL(self, input_url):
        self.url = input_url
        self.base_url = '/'.join(self.url.split('/')[:3]) # :3
        self.driver.get(self.url)

        logger.log(section="Extractors|Crawling",name="message",message=f"Opened URL {self.url}")

        self.driver.implicitly_wait(self.p_implicitly_wait)
    
    def scrollAvailableContent(self):
        # Scrolling until end of page
        last_height   = self.driver.execute_script('return document.body.scrollHeight')
        scroll_cycles = self.p_scroll_cycles
        scroll_iter   = 0
        while True:
            if scroll_iter > scroll_cycles:
                break

            self.driver.execute_script('window.scrollTo(0, document.body.scrollHeight);')
            time.sleep(self.p_scroll_timeout)

            new_height = self.driver.execute_script('return document.body.scrollHeight')
            if new_height == last_height:
                break

            logger.log(section="Extractors|Crawling",name="message",message=f"Scrolled page \"{self.url}\" to the bottom. Current iterator: {scroll_iter}, current height: {new_height}")
            
            last_height = new_height
            scroll_iter += 1 
    
    def printHTML(self):
        self.__html = self.driver.page_source.encode("utf-8")
    
    async def reworkHTML(self):
        __relative_url = self.driver.execute_script(f"return document.querySelector(\"base\") ? document.querySelector(\"base\").href : null")
        if __relative_url == None:
            self.relative_url = "https://" + self.base_url
        else:
            self.relative_url = __relative_url

        # TODO: rewrite as in archive.is
        # inline css options, js removing
        self.__soup = BeautifulSoup(self.__html, 'html.parser')
        # Removing all inline attrs
        if self.p_download_resources_js == 0 or self.p_download_resources == 0:
            # It is by link, yeah?
            HTMLFormatter.removeInlineJS(self.__soup)
            HTMLFormatter.removeScriptTags(self.__soup)
        
        # Allowing scroll
        HTMLFormatter.removeOverflowY(self.__soup)

        self.__meta = HTMLFormatter.parseMeta(self.__soup)
        self.__meta["title"] = self.driver.title
        
        if self.p_download_resources == 1:
            if self.p_download_img == 1:
                for img in HTMLFormatter.findAllIMG(self.__soup):
                    # DownloadManager
                    img_url = HTMLFormatter.srcToBase(img.get('src'), self.relative_url)
                    
                    filename = await self.downloadResource(img_url, os.path.join(self.save_dir, 'assets'))
                    if filename:
                        img['data-orig'] = img_url
                        img['src'] = f"assets/{filename}"
            
                for script in HTMLFormatter.findAllScripts(self.__soup):
                    script_url = script.get('src')
                    if self.p_download_resources_js == 1:
                        if script_url != "":
                            script_url = HTMLFormatter.srcToBase(script_url, self.relative_url)
                            filename = await self.downloadResource(script_url, os.path.join(self.save_dir, 'scripts'))
                            if filename:
                                script["data-orig"] = script_url
                                script["src"] = f"scripts/{filename}"

                for a in HTMLFormatter.findAllHrefs(self.__soup):
                    a_url = a.get("href")
                    if not a_url.startswith("http"):
                        a['data-orig'] = a_url
                        a['href'] = self.relative_url + a_url
        
                for link in HTMLFormatter.findAllLinks(self.__soup):
                    rel = link.get("rel")
                    if rel:
                        # todo: move css processing to another function
                        if 'stylesheet' in rel:
                            css_url = link['href']
                            link['data-orig'] = css_url
                            if not css_url.startswith('http'):
                                css_url = self.relative_url + css_url
                            
                            filename = await self.downloadResource(css_url, os.path.join(self.save_dir, 'css'))
                            if filename:
                                link['href'] = f"css/{filename}"
                                url_pattern = re.compile(r'url\((.*?)\)')

                                if self.p_download_resources_from_css == 1:
                                    try:
                                        # Downloading assets from css too.
                                        async with open(os.path.join(self.save_dir, "css", filename), 'r') as css_stream:
                                            css_text   = css_stream.read()
                                            __css_modified = css_text
                                            css_assets_urls = url_pattern.findall(css_text)
                                            for __css_asset_url in css_assets_urls:
                                                __css_asset_url = __css_asset_url.strip(' "\'')
                                                __css_asset_url_full = urljoin(css_url, __css_asset_url)
                                                __css_download_name  = os.path.basename(__css_asset_url_full)
                                                
                                                __css_modified = __css_modified.replace(__css_asset_url, "assets/" + __css_download_name)
                                                await self.downloadResource(__css_asset_url_full, os.path.join(self.save_dir, 'assets'))
                                                logger.log(section="Extractors|Crawling", name="message", message=f"Downloaded asset from {link} => {__css_asset_url}")

                                            # Rewriting css with new values
                                            async with open(os.path.join(self.save_dir, 'css', filename), 'w') as css_stream_write:
                                                css_stream_write.seek(0)
                                                css_stream_write.write(__css_modified)
                                                css_stream_write.truncate()
                                    except Exception as exc:
                                        logger.logException(exc, "Extractors|Crawling")
                        elif 'icon' in rel:
                            favicon_url = link['href']
                            link['data-orig'] = favicon_url
                            if not favicon_url.startswith('http'):
                                favicon_url = self.relative_url + favicon_url
                            filename = await self.downloadResource(favicon_url, os.path.join(self.save_dir, 'assets'))
                            if filename:
                                link['href'] = f"assets/{filename}"
        
        return self.__soup.prettify()
    
    def writeDocumentHTML(self, html):
        self.driver.execute_script(f"document.write(`{html}`);")

    # Creating page from raw HTML
    def crawlPageFromRawHTML(self, html, url_help = ""):
        logger.log(section="Extractors|Crawling", name="message", message=f"Capturing the page from HTML")

        self.url = "about:blank"
        self.base_url = '/'.join(url_help.split('/')[:3]) # :3

        self.driver.get(self.url)
        self.driver.implicitly_wait(self.p_implicitly_wait)
        self.writeDocumentHTML(html)

    # Save resource to asset
    async def downloadResource(self, url, folder_path):
        if url in self.downloaded_assets:
            logger.log(section="Extractors|Crawling", name="download", message=f"File \"{url}\" already downloaded!!! Skipping.")
            return None
        
        try:
            basename = os.path.basename(url.split("?")[0])
            basename_name_splitted = basename.split(".")
            basename_format = basename_name_splitted[-1]
            basename_name = basename.replace(f".{basename_format}", "")
            
            basename_with_site = basename_name + "_" + utils.remove_protocol(self.base_url) + "." + basename_format
            local_path = os.path.join(folder_path, basename_with_site)
            cache_path = os.path.join(assets_cache_storage.path, basename_with_site)

            if int(config.get("extractor.cache_assets")) == 0:
                # Writing file
                logger.log(section="Extractors|Crawling", name="download", message=f"Downloading URL {url} vid AsyncDownloadManager to original dir")
                await download_manager.addDownload(end=url,dir=local_path)
                self.downloaded_assets.append(url)

                return basename_with_site
            # Because of symlinks you need to start local server to load assets.
            else:
                contains = assets_cache_storage.contains(basename_with_site)
                if contains == False:
                    await download_manager.addDownload(end=url,dir=cache_path)
                
                self.downloaded_assets.append(url)
                assets_cache_storage.mklink_from_cache_to_dir(local_path)

                return basename_with_site
        except Exception as e:
            logger.log(section="Extractors|Crawling", name="download", message=f"Error when downloading file {url} ({e}).")

            return None
    
    # Return parsed HTML
    def printHTML(self):
        self.__html = self.driver.page_source.encode("utf-8")
        #self.__html = self.driver.execute_script("return document.documentElement.outerHTML;")
    
    # Make and write screenshot.
    def printScreenshot(self):
        page_width  = self.driver.execute_script('return document.body.scrollWidth')
        page_height = self.driver.execute_script('return document.body.scrollHeight')
        if self.p_fullsize_page_screenshot == 0:
            page_height = min(self.p_fullsize_page_screenshot_value, max(page_height, 600))

        logger.log(section="Extractors|Crawling", name="download", message=f"Making screenshot with {page_width}x{page_height}")
        self.driver.execute_script('window.scrollTo(0, {0});'.format(self.p_scroll_screenshot_px))
        self.driver.set_window_size(page_width, page_height)
        self.driver.save_screenshot(self.save_dir + "/screenshot.png")
    
    def printMeta(self):
        logger.log(section="Extractors|Crawling", name="message", message=f"Printing meta")
        return self.__meta
