from PyQt5.QtWidgets import QMainWindow, QApplication, QFileDialog, QMessageBox
from gui.MainWindow_ui import Ui_CsvEditor
from back.model import CSVModel
from back.filemanager import WorkFile

class Main(QMainWindow):
    
    def __init__(self, ui: Ui_CsvEditor) -> None:
        super().__init__()
        self.path = ''
        self.ui = ui
        self.ui.setupUi(self)
        self.model = CSVModel()
        self.ui.tableView.setModel(self.model)
        self.ui.actionQuit.triggered.connect(QApplication.instance().quit)
        self.ui.actionOpen.triggered.connect(self.open_file)
        self.ui.actionSave.triggered.connect(self.save)
        self.ui.actionSave_as.triggered.connect(self.save_as_file)
        self.ui.actionAddRows.triggered.connect(self.add_rows)
        self.ui.actionAddColumns.triggered.connect(self.add_columns)
        self.ui.actionRemoveRows.triggered.connect(self.remove_rows)
        self.ui.actionRemoveColumns.triggered.connect(self.remove_columns)
        self.ui.actionAbout.triggered.connect(self.about)
        #self.ui.tableView.selectionModel().selectionChanged.connect(lambda x, y: print(self.ui.tableView.selectionModel().selectedRows()))

    def open_file(self):
        self.path = QFileDialog.getOpenFileName(filter='*.csv *.CSV')[0]
        if self.path != '':
            self.model = CSVModel(QMap= WorkFile(self.path).read())
            self.ui.tableView.setModel(self.model)

    def save(self):
        if self.path != '':
            WorkFile(self.path).write(self.model._QMap, self.model.max_row)
        else:
            self.save_as_file()

    def save_as_file(self):
        self.path = QFileDialog.getSaveFileName(filter='*.csv *.CSV')[0]
        if self.path != '':
            WorkFile(self.path).write(self.model._QMap, self.model.max_row)

    def add_rows(self):
        if (select_rows := self.ui.tableView.selectionModel().selectedRows()) and len(select_rows) !=0:
            for i in select_rows:
                self.model.insertRows(i.row() + 1, 1)
        else:
            self.model.insertRows(self.model.max_row, 1)

    def add_columns(self):
        if (select_columns := self.ui.tableView.selectionModel().selectedColumns()) and len(select_columns) !=0:
            for i in select_columns:
                self.model.insertColumns(i.column() + 1, 1)
        else:
            self.model.insertColumns(self.model.max_colums, 1)

    def remove_rows(self):
        if (select_rows := self.ui.tableView.selectionModel().selectedRows()) and len(select_rows) !=0:
            for i in select_rows:
                self.model.removeRows(i.row(), 1)
    
    def remove_columns(self):
        if (select_rows := self.ui.tableView.selectionModel().selectedColumns()) and len(select_rows) !=0:
            for i in select_rows:
                self.model.removeColumns(i.column(), 1)

    def about(self):
        return QMessageBox.aboutQt(self, self.windowTitle())