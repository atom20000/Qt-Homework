from dataclasses import dataclass
from PyQt5.QtCore import QAbstractTableModel, QModelIndex
import typing
from filemanager import WorkFile

class TeacherModel(QAbstractTableModel):
    
    def rowCount(self, parent: QModelIndex = QModelIndex()) -> int:
        return len(max(self._QMap.values(), key= lambda item: len(item)))

    def columnCount(self, parent: QModelIndex = QModelIndex()) -> int:
        return len(self._QMap)

    def data(self, index: QModelIndex, role: int = 1) -> typing.Any:
        return self._QMap[index.row]

    def load_data(self, path: str, ) -> None:
        WorkFile(path).read()

    def seve_data(self, path: str) -> None:
        WorkFile(path).write()
    _QMap = {}
