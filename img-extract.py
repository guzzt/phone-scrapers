from __future__ import unicode_literals
import argparse
import pandas
import sys
from scrappers.motorola import MotorolaDownloader

if __name__ == '__main__':
    if len(sys.argv) != 2:
        print(f"Uso: {sys.argv[0]} <arquivo.xlsm>")
        exit(0)
    try:
        df = pandas.read_excel(sys.argv[1])
    except Exception as e:
        print("[-] Erro ao abrir o arquivo excel.")
        exit(0)
    df = df.iloc[:,:3]
    print(df)
    m = MotorolaDownloader()
    m.search('moto g9 plus')
    hrefs = m.getProductsLinks()
    for href in hrefs:
        m.getProductImages(href)