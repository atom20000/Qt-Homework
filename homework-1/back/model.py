from PyQt5.QtCore import QAbstractTableModel, QModelIndex, Qt
import typing
from filemanager import WorkFile

class CSVModel(QAbstractTableModel):
    
    _QMap = {}

    def rowCount(self, parent: QModelIndex = QModelIndex()) -> int:
        return len(max(self._QMap.values(), key= lambda item: len(item)))

    def columnCount(self, parent: QModelIndex = QModelIndex()) -> int:
        return len(self._QMap)

    def headerData(self, section: int, orientation: Qt.Orientation, role: int = Qt.ItemDataRole.DisplayRole) -> typing.Any:
        if role != Qt.ItemDataRole.DisplayRole:
            return  #QVariant()
        if orientation == Qt.Orientation.Horizontal:
            return self._QMap.keys()[section]

    def data(self, index: QModelIndex, role: int = Qt.ItemDataRole.DisplayRole) -> typing.Any:
        if role == Qt.ItemDataRole.DisplayRole:
            return self._QMap[index.column][index.row]
        elif role == Qt.ItemDataRole.EditRole:
            pass #TODO

    def load_data(self, path: str, ) -> None:
        self._QMap = WorkFile(path).read()

    def seve_data(self, path: str) -> None:
        WorkFile(path).write(self._QMap)
