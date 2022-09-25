#!/usr/bin/env python3

import sys
from PyQt5.QtWidgets import QMainWindow, QApplication
from gui.MainWindow import Ui_CsvEditor

class CSVEditor(QMainWindow):
    
    def __init__(self, ui: Ui_CsvEditor) -> None:
        super().__init__()
        self.ui = ui
        self.ui.setupUi(self)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    CSVEditor(Ui_CsvEditor()).show()
    sys.exit(app.exec_())