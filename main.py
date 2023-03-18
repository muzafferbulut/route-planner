# -*- coding: utf-8 -*-
"""
Created on Sat Mar 11 22:12:17 2023

@author: Muzaffer Bulut
"""
import io
import sys
import folium
from folium.plugins.draw import Draw
import geopandas as gpd
from scrapper import Site
from PyQt5.uic import loadUi
from PyQt5 import QtWebEngineWidgets
from PyQt5.QtWidgets import QApplication, QMainWindow, QFileDialog

class RoutePlanner(QMainWindow):
    def __init__(self):
        super(RoutePlanner, self).__init__()
        loadUi('route_planner.ui', self)
        
        self.openFilePattButton.clicked.connect(self.openFile)
        self.exportButton.clicked.connect(self.exportData)
        self.getReportButton.accepted.connect(self.generateReport)
        self.getReportButton.rejected.connect(self.close)
        self.horizontalSlider.valueChanged.connect(self.getSliderValue)
        self.getMap()

    def getMap(self):
        self.foliumMap = folium.Map(location=[38.52077, 35.85411], zoom_start=6)

        Draw(
            export=False,
            position="topleft",
            draw_options={
                "polyline": False,
                "rectangle": False,
                "circle": False,
                "circlemarker": False,
            },
            edit_options={"poly": {"allowIntersection": False}},
        ).add_to(self.foliumMap)
        
        data = io.BytesIO()
        self.foliumMap.save(data, close_file=False)
        self.webEngineView.setHtml(data.getvalue().decode())

    def getSliderValue(self):
        self.sliderLabel.setText(str(self.horizontalSlider.value()))
    
    def openFile(self):
        self.selectedFile = []
        self.fileDialog = QFileDialog()
        self.fileDialog.setNameFilter("ESRI Shapefiles (*.shp)")
        self.fileDialog.setFileMode(QFileDialog.ExistingFile)
        self.fileDialog.exec_()
        self.selectedFile = self.fileDialog.selectedFiles()[0]
        self.filePathLineEdit.setText(self.selectedFile)
        
        self.drawRouteOnMap()

    def drawRouteOnMap(self):
        newRoute = gpd.read_file(self.selectedFile)
        newRoute.explore(m=self.foliumMap)
        self.webEngineView.setHtml(self.foliumMap._repr_html_())


        
    def exportData(self):
        print("clicked export button.")

    def generateReport(self):
        print("clicked get report button.")

if __name__ == '__main__':
    app = QApplication(sys.argv)
    route_planner = RoutePlanner()
    route_planner.show()
    sys.exit(app.exec_())