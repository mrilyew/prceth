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
    
    # TODO: resources export
    def start_crawl(self, url):
        print("&Crawler | Capturing the page...")
        self.url = url
        self.base_url = '/'.join(self.url.split('/')[:3]) # :3
        self.driver.get(url)
        self.driver.implicitly_wait(5)

        last_height   = self.driver.execute_script('return document.body.scrollHeight')
        scroll_cycles = int(self.args.get("scroll_cycles", 10))
        scroll_iter   = 0
        while True:
            if scroll_iter > scroll_cycles:
                break

            self.driver.execute_script('window.scrollTo(0, document.body.scrollHeight);')
            time.sleep(int(self.args.get("scroll_timeout", 0)))

            new_height = self.driver.execute_script('return document.body.scrollHeight')
            if new_height == last_height:
                break

            print("&Crawler | Scrolled the page to the bottom. Current iterator: {0}, current height: {1}".format(scroll_iter, new_height))
            
            last_height = new_height
            scroll_iter += 1 
    
    def download_resource(self, url, folder_path):
        try:
            response = requests.get(url, stream=True)
            response.raise_for_status()
            basename = os.path.basename(url.split("?")[0])
            local_path = os.path.join(folder_path, basename)

            with open(local_path, 'wb') as f:
                for chunk in response.iter_content(chunk_size=8192):
                    f.write(chunk)

            print(f"&Crawler | Downloaded file {url}.")
            return basename
        except Exception as e:
            print(f"&Crawler | Error when downloading file {url} ({e}).")
            return None
    
    def parse_html(self, html):
        if int(self.args.get("download_resources", 1)) == 0:
            return html

        soup = BeautifulSoup(html, 'html.parser')
        for img in soup.find_all('img', src=True):
            img_url = img.get('src')
            if not img_url.startswith('http'):
                img_url = self.base_url + img_url
            filename = self.download_resource(img_url, os.path.join(self.save_dir, 'assets'))
            if filename:
                img['data-orig'] = img_url
                img['src'] = f"assets/{filename}"
        
        for script in soup.find_all('script', src=True):
            script_url = script.get('src')
            if int(self.args.get("save_scripts", 1)) == 1:
                if not script_url.startswith('http'):
                    script_url = self.base_url + script_url
                filename = self.download_resource(script_url, os.path.join(self.save_dir, 'scripts'))
                if filename:
                    script['data-orig'] = script_url
                    script['src'] = f"scripts/{filename}"
            else:
                script['src'] = ''

        for link in soup.find_all('link', href=True):
            if link.get('rel') and 'stylesheet' in link.get('rel'):
                css_url = link['href']
                link['data-orig'] = css_url
                if not css_url.startswith('http'):
                    css_url = self.base_url + css_url
                filename = self.download_resource(css_url, os.path.join(self.save_dir, 'css'))
                if filename:
                    link['href'] = f"css/{filename}"
                    url_pattern = re.compile(r'url\((.*?)\)')

                    if int(self.args.get("take_css", 0)) == 1:
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
                            self.download_resource(__css_asset_url_full, os.path.join(self.save_dir, 'assets'))
                            print(f"&Crawler | Downloaded asset from {link} => {__css_asset_url}")

                        css_stream_write = open(os.path.join(self.save_dir, 'css', filename), 'w')
                        css_stream_write.seek(0)
                        css_stream_write.write(__css_modified)
                        css_stream_write.truncate()

        return soup.prettify()
    
    def print_html(self):
        print("&Crawler | Printing html...")
        html = self.driver.page_source.encode("utf-8")
        return self.parse_html(html)
    
    def print_screenshot(self):
        page_width  = self.driver.execute_script('return document.body.scrollWidth')
        page_height = self.driver.execute_script('return document.body.scrollHeight')
        if int(self.args.get("fullsize_screenshots", 0)) == 0:
            page_height = min(1000, page_height)

        print("&Crawler | Making screenshot with {0}x{1}.".format(page_width, page_height))
        self.driver.execute_script('window.scrollTo(0, {0});'.format(self.args.get("screenshot_scroll", 0)))
        self.driver.set_window_size(page_width, page_height)
        self.driver.save_screenshot(self.save_dir + "/screenshot.png")
