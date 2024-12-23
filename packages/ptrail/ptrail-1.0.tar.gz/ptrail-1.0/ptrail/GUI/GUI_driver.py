"""
    This file launches PTRAIL's GUI module.

    | Author: Yaksh J Haranwala
"""
from PyQt5 import QtWidgets
import sys
from ptrail.GUI.gui import Ui_MainWindow

import os
os.environ['QTWEBENGINE_CHROMIUM_FLAGS'] = '--no-sandbox'


def run_app():
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow(MainWindow)
    MainWindow.showMaximized()
    sys.exit(app.exec_())


if __name__ == "__main__":
    run_app()