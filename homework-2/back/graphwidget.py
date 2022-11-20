from PyQt5.QtWidgets import QGraphicsView, QGraphicsScene



class Graphwidget(QGraphicsView):
    
    def __init__(self):
        self.timerId = 0
        self.centernode = None
        self.scene = QGraphicsScene(self)
        self.scene.setItemIndexMethod(QGraphicsScene.NoIndex)
        self.scene.setSceneRect(-200, -200, 400, 400)
        