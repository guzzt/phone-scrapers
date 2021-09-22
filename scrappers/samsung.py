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

class SamsungDownloader(object):
    def __init__(self):
        self.__url   = 'https://www.motorola.com.br'
        self._driver = Firefox(executable_path=GeckoDriverManager().install())
        self._driver.get(self.__url)
        self._blacklist = ['capa','película',]