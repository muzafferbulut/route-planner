# -*- coding: utf-8 -*-
"""
Created on Sat Mar 11 22:12:17 2023

@author: Muzaffer Bulut
"""
import io
import pandas as pd
import sys
import folium
from folium.plugins.draw import Draw
from shapely.geometry import LineString
from simplification.cutil import simplify_coords
import geopandas as gpd
from scrapper import Site
from PyQt5.uic import loadUi
from PyQt5 import QtWebEngineWidgets
from PyQt5.QtWidgets import QApplication, QMainWindow, QFileDialog, QMessageBox

class RoutePlanner(QMainWindow):
    
    def __init__(self):
        super(RoutePlanner, self).__init__()
        loadUi('route_planner.ui', self)
        
        self.openFilePattButton.clicked.connect(self.openFile)
        self.getReportButton.accepted.connect(self.generateReport)
        self.getReportButton.rejected.connect(self.close)
        self.horizontalSlider.valueChanged.connect(self.getSliderValue)

    def getSliderValue(self):
        self.sliderLabel.setText(str(self.horizontalSlider.value()))
        return self.horizontalSlider.value()
    
    def openFile(self):
        self.selectedFile = []
        self.fileDialog = QFileDialog()
        self.fileDialog.setNameFilter("Excel File (*.xlsx)")
        self.fileDialog.setFileMode(QFileDialog.ExistingFile)
        self.fileDialog.exec_()
        self.selectedFile = self.fileDialog.selectedFiles()
        
        if len(self.selectedFile)>0:
            self.citiesFile = self.selectedFile[0]
            self.filePathLineEdit.setText(self.citiesFile)
        else:
            messageBox = QMessageBox()
            messageBox.setIcon(QMessageBox.Information)
            messageBox.setText("Bir dosya seçilmedi.")
            messageBox.setWindowTitle("Bilgi")
            messageBox.setStandardButtons(QMessageBox.Ok)
            messageBox.exec_()
            
    def readCities(self, filename):
        data = pd.read_excel("cities.xlsx")
        return data

    def generateReport(self):
        site = Site()
        
        citiesDf = self.readCities(self.selectedFile)
        cities = citiesDf.values
        
        for i in range(len(cities)):
            
            city = cities[i, 0]
            
            site.setSiteLink(city)
            
            data = site.scrapeData()
            
            ret = site.cleanData(data)
            
            print(ret)
        
        

if __name__ == '__main__':
    app = QApplication(sys.argv)
    route_planner = RoutePlanner()
    route_planner.show()
    sys.exit(app.exec_())