from selenium import webdriver
from selenium.webdriver import Firefox
from selenium.webdriver.common import by
from webdriver_manager.firefox import GeckoDriverManager
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.keys import Keys

class MotorolaDownloader(object):
    def __init__(self):
        self.__url   = 'https://www.motorola.com.br'
        self._driver = Firefox(executable_path=GeckoDriverManager().install())
        self._driver.get(self.__url)

    def search(self,keyword):
        wait = WebDriverWait(self._driver,10)
        wait.until(EC.element_to_be_clickable((By.ID,'downshift-0-input')))
        search_input = self._driver.find_element_by_id('downshift-0-input')
        search_input.click()
        search_input.send_keys(keyword)
        search_input.send_keys(Keys.RETURN)
        wait = WebDriverWait(self._driver,10)
        wait.until(EC.visibility_of_element_located((By.CLASS_NAME,'vtex-search-result-3-x-galleryTitle--layout t-heading-1')))
        return
    
    def getProducts(self):
        try:
            sections = self._driver.find_element_by_tag_name('section')
            for section in sections:
                
                href = section.find_element_by_class_name('vtex-store-link-0-x-link vtex-store-link-0-x-link--product-more-colors')
                href.click()
        except Exception as e:
            print(str(e))