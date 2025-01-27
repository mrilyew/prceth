from resources.globals import os, utils, consts, Path
from resources.exceptions import NotInstalledLibrary
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService

class Crawler():
    def __init__(self, save_dir):
        self.save_dir = save_dir
    
    def crawl_site(self, url):
        os.makedirs(os.path.join(self.save_dir, "assets"), exist_ok=True)
        os.makedirs(os.path.join(self.save_dir, "css"), exist_ok=True)
        os.makedirs(os.path.join(self.save_dir, "scripts"), exist_ok=True)

        _chrome_path    = consts["tmp"] +"\\chrome"
        _webdriver_path = _chrome_path  + "\\chromedriver-win64\\chromedriver.exe"
        _chromium_portable_path = _chrome_path  + "\\chromium\\chrome.exe"
        if Path(_webdriver_path).is_file() == False:
            _crawl = utils.download_chrome_driver()

        if Path(_chromium_portable_path).is_file() == False:
            raise NotInstalledLibrary("Chromium portable is not installed at path /storage/tmp/chrome/chromium (https://commondatastorage.googleapis.com/chromium-browser-snapshots/Win_x64/1411404/chrome-win.zip)")
        
        _options = webdriver.ChromeOptions()
        _options.add_argument('--headless')
        _options.add_argument("user-data-dir={0}".format(_chrome_path + "\\chromium\\user-data"))
        _options.binary_location = _chromium_portable_path
        _options.add_argument('--no-sandbox')
        _options.add_argument('--disable-gpu')
        service = ChromeService(executable_path=_webdriver_path,chrome_options=_options,log_path='NUL')
        driver  = webdriver.Chrome(service=service, options=_options)
        driver.get(url)
        driver.implicitly_wait(5)

        html = driver.page_source
        print(html)
        driver.quit()

        return None
