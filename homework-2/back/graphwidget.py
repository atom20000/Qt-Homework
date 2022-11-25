from PyQt5.QtWidgets import QGraphicsView, QGraphicsScene
from PyQt5.QtGui import QPainter, QLinearGradient
from PyQt5.QtCore import QRectF, QPointF, QRandomGenerator, Qt
from .node import Node
from .edge import Edge


class Graphwidget(QGraphicsView):
    
    def __init__(self, data = None):
        super().__init__()
        self.timerId = 0
        self.centernode = None
        self.scene_ = QGraphicsScene(self)
        self.scene_.setItemIndexMethod(QGraphicsScene.NoIndex)
        self.scene_.setSceneRect(-640, -480, 1280, 720)
        self.setScene(self.scene_)
        self.setCacheMode(QGraphicsView.CacheModeFlag.CacheBackground)
        self.setViewportUpdateMode(QGraphicsView.ViewportUpdateMode.BoundingRectViewportUpdate)
        self.setRenderHint(QPainter.RenderHint.Antialiasing)
        self.setTransformationAnchor(QGraphicsView.ViewportAnchor.AnchorUnderMouse)
        self.scale(0.8, 0.8)
        self.setMinimumSize(400, 400)
        self.setWindowTitle("Tree")
        
        #self.node1 = Node(self)
        #self.node2 = Node(self)
        #self.node3 = Node(self)
        #self.node4 = Node(self)
        #self.centernode = Node(self)
        #self.node6 = Node(self)
        #self.node7 = Node(self)
        #self.node8 = Node(self)
        #self.node9 = Node(self)
        #self.scene_.addItem(self.node1)
        #self.scene_.addItem(self.node2)
        #self.scene_.addItem(self.node3)
        #self.scene_.addItem(self.node4)
        #self.scene_.addItem(self.centernode)
        #self.scene_.addItem(self.node6)
        #self.scene_.addItem(self.node7)
        #self.scene_.addItem(self.node8)
        #self.scene_.addItem(self.node9)
        #self.scene_.addItem(Edge(self.node1, self.node2))
        #self.scene_.addItem(Edge(self.node2, self.node3))
        #self.scene_.addItem(Edge(self.node2, self.centernode))
        #self.scene_.addItem(Edge(self.node3, self.node6))
        #self.scene_.addItem(Edge(self.node4, self.node1))
        #self.scene_.addItem(Edge(self.node4, self.centernode))
        #self.scene_.addItem(Edge(self.centernode, self.node6))
        #self.scene_.addItem(Edge(self.centernode, self.node8))
        #self.scene_.addItem(Edge(self.node6, self.node9))
        #self.scene_.addItem(Edge(self.node7, self.node4))
        #self.scene_.addItem(Edge(self.node8, self.node7))
        #self.scene_.addItem(Edge(self.node9, self.node8))
        #
        #self.node1.setPos(-50, -50)
        #self.node2.setPos(0, -50)
        #self.node3.setPos(50, -50)
        #self.node4.setPos(-50, 0)
        #self.centernode.setPos(0, 0)
        #self.node6.setPos(50, 0)
        #self.node7.setPos(-50, 50)
        #self.node8.setPos(0, 50)
        #self.node9.setPos(50, 50)
        self.centernode = Node(self)
        self.centernode.setPos(0, -(self.scene_.height()/2 - 70))
        #self.centernode.setPos(self.scene_.width()/4, self.scene_.height()/4)
        self.retree(data, self.centernode, self.depth(data))

    def retree(self, root: dict, parent: Node, count):
        if root:
            parent.value = root.get('value')
            self.scene_.addItem(parent)
            #parent.setPos(0, 0)
            if root.get('left'):
                left = Node(self)
                self.scene_.addItem(Edge(parent, left))
                #left.setPos(parent.mapToScene(0, 0) + QPointF(5*5, -8.66*5))
                left.setPos(parent.mapToScene(0, 0) + QPointF(-4.33*10*count, 2.5*10*count))
                self.retree(root.get('left'), left, count-1)
            
            if root.get('right'):
                right = Node(self)
                right.setPos(parent.mapToScene(0, 0) + QPointF(4.33*10*count, 2.5*10*count))
                #right.setPos(parent.mapToScene(0, 0) + QPointF(2.5*10, 4.33*10))
                self.scene_.addItem(Edge(parent, right))
                self.retree(root.get('right'), right, count-1)

    def depth(self, d):
        if isinstance(d, dict):
            return 1 + (max(map(self.depth, d.values())) if d else 0)
        return 0

    def itemmoved(self):
        #return
        if not self.timerId:
            self.timerId = self.startTimer(1000 / 500)
    
    def keyPressEvent(self, event) -> None:
        if (event := event.key()) and (event == Qt.Key.Key_Up):
            self.centernode.moveBy(0, -20)
        elif event == Qt.Key.Key_Down:
            self.centernode.moveBy(0, 20)
        elif event == Qt.Key.Key_Left:
            self.centernode.moveBy(-20, 0)
        elif event == Qt.Key.Key_Right:
            self.centernode.moveBy(20, 0)
        elif event == Qt.Key.Key_Plus:
            self.zoomIn()
        elif event == Qt.Key.Key_Minus:
            self.zoomOut()
        elif event in [Qt.Key.Key_Space, Qt.Key.Key_Enter]:
            self.shuffle()
        else:
            QGraphicsView.keyPressEvent(event)
        
    def timerEvent(self, a0) -> None:
        nodes = []
        items = self.scene().items()
        for item in items:
            if isinstance(item, Node):
                nodes.append(item)
        #[item for item in self.scene().items() if isinstance(item, Node)]
        for node in nodes:
            node.calculateforces()
        
        if not any([node.advanceposition() for node in nodes]):
            self.killTimer(self.timerId)
            self.timerId = 0
    
    def wheelEvent(self, event) -> None:
        self.scaleview(2**(-event.angleDelta().y() / 240.0))

    def drawBackground(self, painter, rect) -> None:
        sceneRect = self.sceneRect()
        rightshadow = QRectF(sceneRect.right(), sceneRect.top() + 5, 5, sceneRect.height())
        bottomshadow = QRectF(sceneRect.left() + 5, sceneRect.bottom(),sceneRect.width(), 5)
        if rightshadow.intersects(rect) or rightshadow.intersects(rect):
            painter.fillRect(rightshadow, Qt.GlobalColor.darkGray)
        if bottomshadow.intersected(rect) or bottomshadow.intersected(rect):
            painter.fillRect(bottomshadow, Qt.GlobalColor.darkGray)

        gradient = QLinearGradient(sceneRect.topLeft(), sceneRect.bottomRight())
        gradient.setColorAt(0, Qt.GlobalColor.white)
        gradient.setColorAt(1, Qt.GlobalColor.lightGray)
        painter.fillRect(rect.intersected(sceneRect), gradient)
        painter.setBrush(Qt.BrushStyle.NoBrush)
        painter.drawRect(sceneRect)

        #textrect = QRectF(sceneRect.left() + 4, sceneRect.top() + 4,
        #                    sceneRect.width() - 4, sceneRect.height() - 4)
        #message = "Click and drag the nodes around and zoom with the mouse wheel or the '+' and '-' keys"

        #font = painter.font()
        #font.setBold(True)
        #font.setPointSize(14)
        #painter.setFont(font)
        #painter.setPen(Qt.GlobalColor.lightGray)
        #painter.drawText(textrect.translated(2, 2), message)
        #painter.setPen(Qt.GlobalColor.black)
        #painter.drawText(textrect, message)
        

    def scaleview(self, scaleFactor):
        factor = self.transform().scale(scaleFactor, scaleFactor).mapRect(QRectF(0, 0, 1, 1)).width()
        if factor < 0.07 or factor > 100:
            return
        self.scale(scaleFactor, scaleFactor)

    def shuffle(self):
        for item in self.scene().items():
            if isinstance(item, Node):
                item.setPos(-150 + QRandomGenerator.global_().bounded(300), -150 + QRandomGenerator.global_().bounded(300))
    
    def zoomIn(self):
        self.scaleview(1.2)
    
    def zoomOut(self):
        self.scaleview(1 / 1.2)