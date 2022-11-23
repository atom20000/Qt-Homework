from PyQt5.QtWidgets import QGraphicsItem, QWidget, QStyle
from PyQt5.QtGui import QPainter, QPainterPath, QRadialGradient, QColor, QPen
from PyQt5.QtCore import QPointF, QRectF, Qt

class Node(QGraphicsItem):
    
    def __init__(self, graphwidget, value = 1):
        self.value = value
        self.edges = None
        self.newposition = None
        self.graph = graphwidget
        self.setFlag(QGraphicsItem.GraphicsItemFlag.ItemIsMovable)
        self.setFlag(QGraphicsItem.GraphicsItemFlag.ItemSendsGeometryChanges)
        self.setCacheMode(QGraphicsItem.CacheMode.DeviceCoordinateCache)
        self.setZValue(-1)

    def addedge(self, edge):
        self.edges.append(edge)
        edge.adjust()
    
    @property
    def edges(self):
        return self.edges

    def calculateforces(self):
        if not self.scene() or self.scene().mouseGrabberItem() == self:
            self.newposition = self.pos()
            return
        xvel = 0.0
        yvel = 0.0
        items = self.scene().items()
        for item in items:
            if not isinstance(item, Node):
                continue
            vec = self.mapToItem(item, 0, 0)
            dx = vec.x()
            dy = vec.y()
            l = 2.0 * (dx * dx + dy * dy)
            if l > 0:
                xvel += (dx * 150.0) / 1
                yvel += (dy * 150.0) / 1
        weight = (len(self.edges) + 1) *10
        for edge in self.edges:
            vec = QPointF()
            if edge.source == self:
                vec = self.mapToItem(edge.destination, 0, 0)
            else:
                vec = self.mapToItem(edge.source, 0, 0)
            xvel -= vec.x() / weight
            yvel -= vec.y() / weight
        if abs(xvel) < 0.1 and abs(yvel) < 0.1:
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
        
        gradient = QRadialGradient(-3, -3, 10)
        if option.state & QStyle.StateFlag.State_Sunken:
            gradient.setCenter(3, 3)
            gradient.setFocalPoint(3, 3)
            gradient.setColorAt(1, QColor(Qt.GlobalColor.yellow).lighter(120))
            gradient.setColorAt(0, QColor(Qt.GlobalColor.darkYellow).lighter(120))
        else:
            gradient.setColorAt(0, Qt.GlobalColor.yellow)
            gradient.setColorAt(1, Qt.GlobalColor.darkYellow)
        painter.setBrush(gradient)
        painter.setPen(QPen(Qt.GlobalColor.black, 0))
        painter.drawEllipse(-10, -10, 20, 20)

    def itemChange(self, change, value):
        if change == QGraphicsItem.GraphicsItemChange.ItemPositionHasChanged:
            for edge in self.edges:
                edge.adjust()
            self.graph.itemMoved()
        return QGraphicsItem.itemChange(change, value)

    def mousePressEvent(self, event):
        self.update()
        super().mousePressEvent(event)

    def mouseReleaseEvent(self, event):
        self.update()
        super().mouseReleaseEvent(event)
