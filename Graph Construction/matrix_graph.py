import typing

from PyQt5.QtWidgets import QWidget, QTableView
from PyQt5.QtCore import QAbstractTableModel, QModelIndex, Qt, QVariant

import networkx as nx


class GraphMatrixModel(QAbstractTableModel):
    def __init__(self, parent: QWidget = None):
        super(GraphMatrixModel, self).__init__(parent)
        self.graph = nx.Graph()
        nodes_count = 5

        for i in range(nodes_count):
            self.graph.add_node(i)

    def rowCount(self, parent: QModelIndex = None) -> int:
        if parent is None:
            parent = QModelIndex()
        return len(self.graph.nodes)

    def columnCount(self, parent: QModelIndex = None) -> int:
        if parent is None:
            parent = QModelIndex()
        return len(self.graph.nodes)

    def data(self, index: QModelIndex, role: int = None) -> typing.Any:
        if role is None:
            role = Qt.DisplayRole

        if role == Qt.DisplayRole:
            return int(self.graph.has_edge(index.row(), index.column()))
        return QVariant()

    def setData(self, index: QModelIndex, value: typing.Any, role: int = ...) -> bool:
        if role == Qt.EditRole:
            if not self.checkIndex(index):
                return False
            try:
                value = int(value)
            except ValueError:
                return False
            uv = index.row(), index.column()
            if uv[0] == uv[1]:
                return False
            if abs(value) > 0:
                if not self.graph.has_edge(*uv):
                    self.graph.add_edge(*uv)
            else:
                if self.graph.has_edge(*uv):
                    self.graph.remove_edge(*uv)
            return True
        return False

    def flags(self, index: QModelIndex) -> Qt.ItemFlags:
        return Qt.ItemIsEditable | Qt.ItemIsSelectable | Qt.ItemIsEnabled

