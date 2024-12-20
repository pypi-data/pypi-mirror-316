from PySide6.QtWidgets import (QGraphicsView, QWidget, QGraphicsScene, 
                            QScrollBar, QVBoxLayout, QMenu, QGraphicsProxyWidget)
from PySide6.QtCore import Qt, QPoint, QPointF
from PySide6.QtGui import QPainter, QBrush, QWheelEvent, QMouseEvent
from lxfx.gui.leftClickWidget import LeftClickWidget

class GraphingView(QGraphicsView):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.panning = False
        self.vertical_scale_factor = 1
        self.horizontal_scale_factor = 1
        
        self.setRenderHint(QPainter.Antialiasing)
        self.setDragMode(QGraphicsView.ScrollHandDrag)
        self.setOptimizationFlags(QGraphicsView.DontSavePainterState)
        self.setViewportUpdateMode(QGraphicsView.SmartViewportUpdate)
        self.setTransformationAnchor(QGraphicsView.AnchorUnderMouse)
        self.setBackgroundBrush(QBrush(Qt.white))

    def set_horizontal_scale(self, value):
        scale_factor = value / 5000.0
        self.scale(scale_factor / self.horizontal_scale_factor, 1.0)
        self.horizontal_scale_factor = scale_factor

    def set_vertical_scale(self, value):
        scale_factor = value / 5000.0
        self.scale(1.0, scale_factor / self.vertical_scale_factor)
        self.vertical_scale_factor = scale_factor

    def wheelEvent(self, event: QWheelEvent):
        scale_factor = 1.15
        self.vertical_scale_factor = scale_factor
        self.horizontal_scale_factor = scale_factor
        if event.angleDelta().y() > 0:
            self.scale(scale_factor, scale_factor)
        else:
            self.scale(1.0 / scale_factor, 1.0 / scale_factor)

    def draw_figure(self, figure):
        # self.setMouseTracking(True)
        self.set_drawing_cursor()
        self.scene().draw_figure(figure)

    def set_drawing_cursor(self):
        self.setCursor(Qt.CrossCursor)

    def reset_cursor(self):
        self.setCursor(Qt.ArrowCursor)

    def mousePressEvent(self, event: QMouseEvent):
        if event.button() == Qt.LeftButton:
            self.panning = True
            self.last_mouse_pos = event.pos()
            # self.setCursor(Qt.ClosedHandCursor)
            self.set_drawing_cursor()
        # elif event.button() == Qt.RightButton:
        #     scene = self.scene()
        #     mouse_position = event.pos()
        #     scene_pos = self.mapToScene(mouse_position)
        #     left_click_widget = LeftClickWidget(self.scene(), self.graph)
        #     proxy = left_click_widget.getProxyWidget()
        #     proxy.setWidget(left_click_widget)
        #     proxy.setZValue(1)  # be on top
        #     self.graph.set_mouse_pos(scene_pos)
        #     proxy.setPos(scene_pos + QPointF(10, 10))
        #     scene.addItem(proxy)
        super().mousePressEvent(event)

    def mouseMoveEvent(self, event: QMouseEvent):
        if self.panning:
            self.horizontalScrollBar().setValue(
                self.horizontalScrollBar().value() - (event.x() - self.last_mouse_pos.x())
            )
            self.verticalScrollBar().setValue(
                self.verticalScrollBar().value() - (event.y() - self.last_mouse_pos.y())
            )
            self.last_mouse_pos = event.pos()
        super().mouseMoveEvent(event)

    def mouseReleaseEvent(self, event: QMouseEvent):
        if event.button() == Qt.LeftButton:
            self.panning = False
            self.setCursor(Qt.ArrowCursor)
        super().mouseReleaseEvent(event)
