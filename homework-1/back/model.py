from PyQt5.QtCore import QAbstractTableModel, QModelIndex, Qt, QObject, QVariant
import typing

class CSVModel(QAbstractTableModel):
    
    _QMap = {}

    @property
    def match_keys(self):
        return { i:j for i, j in zip(range(self.max_colums), self._QMap.keys())}

    @property
    def max_row(self):
        return len(max(self._QMap.values(), key= lambda item: len(item), default=[]))

    @property
    def max_colums(self):
        return len(self._QMap)

    def __init__(self, parent: typing.Optional[QObject] = QObject(), QMap = {}) -> None:
        super().__init__(parent)
        self._QMap = QMap
        #self.match_keys = { i:j for i, j in zip(range(self.columnCount()), self._QMap.keys())}

    def rowCount(self, parent: QModelIndex = QModelIndex()) -> int:
        return self.max_row if not parent.isValid() else 0

    def columnCount(self, parent: QModelIndex = QModelIndex()) -> int:
        return self.max_colums if not parent.isValid() else 0

    def headerData(self, section: int, orientation: Qt.Orientation, role: int = Qt.ItemDataRole.DisplayRole) -> typing.Any:
        if role != Qt.ItemDataRole.DisplayRole:
            return  QVariant()
        if orientation == Qt.Orientation.Horizontal and role == Qt.ItemDataRole.DisplayRole:
            return QVariant(list(self._QMap.keys())[section])
        elif orientation == Qt.Orientation.Vertical and role == Qt.ItemDataRole.DisplayRole:
            return QVariant('  ')
        if orientation == Qt.Orientation.Horizontal and role == Qt.ItemDataRole.EditRole:
            return QVariant(list(self._QMap.keys())[section])
        return QVariant()

    def data(self, index: QModelIndex, role: int = Qt.ItemDataRole.DisplayRole) -> typing.Any:
        if role == Qt.ItemDataRole.DisplayRole:
            return QVariant(self._QMap[self.match_keys[index.column()]][index.row()])
        elif role == Qt.ItemDataRole.EditRole:
            return QVariant(self._QMap[self.match_keys[index.column()]][index.row()])

    def flags(self, index: QModelIndex) -> Qt.ItemFlags:
        return super().flags(index) | Qt.ItemFlag.ItemIsEditable if index.isValid() else Qt.ItemFlag.ItemIsEnabled

    def insertRows(self, row: int, count: int, parent: QModelIndex = QModelIndex()) -> bool:
        super().beginInsertRows(QModelIndex(), row, row + count - 1)
        if len(self._QMap.keys()) == 0:
            self.insertColumns(0, 1)
        for r in range(row, row + count):
            for i in self._QMap.keys():
                self._QMap[i].insert(row, '')
        super().endInsertRows()
        return True

    def insertColumns(self, column: int, count: int, parent: QModelIndex = QModelIndex()) -> bool:
        super().beginInsertColumns(QModelIndex(), column, column + count - 1)
        tmp_lst = list(self._QMap.items())
        for c in range(column, column + count):
            tmp_lst.insert(column, ( self.generate_header_name(), ['' for i in range(self.max_row)]))
        self._QMap = {i[0] : i[1] for i in tmp_lst}
        super().endInsertColumns()
        return True

    def removeRows(self, row: int, count: int, parent: QModelIndex = QModelIndex()) -> bool:
        super().beginRemoveRows(QModelIndex(), row, row + count - 1)
        for r in range(row, row + count):
            for i in self._QMap.keys():
                self._QMap[i].pop(row)
        super().endRemoveRows()
        return True

    def removeColumns(self, column: int, count: int, parent: QModelIndex = QModelIndex()) -> bool:
        super().beginRemoveColumns(QModelIndex(), column, column + count - 1)
        for c in range(column, column + count):
            self._QMap.pop(self.match_keys[c])
        super().endRemoveColumns()
        return True

    def setData(self, index: QModelIndex, value: typing.Any, role: int = Qt.ItemDataRole.EditRole) -> bool:
        if role == Qt.ItemDataRole.EditRole:
            self._QMap[self.match_keys[index.column()]][index.row()] = str(value)
            super().dataChanged.emit(index, index, [Qt.ItemDataRole.DisplayRole, Qt.ItemDataRole.EditRole])
            return True
    
    def setHeaderData(self, section: int, orientation: Qt.Orientation, value: typing.Any, role: int = Qt.ItemDataRole.EditRole) -> bool:
        if role == Qt.ItemDataRole.EditRole and orientation == Qt.Orientation.Horizontal:
            data = self._QMap.pop([self.match_keys[section]])
            tmp_lst = list(self._QMap.items())
            tmp_lst.insert(section, ( value, data))
            self._QMap = {i[0] : i[1] for i in tmp_lst}
            super().headerDataChanged.emit(section, section, [Qt.ItemDataRole.DisplayRole, Qt.ItemDataRole.EditRole])
            return True
    
    def generate_header_name(self):
        count = 1
        while ' '*count in self._QMap.keys(): count+=1
        return ' '*count