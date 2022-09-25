from PyQt5.QtCore import QAbstractTableModel, QModelIndex, Qt, QObject, QVariant
import typing
#from filemanager import WorkFile

class CSVModel(QAbstractTableModel):
    
    _QMap = {}
    match_keys = {}

    def __init__(self, parent: typing.Optional[QObject] = QObject(), QMap = {}) -> None:
        super().__init__(parent)
        self._QMap = QMap
        self.match_keys = { i:j for i, j in zip(range(self.columnCount()), self._QMap.keys())}

    def rowCount(self, parent: QModelIndex = QModelIndex()) -> int:
        return len(max(self._QMap.values(), key= lambda item: len(item)))

    def columnCount(self, parent: QModelIndex = QModelIndex()) -> int:
        return len(self._QMap)

    def headerData(self, section: int, orientation: Qt.Orientation, role: int = Qt.ItemDataRole.DisplayRole) -> typing.Any:
        if role != Qt.ItemDataRole.DisplayRole:
            return  QVariant()
        if orientation == Qt.Orientation.Horizontal:
            return QVariant(list(self._QMap.keys())[section])

    def data(self, index: QModelIndex, role: int = Qt.ItemDataRole.DisplayRole) -> typing.Any:
        if role == Qt.ItemDataRole.DisplayRole:
            return QVariant(self._QMap[self.match_keys[index.column()]][index.row()])
        elif role == Qt.ItemDataRole.EditRole:
            pass #TODO

    #def load_data(self, path: str, ) -> None:
    #    self._QMap = WorkFile(path).read()
    #
    #def seve_data(self, path: str) -> None:
    #    WorkFile(path).write(self._QMap)
