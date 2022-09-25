from PyQt5.QtWidgets import QMainWindow
from gui.MainWindow_ui import Ui_CsvEditor
from back.model import CSVModel
from back.filemanager import WorkFile


class Main(QMainWindow):
    
    def __init__(self, ui: Ui_CsvEditor) -> None:
        super().__init__()
        self.ui = ui
        self.ui.setupUi(self)
        self.model = CSVModel(QMap=WorkFile('/home/atom/atom/Qt-Homework/homework-1/back/addresses.csv').read())
        self.ui.tableView.setModel(self.model)

