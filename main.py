# -*- coding: utf-8 -*-
"""
Created on Sat Mar 11 22:12:17 2023

@author: Muzaffer Bulut
"""

import sys
from PyQt5.QtWidgets import QApplication, QMainWindow
from PyQt5.uic import loadUi
from scrapper import Site
from PyQt5 import QtWebEngineWidgets
import folium
import geopandas as gpd


class RoutePlanner(QMainWindow):
    def __init__(self):
        super(RoutePlanner, self).__init__()
        loadUi('route_planner.ui', self)
        
        self.openFilePattButton.clicked.connect(self.open_file)
        self.exportButton.clicked.connect(self.export_data)
        self.getReportButton.accepted.connect(self.generate_report)
        self.getReportButton.rejected.connect(self.close)
        
        # folium map
        foliumMap = folium.Map(location=[38.52077, 35.85411], zoom_start=6)
        data = foliumMap._repr_html_()
        self.webEngineView.setHtml(data)

    def open_file(self):
        print("clicked tool button")

    def export_data(self):
        print("clicked export data!")

    def generate_report(self):
        print("clicked get report")

if __name__ == '__main__':
    app = QApplication(sys.argv)
    route_planner = RoutePlanner()
    route_planner.show()
    sys.exit(app.exec_())