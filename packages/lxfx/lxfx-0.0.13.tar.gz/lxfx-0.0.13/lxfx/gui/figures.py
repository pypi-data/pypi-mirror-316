from PySide6.QtWidgets import (QGraphicsSceneDragDropEvent, QWidget, QVBoxLayout, QLabel, QSlider, QColorDialog, QMenu,
                               QGraphicsItem)
from PySide6.QtCore import Qt, QRectF, QPointF
from PySide6.QtGui import QPen, QBrush, QPainterPath, QPolygonF
from lxfx.gui.modelsWidget import ModelsWidget

supported_strategies = ["mean_reversion",
                        "momentum",
                        "breakout",
                        "arbitrage"]
supported_figures = ["line",
                     "horizontal_ray",
                     "rectangle",
                     "ellipse",
                     "trend_line",
                     "circle",
                     "ray",
                     "fibonacci",
                     "range_selector"]
supported_indicators = ["volume",
                        "moving_averages",
                        "sma",
                        "ema",
                        "rsi",
                        "macd",
                        "bbands",
                        "stoch"]
supported_tickers = {
    "currencies": ["EURUSD", "GBPUSD", "USDCHF", "USDJPY", "AUDUSD", "NZDUSD", "USDCAD"],
    "coins": ["BTCUSD", "ETHUSD"],
    "stocks": ["AAPL", "MSFT", "GOOGL", "AMZN", "TSLA", "FB", "BRK.A", "V", "JNJ", "WMT", "NASDAQ", "SP500"]
}

supported_timeframes = {
                    "1min": "1m",
                    "3min": "3m",
                    "5min": "5m", 
                    "15min": "15m",
                    "30min": "30m",
                    "1hour": "1h",
                    "4hour": "4h",
                    "1day": "1d",
                    "1week": "1w",
                    "1month": "1m",
                    "1year": "1y"}

class OpacityWidget(QWidget):
    def __init__(self, parent=None, current_opacity: float = 1):
        super().__init__(parent)
        self.current_opacity = current_opacity
        self.setFixedSize(250, 100)
        self.layout = QVBoxLayout()
        self.layout.setContentsMargins(10, 10, 10, 10)
        self.layout.setSpacing(5)
        self.setLayout(self.layout)

        # Add a slider for opacity control
        self.opacity_label = QLabel("Opacity", self)
        self.opacity_label.setAlignment(Qt.AlignCenter)
        self.layout.addWidget(self.opacity_label)

        self.opacity_slider = QSlider(Qt.Horizontal, self)
        self.opacity_slider.setRange(0, 100)  # Slider range from 0 to 100
        self.opacity_slider.setValue(self.current_opacity * 100)  # Default to current opacity
        self.opacity_slider.valueChanged.connect(self.change_opacity)
        self.layout.addWidget(self.opacity_slider)

    def change_opacity(self, value):
        # Convert slider value to opacity (0.0 to 1.0)
        opacity = value / 100.0
        # Assuming you have a reference to the selected figure
        if hasattr(self, 'selected_figure') and self.selected_figure:
            self.selected_figure.set_opacity(opacity)

class DrawableFigure(QGraphicsItem):
    def __init__(self, pen_color=Qt.black, pen_width=2, opacity=1.0, is_indicator=False):
        super().__init__()
        self.figure_name = None
        self.setFlags(QGraphicsItem.ItemIsSelectable | 
                      QGraphicsItem.ItemIsMovable)
        self.pen = QPen(pen_color, pen_width)
        self.brush = QBrush(Qt.NoBrush)
        self.set_opacity(opacity)
        self.opacity_widget = None  # Reference to the opacity widget
        self.is_indicator = is_indicator

    def set_pen(self, color, width):
        self.pen = QPen(color, width)
        self.update()

    def set_brush(self, color):
        self.brush = QBrush(color)
        self.update()

    def set_opacity(self, opacity):
        opacity = max(0, min(opacity, 1))
        self.setOpacity(opacity)
        pen_color = self.pen.color()
        pen_color.setAlphaF(opacity)
        self.pen.setColor(pen_color)
        brush_color = self.brush.color()
        brush_color.setAlphaF(opacity)
        self.brush.setColor(brush_color)
        self.update()

    def delete(self):
        if self.scene():
            self.scene().removeItem(self)

    def translate(self, dx, dy):
        self.moveBy(dx, dy)

    def change_color(self):
        color = QColorDialog.getColor()
        if color.isValid():
            self.set_pen(color, self.pen.width())
            self.set_brush(color)

    def contextMenuEvent(self, event):
        if self.isSelected():
            menu = QMenu()
            if self.figure_name == "range_selector":
                predict_action = menu.addAction("Predict")
                predict_action.triggered.connect(self.showModelsWidget)
            if not self.is_indicator:
                delete_action = menu.addAction("Delete")
            hide_action = menu.addAction("Hide")
            show_action = menu.addAction("Show")
            change_color_action = menu.addAction("Change Color")
            toggle_opacity_action = menu.addAction("Adjust Opacity")
            action = menu.exec_(event.screenPos())

            if action == delete_action:
                self.scene().removeItem(self)
            elif action == change_color_action:
                self.change_color()
            elif action == toggle_opacity_action:
                self.toggle_opacity_widget(event.screenPos())
            elif action == hide_action:
                self.setOpacity(0)
            elif action == show_action:
                self.setOpacity(1)

    def toggle_opacity_widget(self, pos):
        if self.opacity_widget is None:
            self.opacity_widget = OpacityWidget()
            self.opacity_widget.selected_figure = self  # Set the current figure
        if self.opacity_widget.isVisible():
            self.opacity_widget.hide()
        else:
            self.opacity_widget.move(pos)
            self.opacity_widget.show()

    def mouseDoubleClickEvent(self, event):
        if self.isSelected():
            pass
        else:
            self.setSelected(True)
        super().mouseDoubleClickEvent(event)

    def keyPressEvent(self, event):
        if event.key() == Qt.Key_Delete:
            self.delete()
        super().keyPressEvent(event)

    def paint(self, painter, option, widget):
        pass

    def boundingRect(self):
        pass

class DrawableLine(DrawableFigure):
    def __init__(self, start_point, end_point, pen_color=Qt.blue, pen_width=2):
        super().__init__(pen_color, pen_width)
        self.figure_name = "line"
        self.start_point = start_point
        self.end_point = end_point

        # self.boundingRect().setHeight(50)

    def paint(self, painter, option, widget):
        painter.setPen(self.pen)
        painter.drawLine(self.start_point, self.end_point)

    def boundingRect(self):
        return QRectF(self.start_point, self.end_point).normalized()

class DrawableRectangle(DrawableFigure):
    def __init__(self, rect, pen_color=Qt.blue, pen_width=2):
        self.figure_name = "rectangle"
        super().__init__(pen_color, pen_width)
        self.rect = rect

    def paint(self, painter, option, widget):
        painter.setPen(self.pen)
        painter.setBrush(self.brush)
        painter.drawRect(self.rect)

    def boundingRect(self):
        return self.rect.normalized()

class DrawableCircle(DrawableFigure):
    def __init__(self, center, radius, pen_color=Qt.blue, pen_width=2):
        super().__init__(pen_color, pen_width)
        self.figure_name = "circle"
        self.center = center
        self.radius = radius

    def paint(self, painter, option, widget):
        painter.setPen(self.pen)
        painter.setBrush(self.brush)
        rect = QRectF(self.center.x() - self.radius, self.center.y() - self.radius, self.radius * 2, self.radius * 2)
        painter.drawEllipse(rect)

    def boundingRect(self):
        return QRectF(self.center.x() - self.radius, self.center.y() - self.radius, self.radius * 2, self.radius * 2).normalized()

class DrawableEllipse(DrawableFigure):
    def __init__(self, rect, pen_color=Qt.blue, pen_width=2):
        super().__init__(pen_color, pen_width)
        self.figure_name = "ellipse"
        self.rect = rect

    def paint(self, painter, option, widget):
        painter.setPen(self.pen)
        painter.setBrush(self.brush)
        painter.drawEllipse(self.rect)

    def boundingRect(self):
        return self.rect.normalized()

class DrawableRay(DrawableFigure):
    def __init__(self, points, pen_color=Qt.blue, pen_width=2):
        super().__init__(pen_color, pen_width)
        self.figure_name = "ray"
        self.points = points

    def paint(self, painter, option, widget):
        painter.setPen(self.pen)
        path = QPainterPath(self.points[0])
        for point in self.points[1:]:
            path.lineTo(point)
        painter.drawPath(path)
        if len(self.points) > 1:
            self.draw_arrowhead(painter, self.points[-2], self.points[-1])

    def boundingRect(self):
        return QRectF(min(p.x() for p in self.points), min(p.y() for p in self.points),
                      max(p.x() for p in self.points) - min(p.x() for p in self.points),
                      max(p.y() for p in self.points) - min(p.y() for p in self.points)).normalized()

    def draw_arrowhead(self, painter, start_point, end_point):
        direction = end_point - start_point
        length = direction.manhattanLength()
        if length == 0:
            return

        direction /= length
        arrow_size = 10
        left_point = end_point - direction * arrow_size + QPointF(-direction.y(), direction.x()) * arrow_size / 2
        right_point = end_point - direction * arrow_size + QPointF(direction.y(), -direction.x()) * arrow_size / 2
        arrow_head = QPolygonF([end_point, left_point, right_point])
        painter.setBrush(self.pen.color())
        painter.drawPolygon(arrow_head)


class DrawableFibonacciRetracement(DrawableFigure):
    def __init__(self, start_point, end_point, pen_width=2):
        super().__init__(Qt.blue, pen_width)
        self.figure_name = "fibonacci"
        self.start_point = start_point
        self.end_point = end_point
        self.levels = [0.0, 0.236, 0.382, 0.5, 0.618, 0.786, 1.0]
        self.lines = []
        self.colors = [Qt.red, Qt.green, Qt.blue, Qt.yellow, Qt.magenta, Qt.cyan, Qt.gray]

    def calculate_levels(self):
        min_y = min(self.start_point.y(), self.end_point.y())
        max_y = max(self.start_point.y(), self.end_point.y())
        height = max_y - min_y
        return [min_y + level * height for level in self.levels]

    def paint(self, painter, option, widget):
        levels = self.calculate_levels()
        for i, level in enumerate(levels):
            painter.setPen(QPen(self.colors[i], self.pen.width()))
            painter.drawLine(self.start_point.x(), level, self.end_point.x(), level)
            # Draw the retracement level text
            painter.drawText(self.end_point.x() + 5, level, f"{self.levels[i]:.3f}")

    def boundingRect(self):
        return QRectF(self.start_point, self.end_point).normalized()

class DrawableRangeSelector(DrawableFigure):
    def __init__(self,
                 scene_height,
                 pen_color=Qt.blue,
                 pen_width=2,
                 start_point:QPointF = None, 
                 end_point:QPointF = None,
                 scene_top_left_y_pos:float = None,
                 node_width:float = None,
                 id = 0):
        super().__init__(pen_color, pen_width)
        self.figure_name = "range_selector"
        self.id = id
        self.node_width = node_width
        self.scene_height = scene_height
        self.start_point = start_point 
        self.end_point = end_point
        self.scene_top_left_y_pos = scene_top_left_y_pos
        self.width = end_point.x()-start_point.x()
        self.rect = QRectF(start_point.x(), self.scene_top_left_y_pos, self.get_width(), self.scene_height)
        self.setFlag(QGraphicsItem.ItemIsMovable, True)
        self.setOpacity(0.5)
        self.set_brush(Qt.red)

    def itemChange(self, change, value):
        if change == QGraphicsItem.ItemPositionChange:
            # Update the rectangle's position based on the new position
            new_pos = value.toPointF()
            self.rect.moveTo(new_pos.x(), self.scene_top_left_y_pos)
        return super().itemChange(change, value)

    def get_width(self):
        candles_in_range = self.width//self.node_width+1
        return candles_in_range*self.node_width

    def paint(self, painter, option, widget):
        painter.setPen(self.pen)
        painter.setBrush(self.brush)
        painter.drawRect(self.rect)

    def boundingRect(self):
        return self.rect.normalized()

    def get_selected_candle_ids(self):
        selected_candle_ids = []
        start_candle_id = self.rect.bottomLeft().x()//self.node_width if self.rect.bottomLeft().x()%self.node_width == 0 else ((self.rect.bottomLeft().x()//self.node_width)+1)
        num_selected_num_candles = int((self.rect.bottomRight().x() - self.rect.bottomLeft().x())//self.node_width)
        for node_id in range(num_selected_num_candles):
            selected_candle_ids.append(start_candle_id+node_id)
        return selected_candle_ids

    def get_selected_range(self):
        # Return the range of the graph selected by the rectangle
        # return self.rect.left(), self.rect.right()
        return self.rect.bottomLeft().x(), self.rect.bottomRight().x()

    def showModelsWidget(self):
        self.models_widget = ModelsWidget()
        self.models_widget.set_model_input_data(self.scene().get_node_data_dict(ids=self.get_selected_candle_ids()))
        self.models_widget.show_model_input_data()
        self.models_widget.show()

    def delete(self):
        if self.scene():
            self.scene().range_selectors.remove(self.scene().range_selectors[self.id])
            self.scene().removeItem(self)

    def export_selected_data(self):
        # Placeholder for exporting data logic
        left, right = self.get_selected_range()
        # Implement logic to export data within this range
        pass

    def dragMoveEvent(self, event: QGraphicsSceneDragDropEvent) -> None:
        return super().dragMoveEvent(event)
