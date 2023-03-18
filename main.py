# -*- coding: utf-8 -*-
"""
Created on Sat Mar 11 22:12:17 2023

@author: Muzaffer Bulut
"""

import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QFileDialog
from PyQt5.uic import loadUi
from scrapper import Site
from PyQt5 import QtWebEngineWidgets
import folium
import geopandas as gpd


class RoutePlanner(QMainWindow):
    def __init__(self):
        super(RoutePlanner, self).__init__()
        loadUi('route_planner.ui', self)
        
        self.openFilePattButton.clicked.connect(self.openFile)
        self.exportButton.clicked.connect(self.exportData)
        self.getReportButton.accepted.connect(self.generateReport)
        self.getReportButton.rejected.connect(self.close)
        self.horizontalSlider.valueChanged.connect(self.getSliderValue)
        
        # folium map
        self.foliumMap = folium.Map(location=[38.52077, 35.85411], zoom_start=6)
        
        dataShp = gpd.read_file("C:\MyFiles\Kişisel\cekim.shp")
        
        folium.GeoJson(dataShp).add_to(self.foliumMap)
        
        self.webEngineView.setHtml(self.foliumMap._repr_html_())

    def getSliderValue(self):
        self.sliderLabel.setText(str(self.horizontalSlider.value()))
    
    def openFile(self):
        self.selectedFile = []
        self.fileDialog = QFileDialog()
        self.fileDialog.setNameFilter("ESRI Shapefiles (*.shp)")
        self.fileDialog.setFileMode(QFileDialog.ExistingFile)
        self.fileDialog.exec_()
        self.selectedFile = self.fileDialog.selectedFiles()
        self.filePathLineEdit.setText(self.selectedFile[0])

    def exportData(self):
        print("clicked export button.")

    def generateReport(self):
        print("clicked get report button.")

if __name__ == '__main__':
    app = QApplication(sys.argv)
    route_planner = RoutePlanner()
    route_planner.show()
    sys.exit(app.exec_())