# -*- coding: utf-8 -*-
"""
Created on Sat Mar 11 22:12:17 2023

@author: Muzaffer Bulut
"""

from scrapper import Site
import pandas as pd
import numpy as np
from PyQt5 import QtWidgets, uic

uiFile = "route-planner.ui"

application = QtWidgets.QApplication([])
window = uic.loadUi(uiFile)

window.show()
application.exec_()
