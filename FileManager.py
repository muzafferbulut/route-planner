from PyQt5.QtWidgets import QFileDialog, QMessageBox
import pandas as pd

class FileManager():
    
    def __init__(self):
        self.messagebox = QMessageBox()
        self.filedialog = QFileDialog()
    
    def selectFile(self):
        selectedFile = []
        self.filedialog = QFileDialog()
        self.filedialog.setNameFilter("Excel File (*.xlsx);;ESRI Shapefile (*.shp)")
        self.filedialog.setFileMode(QFileDialog.ExistingFile)
        self.filedialog.exec_()
        selectedFile = self.filedialog.selectedFiles()
        
        # dosya seçilmediyse uyarı göster
        if len(selectedFile)>0:
            citiesFile = selectedFile[0]
            return citiesFile
        else:
            self.infoMessage("Bir dosya seçilmedi!")
    
    def readExcel(self, path):
        return pd.read_excel(path)
        
    def infoMessage(self, text):
            self.messagebox.setIcon(QMessageBox.Information)
            self.messagebox.setText(text)
            self.messagebox.setWindowTitle("Bilgi")
            self.messagebox.setStandardButtons(QMessageBox.Ok)
            self.messagebox.exec_()
    
    def warningMessage(self, text):
        self.messageBox.setIcon(QMessageBox.Warning)
        self.messageBox.setWindowTitle("Uyarı")
        self.messageBox.setText(text)
        self.messageBox.setStandardButtons(QMessageBox.Ok)
    
    def saveReport(self, df):
        filename, _ = QFileDialog.getSaveFileName(None, "Excel Dosyası Kaydet", "report.xlsx", "Excel Dosyası (*.xlsx)")
        if not filename:
            exit()
        if not filename.endswith(".xlsx"):
            filename += ".xlsx"
        df.to_excel(filename)