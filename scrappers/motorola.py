from selenium import webdriver
from selenium.webdriver import Firefox
from selenium.webdriver.common import by
from webdriver_manager.firefox import GeckoDriverManager
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.keys import Keys
import requests
import shutil
from os.path import join

class MotorolaDownloader(object):
    def __init__(self):
        self.__url   = 'https://www.motorola.com.br'
        self._driver = Firefox(executable_path=GeckoDriverManager().install())
        self._driver.get(self.__url)
        self._blacklist = ['capa','película',]

    def search(self,keyword):
        wait = WebDriverWait(self._driver,10)
        wait.until(EC.element_to_be_clickable((By.ID,'downshift-0-input')))
        search_input = self._driver.find_element_by_id('downshift-0-input')
        search_input.click()
        search_input.send_keys(keyword)
        search_input.send_keys(Keys.RETURN)

    def downloadImage(self,name,url):
        response = requests.get(url,stream=True)
        if response.status_code == 200:
            with open(join('img','motorola',name+'.jpg'), 'wb') as f:
                response.raw.decode_content = True
                shutil.copyfileobj(response.raw, f)

    def getProductImages(self,href):
        self._driver.get(href)
        wait = WebDriverWait(self._driver,15)
        wait.until(EC.visibility_of_element_located((By.XPATH,'//img[@class="vtex-store-components-3-x-productImageTag vtex-store-components-3-x-productImageTag--main"]')))
        imgFrame = self._driver.find_elements_by_xpath('//img[@class="vtex-store-components-3-x-productImageTag vtex-store-components-3-x-productImageTag--main"]')
        phoneName = self._driver.find_element_by_xpath('//span[@class="vtex-breadcrumb-1-x-term ph2 c-on-base"]').text
        phoneName = phoneName.replace(' ','_')
        for i,img in enumerate(imgFrame):
            src = img.get_attribute('src')
            self.downloadImage(phoneName+str(i),src)

    def getProductsLinks(self):
        try:
            wait = WebDriverWait(self._driver,10)
            wait.until(EC.visibility_of_element_located((By.ID,'gallery-layout-container')))
            galeria = self._driver.find_element_by_id('gallery-layout-container')
            sections = galeria.find_elements_by_tag_name('section')
            hrefs = []
            for section in sections:
                description = section.find_element_by_tag_name("h3").text
                blacklisted = False
                for word in description.lower().split():
                    if word in self._blacklist:
                        blacklisted = True
                        break
                if not blacklisted:
                    hrefs.append(section.find_element_by_tag_name('a').get_attribute('href'))
            return hrefs
        except Exception as e:
            self._driver.refresh()
            return self.getProductsLinks()