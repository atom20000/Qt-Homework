#!/usr/bin/env python3

import sys
from gui.MainWindow import Main
from PyQt5.QtWidgets import QApplication
from gui.MainWindow_ui import Ui_BinaryTree

if __name__ == '__main__':
    app = QApplication(sys.argv)
    main = Main(Ui_BinaryTree())
    main.show()
    sys.exit(app.exec_())