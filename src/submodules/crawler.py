from resources.globals import os, utils, consts, Path
from resources.exceptions import NotInstalledLibrary
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService

class Crawler():
    def __makeDirs(self):
        os.makedirs(os.path.join(self.save_dir, "assets"), exist_ok=True)
        os.makedirs(os.path.join(self.save_dir, "css"), exist_ok=True)
        os.makedirs(os.path.join(self.save_dir, "scripts"), exist_ok=True)

    def __init__(self, save_dir):
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
        self.driver.get(url)
        self.driver.implicitly_wait(5)
    
    def print_html(self):
        print("&Crawler | Printing html...")
        return self.driver.page_source.encode("utf-8")
    
    def print_screenshot(self):
        page_width  = self.driver.execute_script('return document.body.scrollWidth')
        page_height = self.driver.execute_script('return document.body.scrollHeight')

        print("&Crawler | Making screenshot with {0}x{1}.".format(page_width, page_height))
        self.driver.set_window_size(page_width, page_height)
        self.driver.save_screenshot(self.save_dir + "/screenshot.png")
