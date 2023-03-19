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
from PyQt5.QtWidgets import QApplication, QMainWindow, QFileDialog

class RoutePlanner(QMainWindow):
    def __init__(self):
        super(RoutePlanner, self).__init__()
        loadUi('route_planner.ui', self)
        
        self.openFilePattButton.clicked.connect(self.openFile)
        self.exportButton.clicked.connect(self.exportData)
        self.resetMapButton.clicked.connect(self.resetMap)
        self.getReportButton.accepted.connect(self.generateReport)
        self.getReportButton.rejected.connect(self.close)
        self.horizontalSlider.valueChanged.connect(self.getSliderValue)
        self.getMap()

    def getMap(self):
        self.foliumMap = folium.Map(location=[38.82, 35.15], zoom_start=6)

        Draw(
            export=False,
            position="topleft",
            draw_options={
                "polyline": True,
                "rectangle": True,
                "circle": True,
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
        self.simplifyGeom(newRoute)
        self.fitBounds(newRoute)
        self.webEngineView.setHtml(self.foliumMap._repr_html_())

    def simplifyGeom(self, newRoute, tolerance=0.00001):
        coords = [feature.geometry.coords for _, feature in newRoute.iterrows()]
        lines = [LineString(coord) for coord in coords]
        df = pd.DataFrame({'geometry': lines})
        simple_coords = [simplify_coords(line.coords, tolerance) for line in newRoute.geometry]
        simple_gdf = gpd.GeoDataFrame(geometry=[LineString(coord) for coord in simple_coords])
        for _, feature in simple_gdf.iterrows():
            folium.PolyLine(locations=feature.geometry.coords).add_to(self.foliumMap)

    def fitBounds(self, newRoute):
        min_lon, min_lat, max_lon, max_lat = newRoute.total_bounds
        if min_lon == max_lon and min_lat == max_lat:
            # Tüm değerler sıfır ise, harita boyutlarını manuel olarak ayarla
            map_center = [min_lat, min_lon]
            self.foliumMap.setView(location=map_center, zoom_start=10)
        else:
            # Harita boyutlarını otomatik olarak ayarla
            bounds = [[min_lat, min_lon], [max_lat, max_lon]] 
        self.foliumMap.fit_bounds(bounds)
        
    def resetMap(self):
        self.getMap()
        
    def exportData(self):
        print("clicked export data button")
        
    def generateReport(self):
        print("clicked generate report button")

if __name__ == '__main__':
    app = QApplication(sys.argv)
    route_planner = RoutePlanner()
    route_planner.show()
    sys.exit(app.exec_())