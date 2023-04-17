# -*- coding: utf-8 -*-
"""
Created on Sat Mar 11 22:12:17 2023

@author: Muzaffer Bulut
"""

import requests
import pandas as pd
import numpy as np

class Site():

    def __init__(self):
        # ctor func
        super().__init__()
        self.site_link = "https://havadurumu15gunluk.xyz/havadurumu45gunluk/630/istanbul-hava-durumu-45-gunluk.html"

    def getSiteLink(self):
        return self.site_link

    def mappingData(self, statement):
        if "yağmurlu" in statement.lower() or "yağmur" in statement.lower() or "yağış" in statement.lower() or "sağanak" in statement.lower():
            return 3
        elif "güneşli" in statement.lower() or "güneş" in statement.lower():
            return 1
        elif "bulutlu" in statement.lower() or "bulutlar" in statement.lower():
            return 2
        else:
            return 0

    def getTimeSeries(self):
        data = self.scrapeData(self.getSiteLink())
        self.timeSeries = data["Tarih"]
        return self.timeSeries

    def scrapeData(self, link):
        response = requests.get(link)
        whetherData = pd.read_html(response.text)
        return whetherData[0]

    def cleanData(self, df):
        dataWithMapping = pd.DataFrame(columns=["Tarih", "Kod"])
        data = df[["Tarih","Hava durumu"]].values

        self.timeSeries = df["Tarih"]

        for i in range(45):
            row = {"Tarih":data[i,0], "Kod":self.mappingData(data[i,1])}
            dataWithMapping = pd.concat([dataWithMapping, pd.DataFrame(row, index=[0])], ignore_index=1)

        return dataWithMapping.transpose()
