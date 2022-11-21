from PyQt5.QtWidgets import QGraphicsView, QGraphicsScene
from PyQt5.QtGui import QPainter
#from node import Node


class Graphwidget(QGraphicsView):
    
    def __init__(self):
        self.timerId = 0
        self.centernode = None
        super().__init__()
        self.scene = QGraphicsScene(self)
        self.scene.setItemIndexMethod(QGraphicsScene.NoIndex)
        self.scene.setSceneRect(-200, -200, 400, 400)
        self.setScene(self.scene)
        self.setCacheMode(QGraphicsView.CacheModeFlag.CacheBackground)
        self.setViewportUpdateMode(QGraphicsView.ViewportUpdateMode.BoundingRectViewportUpdate)
        self.setRenderHint(QPainter.RenderHint.Antialiasing)
        self.setTransformationAnchor(QGraphicsView.ViewportAnchor.AnchorUnderMouse)
        self.scale(0.8, 0.8)
        self.setMinimumSize(400, 400)
        self.setWindowTitle("Tree")
        
        