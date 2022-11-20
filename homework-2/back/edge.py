from PyQt5.QtWidgets import QGraphicsItem, QWidget
from PyQt5.QtGui import QPainter


class Edge(QGraphicsItem):
    
    def __init__(self, source, destination):
        self.source = source
        self.destination = destination
        self.sourcepoint = None
        self.destpoint = None
        self.arrowsize = 10
    
    def paint(self, painter: QPainter, option: 'QStyleOptionGraphicsItem', widget) -> None:
        
        return super().paint(painter, option, widget)