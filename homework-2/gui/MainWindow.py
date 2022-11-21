from PyQt5.QtWidgets import QMainWindow, QApplication, QFileDialog
from gui.MainWindow_ui import Ui_BinaryTree
from back.graphwidget import Graphwidget

class Main(QMainWindow):
    
    def __init__(self, ui: Ui_BinaryTree) -> None:
        super().__init__()
        self.path = ''
        self.ui = ui
        self.ui.centralwidget = Graphwidget()
        self.ui.setupUi(self)
        self.ui.actionQuit.triggered.connect(QApplication.instance().quit)
        self.ui.actionOpen.triggered.connect(self.open_file)
        
    def open_file(self):
        self.path = QFileDialog.getOpenFileName(filter='*.json *.JSON')[0]
        if self.path != '':
            pass