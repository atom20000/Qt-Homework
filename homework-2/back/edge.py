from PyQt5.QtWidgets import QGraphicsItem
from PyQt5.QtGui import QPainter, QPen, QPolygonF
from PyQt5.QtCore import QLineF, QPointF, QRectF, QSizeF, Qt
from math import atan2, sin, cos, pi


class Edge(QGraphicsItem):
    
    def __init__(self, source, destination):
        self.source = source
        self.destination = destination
        self.sourcepoint = None
        self.destpoint = None
        self.arrowsize = 10
        self.adjust()
    
    def adjust(self):
        if (not self.source)  or (not self.destination):
            return
        line = QLineF(QGraphicsItem.mapFromItem(self.source, 0, 0), QGraphicsItem.mapFromItem(self.destination, 0, 0))
        length = line.length()
        QGraphicsItem.prepareGeometryChange()
        if (length > 20.0):
            edgeoffset = QPointF((line.dx()*10) / length, (line.dy()*10) / length)
            self.sourcepoint = line.p1() + edgeoffset
            self.destpoint = line.p2() - edgeoffset
        else:
            self.sourcepoint = self.destpoint = line.p1()

    def boundingRect(self) -> QRectF:
        if (not self.source)  or (not self.destination):
            return
        penWidth = 1.0
        extra = (penWidth + self.arrowsize) / 2.0
        return QRectF(self.sourcepoint, QSizeF(self.destpoint.x() - self.sourcepoint.x(),
                                                self.destpoint.y() - self.sourcepoint.y())).normalized().adjusted(-extra, -extra, extra, extra)        

    def paint(self, painter: QPainter, option: 'QStyleOptionGraphicsItem', widget) -> None:
        if (not self.source)  or (not self.destination):
            return
        line = QLineF(self.sourcepoint, self.destpoint)
        if line.length() == 0.0:
            return
        painter.setPen(QPen(Qt.GlobalColor.black, 1, Qt.PenStyle.SolidLine, Qt.PenCapStyle.RoundCap, Qt.PenJoinStyle.RoundJoin))
        painter.drawLine(line)
        angle = atan2(-line.dy(), line.dx())
        sourcearrowp1 = self.sourcepoint + QPointF(sin(angle + pi / 3) * self.arrowsize,
                                                   cos(angle + pi / 3) * self.arrowsize)
        sourcearrowp2 = self.sourcepoint + QPointF(sin(angle + pi - pi / 3) * self.arrowsize,
                                                   cos(angle + pi - pi / 3) * self.arrowsize)
        destarrowp1 = self.destpoint + QPointF(sin(angle - pi / 3) * self.arrowsize,
                                               cos(angle - pi / 3) * self.arrowsize)
        destarrowp2 = self.destpoint + QPointF(sin(angle - pi + pi / 3) * self.arrowsize,
                                               cos(angle - pi + pi / 3) * self.arrowsize)
        painter.setBrush(Qt.GlobalColor.black)
        painter.drawPolygon(QPolygonF([line.p1(), sourcearrowp1, sourcearrowp2]))
        painter.drawPolygon(QPolygonF([line.p2(), destarrowp1, destarrowp2]))