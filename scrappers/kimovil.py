from __future__ import unicode_literals
import requests
from pandas import read_excel
from urllib.parse import quote
from bs4 import BeautifulSoup
from difflib import SequenceMatcher
import json,sys
from os.path import exists,join
from os import mkdir,getcwd
import shutil

from requests.api import get

class KimovilImageDownload(object):
    def __init__(self):
        self.__searchUrl = 'https://www.kimovil.com:443/_json/autocomplete_devicemodels_joined.json?device_type=0&name='
        self.__headers = {"User-Agent": "Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:92.0) Gecko/20100101 Firefox/92.0", "Accept": "*/*", "Accept-Language": "pt-PT,pt;q=0.8,en;q=0.5,en-US;q=0.3", "Accept-Encoding": "gzip, deflate", "Sec-Fetch-Dest": "empty", "Sec-Fetch-Mode": "cors", "Sec-Fetch-Site": "same-origin", "Referer": "https://www.kimovil.com/pt/onde-comprar-samsung-galaxy-s21-5g", "Te": "trailers"}
        self.__session = requests.session()
        self.__deviceUrl = 'https://www.kimovil.com/pt/onde-comprar-'

    def start(self,keyword,fornecedor):
        results = self.getDeviceInfo(keyword)
        uri     = self.getDeviceUri(keyword,results)
        linkImages = self.getImagesLinks(self.__deviceUrl+uri)
        for i,link in enumerate(linkImages):
            imgName = uri.replace('-','_')
            if not 'https:' in link:
                link = 'https:' + link
            if self.downloadImage(fornecedor,link,imgName+str(i)):
                print(f'[+] Download concluido {link}')

    def getDeviceInfo(self,keyword):
        response = self.__session.get(self.__searchUrl+quote(keyword),headers=self.__headers)
        if response.status_code == 200:
            results = json.loads(response.content)['results']
            return results
        else:
            raise f'[-] ERRO: codigo retornado: {self.__baseUrl+quote(keyword)} => {response.status_code}'

    def getDeviceUri(self,keyword,results):
        maxim = 0.
        uri   = ''
        for r in results:
            if r['result_type'] == 'smartphones':
                rate = SequenceMatcher(None,keyword.lower(),r['full_name'].lower()).ratio()
                if rate > maxim:
                    maxim = rate
                    uri = r['url']
        return uri

    def getImagesLinks(self,url):
        response = self.__session.get(url)
        images = []
        if response.status_code == 200:
            bsObj = BeautifulSoup(response.text,features='lxml')
            itens = bsObj.find_all('li',{'class':'item image'})
            for i in itens:
                images.append(i.find('a',{'class':'kigallery'})['href'])
        return images

    def downloadImage(self,fornecedor,linkImage,imgName):
        response = requests.get(linkImage,stream=True)
        if not exists(join(getcwd(),'img')):
            mkdir(join(getcwd(),'img'))
        if not exists(join(getcwd(),fornecedor.lower())):
            mkdir(join(getcwd(),fornecedor.lower()))
        if response.status_code == 200:
            with open(join(getcwd(),'img',fornecedor.lower(),imgName+'.jpg'), 'wb') as f:
                response.raw.decode_content = True
                shutil.copyfileobj(response.raw, f)
            return True
        else:
            return False


if __name__ == '__main__':
    k = KimovilImageDownload()
    k.start('mi 11 ultra','xiaomi')