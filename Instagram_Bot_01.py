from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.common.keys import Keys
import time


class InstagramBot:
    def __init__(self):
        self.browser = webdriver.Chrome("chromedriver.exe")
        self.browser.delete_all_cookies()
        self.browser.maximize_window()

    def wait_for_object(self, type, string):
        return WebDriverWait(self.browser, 3).until(ec.presence_of_element_located((type, string)))

    def wait_for_objects(self, type, string):
        return WebDriverWait(self.browser, 3).until(ec.presence_of_all_elements_located((type, string)))

    def get_website(self, url):
        self.browser.get(url)

        window = self.wait_for_object(By.CSS_SELECTOR, '#sp-cc-accept')
        window.click()

    def search(self, search_string):
        window = self.wait_for_object(By.CSS_SELECTOR, '#twotabsearchtextbox')
        window.send_keys(search_string)
        time.sleep(1)
        window.send_keys(Keys.ENTER)

        window = self.wait_for_objects(By.CSS_SELECTOR, '.a-size-base-plus.a-color-base.a-text-normal')
        window[0].click()


bot = InstagramBot()
bot.get_website("https://www.amazon.de/?tag=operadesktop14-sd-de-21")
bot.search("Protein")