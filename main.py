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
        
        # folium map
        self.foliumMap = folium.Map(location=[38.52077, 35.85411], zoom_start=6)
        self.webEngineView.setHtml(self.foliumMap._repr_html_())

    def openFile(self):
        self.selectedFile = []
        self.fileDialog = QFileDialog()
        self.fileDialog.exec_()
        self.selectedFile = self.fileDialog.selectedFiles()
        self.filePathLineEdit.setText(self.selectedFile[0])

    def exportData(self):
        print(self.selectedFile[0])

    def generateReport(self):
        print("clicked get report")

if __name__ == '__main__':
    app = QApplication(sys.argv)
    route_planner = RoutePlanner()
    route_planner.show()
    sys.exit(app.exec_())