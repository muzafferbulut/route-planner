# -*- coding: utf-8 -*-
"""
Created on Sat Mar 11 22:12:17 2023

@author: Muzaffer Bulut
"""

import requests
import pandas as pd

class Site():

    def __init__(self):
        # ctor func
        super().__init__()
        self.site_link = "https://havadurumu15gunluk.xyz/havadurumu45gunluk/630/istanbul-hava-durumu-45-gunluk.html"

    def getSiteLink(self):
        return self.site_link

    def setSiteLink(self, cityName):
        self.site_link = self.site_link.replace("istanbul", cityName)
        return self.site_link

    def scrapeData(self):
        response = requests.get(self.site_link)
        whetherData = pd.read_html(response.text)
        return whetherData
    
