from PySide6.QtCore import Qt, QPointF, QEvent, QLineF
from PySide6.QtWidgets import QGraphicsItem, QGraphicsLineItem
from PySide6.QtGui import QPainter, QPen, QBrush

class TViewLine(QGraphicsLineItem):
    def __init__(self, point1: QPointF):
        super().__init__()
        self.point1 = point1
        self.isdrawing = True
        
        self.setFlag(QGraphicsItem.ItemIsSelectable)
        self.setFlag(QGraphicsItem.ItemIsMovable) 
        self.setFlag(QGraphicsItem.ItemIsFocusable)
        self.setAcceptHoverEvents(True)
        self.setAcceptedMouseButtons(Qt.RightButton | Qt.LeftButton)
        self.setX(point1.x())
        self.setY(point1.y())
        self.setPen(QPen(Qt.black, 2))
        self.setLine(QLineF(point1, point1 + QPointF(20, 20)))
        self.setVisible(True)
        self.setZValue(1)

    def sceneEventFilter(self, watched: QGraphicsItem, event: QEvent) -> bool:
        print("Event Filter called!")
        return super().sceneEventFilter(watched, event)

    def mousePressEvent(self, event):
        print("mouse press event recorded")
        if event.button() == Qt.LeftButton:
            self.isdrawing = False
        super().mousePressEvent(event)

    def mouseMoveEvent(self, event):
        if self.isdrawing:
            print("following mouse")
            cur_mouse_position = event.scenePos()
            self.setLine(QLineF(self.point1, cur_mouse_position))
            super().mouseMoveEvent(event)
