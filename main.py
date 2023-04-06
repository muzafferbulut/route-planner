# -*- coding: utf-8 -*-
"""
Created on Sat Mar 11 22:12:17 2023

@author: Muzaffer Bulut
"""
import sys
import pandas as pd
from Scrapper import Site
from FileManager import FileManager
from PyQt5.uic import loadUi
from PyQt5.QtWidgets import QApplication, QMainWindow
from PyQt5 import QtWebEngineWidgets

class RoutePlanner(QMainWindow):

    def __init__(self):
        super(RoutePlanner, self).__init__()
        loadUi('files/route_planner.ui', self)

        self.fileManager = FileManager()
        self.site = Site()

        self.openFilePattButton.clicked.connect(self.openFile)
        self.getReportButton.accepted.connect(self.generateReport)
        self.getReportButton.rejected.connect(self.close)
        self.horizontalSlider.valueChanged.connect(self.getSliderValue)

    def getSliderValue(self):
        self.sliderLabel.setText(str(self.horizontalSlider.value()))
        return self.horizontalSlider.value()

    def openFile(self):
        self.filePath = self.fileManager.selectFile()
        self.filePathLineEdit.setText(self.filePath)

    def generateReport(self):
        cities = self.fileManager.readExcel(self.filePath).values

        report = pd.DataFrame({"il":self.site.getTimeSeries()}).transpose()

        for i in range(len(cities)):

            # şehirlere tek tek istek atıp gelen verileri yazma
            city = cities[i, 0]
            link = self.site.getSiteLink().replace("istanbul",city)
            data = self.site.scrapeData(link)
            content = self.site.cleanData(data)

            row = content.iloc[1]
            row = pd.DataFrame({city:row})   
            row = row.transpose()

            report = pd.concat([report, row])
            report_term = self.getSliderValue()
            report = report.iloc[:,:report_term]

        try:
            self.fileManager.saveReport(report)
            self.fileManager.infoMessage("Raporlama tamamlandı.")
        except:
            self.fileManager.warningMessage("Raporlamada bir hata oluştu!")

if __name__ == '__main__':
    app = QApplication(sys.argv)
    route_planner = RoutePlanner()
    route_planner.show()
    sys.exit(app.exec_())