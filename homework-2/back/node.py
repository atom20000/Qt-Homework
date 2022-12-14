from PyQt5.QtWidgets import QGraphicsItem, QWidget, QStyle
from PyQt5.QtGui import QPainter, QPainterPath, QRadialGradient, QColor, QPen
from PyQt5.QtCore import QPointF, QRectF, Qt
from math import cos, sin, atan

class Node(QGraphicsItem):
    
    def __init__(self, graphwidget, value = None):
        super().__init__()
        self.value = value
        self.edges = []
        self.newposition = None
        self.graph = graphwidget
        self.setFlag(QGraphicsItem.GraphicsItemFlag.ItemIsMovable)
        self.setFlag(QGraphicsItem.GraphicsItemFlag.ItemSendsGeometryChanges)
        self.setCacheMode(QGraphicsItem.CacheMode.DeviceCoordinateCache)
        self.setZValue(-1)

    def addedge(self, edge):
        self.edges.append(edge)
        edge.adjust()
    
    #def calculateforces(self):
    #    if not self.scene() or self.scene().mouseGrabberItem() == self:
    #        self.newposition = self.pos()
    #        return
    #    for item in self.scene().items():
    #        if not isinstance(item, Node):
    #            continue
            
    def calculateforces(self):
        if not self.scene() or self.scene().mouseGrabberItem() == self:
            self.newposition = self.pos()
            return
        xvel = 0.0
        yvel = 0.0
        for item in self.scene().items():
            if not isinstance(item, Node):
                continue
            vec = self.mapToItem(item, 0, 0)
            dx = vec.x()
            dy = vec.y()
            l = 7 * (dx * dx + dy * dy)
            if l > 0:
                xvel += (dx * 170.0) / l
                yvel += (dy * 170.0) / l
        weight = (len(self.edges) + 1) * 25
        for edge in self.edges:
            vec = QPointF()
            if edge.source == self:
                vec = self.mapToItem(edge.destination, 0, 0)
                #print(vec, '---', self.value)
            else:
                vec = self.mapToItem(edge.source, 0, 0)
                #print(vec, '---', self.value)
                #a = 0.1 - (atan(vec.x()/vec.y()) if vec.y() != 0 else 0)
                #xvel += vec.x()*cos(a) - vec.y()*sin(a)
                #yvel += vec.y()*cos(a) + vec.x()*sin(a)
            xvel -= vec.x() / weight
            yvel -= vec.y() / weight

        if abs(xvel) < 0.55 and abs(yvel) < 0.55:
            xvel = yvel = 0
        sceneRect = self.scene().sceneRect()
        self.newposition = self.pos() + QPointF(xvel, yvel)
        self.newposition.setX(min(max(self.newposition.x(), sceneRect.left() + 10), sceneRect.right() - 10))
        self.newposition.setY(min(max(self.newposition.y(), sceneRect.top() + 10), sceneRect.bottom() - 10))

    def advanceposition(self):
        if self.newposition == self.pos():
            return
        self.setPos(self.newposition)
        return True

    def boundingRect(self):
        adjust = 2
        return QRectF(-10 - adjust, -10 - adjust, 23 + adjust, 23 + adjust)

    def shape(self):
        path = QPainterPath()
        path.addEllipse(-10, -10, 20, 20)
        return path
    
    def paint(self, painter: QPainter, option, widget) -> None:
        painter.setPen(Qt.PenStyle.NoPen)
        painter.setBrush(Qt.GlobalColor.darkGray)
        painter.drawEllipse(-7, -7, 20, 20)
        
        #gradient = QRadialGradient(-3, -3, 10)
        #if option.state & QStyle.StateFlag.State_Sunken:
        #    gradient.setCenter(3, 3)
        #    gradient.setFocalPoint(3, 3)
        #    gradient.setColorAt(1, QColor(Qt.GlobalColor.yellow).lighter(120))
        #    gradient.setColorAt(0, QColor(Qt.GlobalColor.darkYellow).lighter(120))
        #else:
        #    gradient.setColorAt(0, Qt.GlobalColor.blue)
        #    gradient.setColorAt(1, Qt.GlobalColor.darkYellow)
        painter.setBrush(Qt.GlobalColor.blue)
        painter.setPen(QPen(Qt.GlobalColor.black, 0))
        painter.drawEllipse(-10, -10, 20, 20)

        font = painter.font()
        font.setPointSize(8)
        painter.setFont(font)
        painter.setPen(Qt.GlobalColor.lightGray)
        painter.drawText(QRectF(-5, -7, 20, 20), self.value)

    def itemChange(self, change: QGraphicsItem.GraphicsItemChange, value):
        if change == QGraphicsItem.GraphicsItemChange.ItemPositionHasChanged:
            for edge in self.edges:
                edge.adjust()
            self.graph.itemmoved()
        return QGraphicsItem.itemChange(self, change, value)

    def mousePressEvent(self, event):
        self.update()
        super().mousePressEvent(event)

    def mouseReleaseEvent(self, event):
        self.update()
        super().mouseReleaseEvent(event)
