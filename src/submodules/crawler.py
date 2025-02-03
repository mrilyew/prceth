from resources.globals import os, utils, consts, Path, time, requests
from resources.exceptions import NotInstalledLibrary
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from urllib.parse import urljoin
import re

class Crawler():
    def __makeDirs(self):
        os.makedirs(os.path.join(self.save_dir, "assets"), exist_ok=True)
        os.makedirs(os.path.join(self.save_dir, "css"), exist_ok=True)
        os.makedirs(os.path.join(self.save_dir, "scripts"), exist_ok=True)

    def __init__(self, save_dir, args):
        self.args     = args

        self.p_scroll_cycles   = int(self.args.get("scroll_cycles", 10))
        self.p_scroll_timeout  = int(self.args.get("scroll_timeout", 0))
        self.p_download_resources_js = int(self.args.get("download_resources_js", 1))
        self.p_download_resources = int(self.args.get("download_resources", 1))
        self.p_download_resources_from_css = int(self.args.get("download_resources_from_css", 0))
        self.p_fullsize_page_screenshot    = int(self.args.get("fullsize_page_screenshot", 0))
        self.p_fullsize_page_screenshot_value = int(self.args.get("fullsize_page_screenshot_value", 1000))
        self.p_scroll_screenshot_px        = int(self.args.get("screenshot_scroll", 0))
        self.p_implicitly_wait = int(self.args.get("implicitly_wait", 5))

        self.save_dir = save_dir
        self.__makeDirs()
        _chrome_path = consts["tmp"] +"\\chrome" # Main dir
        _webdriver_path = _chrome_path  + "\\chromedriver-win64\\chromedriver.exe" # Chromedriver
        _chrome_headless = _chrome_path + "\\chrome-headless"
        if Path(_webdriver_path).is_file() == False:
            _crawl = utils.download_chrome_driver()

        if Path(_chrome_headless).is_dir() == False:
            raise NotInstalledLibrary("Chromium headless is not installed at path /storage/tmp/chrome/chrome-headless (https://googlechromelabs.github.io/chrome-for-testing/)")
        
        _options = webdriver.ChromeOptions()
        _options.binary_location = _chrome_headless + "\\chrome-headless-shell.exe"
        _options.add_argument('--start-maximized')
        _options.add_argument('--start-fullscreen')
        _options.add_argument('--headless')
        _options.add_argument('--no-sandbox')
        _options.add_argument('--window-size=1920,1200')

        self.service = ChromeService(executable_path=_webdriver_path,chrome_options=_options,log_path='NUL')
        self.driver  = webdriver.Chrome(service=self.service,options=_options)

    def __del__(self):
        self.driver.quit()
    
    def start_crawl(self, url):
        print("&Crawler | Capturing the page...")
        self.url = url
        self.base_url = '/'.join(self.url.split('/')[:3]) # :3
        self.driver.get(url)
        self.driver.implicitly_wait(self.p_implicitly_wait)

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

            print("&Crawler | Scrolled the page to the bottom. Current iterator: {0}, current height: {1}".format(scroll_iter, new_height))
            
            last_height = new_height
            scroll_iter += 1 
    
    # Save resource to asset
    @staticmethod
    def download_resource(url, folder_path):
        try:
            response = requests.get(url, stream=True)
            response.raise_for_status()
            basename = os.path.basename(url.split("?")[0])
            local_path = os.path.join(folder_path, basename)

            # Writing file
            with open(local_path, 'wb') as f:
                for chunk in response.iter_content(chunk_size=8192):
                    f.write(chunk)

            print(f"&Crawler | Downloaded file {url}.")
            return basename
        except Exception as e:
            print(f"&Crawler | Error when downloading file {url} ({e}).")
            return None
    
    # Format html (download assets, format links)
    def parse_html(self, html):
        soup = BeautifulSoup(html, 'html.parser')
        if self.p_download_resources == 0:
            return soup.prettify()
        
        # TODO ADD CHECK IF FILE ALREADY DOWNLOADED
        
        # Finding images
        for img in soup.find_all('img', src=True):
            img_url = img.get('src')
            if not img_url.startswith('http'):
                img_url = self.base_url + img_url
            filename = Crawler.download_resource(img_url, os.path.join(self.save_dir, 'assets'))
            if filename:
                img['data-orig'] = img_url
                img['src'] = f"assets/{filename}"
        
        # Attempt to save scripts
        for script in soup.find_all('script', src=True):
            script_url = script.get('src')
            if self.p_download_resources_js == 1:
                if script_url != "":
                    if not script_url.startswith('http'):
                        script_url = self.base_url + script_url
                    filename = Crawler.download_resource(script_url, os.path.join(self.save_dir, 'scripts'))
                    if filename:
                        script['data-orig'] = script_url
                        script['src'] = f"scripts/{filename}"
            else:
                # Todo make remover js calls on another tags
                script.decompose()

        for a in soup.find_all('a', href=True):
            a_url = a.get('href')
            if not a_url.startswith('http'):
                a['data-orig'] = a_url
                a['href'] = self.base_url + a_url
        
        # Finding links
        for link in soup.find_all('link', href=True):
            rel = link.get("rel")
            if rel:
                # todo: move css processing to another function
                if 'stylesheet' in rel:
                    css_url = link['href']
                    link['data-orig'] = css_url
                    if not css_url.startswith('http'):
                        css_url = self.base_url + css_url
                    filename = Crawler.download_resource(css_url, os.path.join(self.save_dir, 'css'))
                    if filename:
                        link['href'] = f"css/{filename}"
                        url_pattern = re.compile(r'url\((.*?)\)')

                        if self.p_download_resources_from_css == 1:
                            # Downloading assets from css too.
                            css_stream = open(os.path.join(self.save_dir, 'css', filename), 'r')
                            css_text   = css_stream.read()
                            __css_modified = css_text
                            css_assets_urls = url_pattern.findall(css_text)
                            for __css_asset_url in css_assets_urls:
                                __css_asset_url = __css_asset_url.strip(' "\'')
                                __css_asset_url_full = urljoin(css_url, __css_asset_url)
                                __css_download_name  = os.path.basename(__css_asset_url_full)
                                
                                __css_modified = __css_modified.replace(__css_asset_url, "assets/" + __css_download_name)
                                Crawler.download_resource(__css_asset_url_full, os.path.join(self.save_dir, 'assets'))
                                print(f"&Crawler | Downloaded asset from {link} => {__css_asset_url}")

                            # Rewriting css with new values
                            css_stream_write = open(os.path.join(self.save_dir, 'css', filename), 'w')
                            css_stream_write.seek(0)
                            css_stream_write.write(__css_modified)
                            css_stream_write.truncate()
                elif 'icon' in rel:
                    favicon_url = link['href']
                    link['data-orig'] = favicon_url
                    if not favicon_url.startswith('http'):
                        favicon_url = self.base_url + favicon_url
                    filename = Crawler.download_resource(favicon_url, os.path.join(self.save_dir, 'assets'))
                    if filename:
                        link['href'] = f"assets/{filename}"

        return soup.prettify()
    
    def parse_meta(self, html):
        final_meta = {"title": self.driver.title}
        soup = BeautifulSoup(html, 'html.parser')
        for meta in soup.find_all('meta'):
            meta_name = meta.get('name')
            meta_content = meta.get('content')
            if meta_name == None:
                continue

            final_meta[meta_name] = meta_content

        return final_meta

    # Return parsed HTML
    def print_html(self):
        print("&Crawler | Printing html...")
        self.__html = self.driver.page_source.encode("utf-8")
        return self.parse_html(self.__html)
    
    # Make and write screenshot.
    def print_screenshot(self):
        page_width  = self.driver.execute_script('return document.body.scrollWidth')
        page_height = self.driver.execute_script('return document.body.scrollHeight')
        if self.p_fullsize_page_screenshot == 0:
            page_height = min(self.p_fullsize_page_screenshot_value, page_height)

        print("&Crawler | Making screenshot with {0}x{1}.".format(page_width, page_height))
        self.driver.execute_script('window.scrollTo(0, {0});'.format(self.p_scroll_screenshot_px))
        self.driver.set_window_size(page_width, page_height)
        self.driver.save_screenshot(self.save_dir + "/screenshot.png")
    
    def print_meta(self):
        print("&Crawler | Taking metadata...")
        return self.parse_meta(self.__html)
