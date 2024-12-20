from PySide6.QtCore import Qt
from PySide6.QtWidgets import QGraphicsRectItem
from PySide6.QtGui import QPen, QBrush

class CandleBody(QGraphicsRectItem):
    def __init__(self, parent=None, node_state=None):
        super().__init__(parent)
        self.node_state = node_state
        self.m_isHighlighted = False
        
        # Initialize the rectangle based on the node state
        self.setRect(0, 
                    self.node_state.get_cur_candle_stick_body_top_position().y(),
                    self.node_state.get_cur_candle_stick_body_width(),
                    self.node_state.get_cur_candle_stick_body_length())

    def paint(self, painter, option, widget):
        # Set the pen and brush for the candlestick body
        painter.setPen(QPen(self.node_state.get_candle_stick_body_color()))
        painter.setBrush(QBrush(self.node_state.get_candle_stick_body_color()))

        # Draw the candlestick body
        painter.drawRect(self.rect())

    def isHighlighted(self):
        return self.m_isHighlighted

    def setHighlighted(self, highlighted):
        if self.m_isHighlighted != highlighted:
            self.m_isHighlighted = highlighted
            if self.m_isHighlighted:
                self.setPen(QPen(Qt.GlobalColor.yellow, 2))
            else:
                self.setPen(QPen(Qt.GlobalColor.black, 1))
