from PyQt5.QtWidgets import QGraphicsItem, QWidget
from PyQt5.QtGui import QPainter

class Node(QGraphicsItem):
    
    def __init__(self, edges, position, qwidget, value = 1):
        self.value = value
        self.edges = edges
        self.position = position
        self.qwidget = qwidget
    
    def paint(self, painter: QPainter, option: 'QStyleOptionGraphicsItem', widget) -> None:
        return super().paint(painter, option, widget)
