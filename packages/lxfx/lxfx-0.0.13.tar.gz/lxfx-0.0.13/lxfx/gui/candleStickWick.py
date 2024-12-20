from PySide6.QtCore import QLineF
from PySide6.QtGui import QPen
from PySide6.QtCore import QPointF
from PySide6.QtWidgets import QGraphicsLineItem

class CandleStickWick(QGraphicsLineItem):
    def __init__(self, parent=None, node_state=None):
        super().__init__(parent)
        self.node_state = node_state
        # Initialize the line based on the initial state
        self.setLength(self.node_state.get_cur_candle_stick_wick_length())

    def paint(self, painter, option, widget):
        # Set the pen for the candlestick wick
        # Set the position of the wick line
        wick_line = QLineF(self.node_state.get_cur_candle_stick_wick_start_position(), 
                          self.node_state.get_cur_candle_stick_wick_end_position())
        self.setLine(wick_line)
        painter.setPen(QPen(self.node_state.get_candle_stick_wick_color()))

        # Draw the candlestick wick
        painter.drawLine(self.line())

    def setLength(self, new_length):
        # Only update if the new length is greater than the current length
        if new_length > self.node_state.get_cur_candle_stick_wick_length():
            current_line = self.line()
            body_center = QPointF(current_line.x1(), self.node_state.get_open())
                
            # Determine direction based on whether it's the upper or lower wick
            is_upper_wick = self.node_state.get_close() > self.node_state.get_open()
            
            # Calculate new start and end points
            if is_upper_wick:
                start_point = body_center
                end_point = body_center + QPointF(0, -new_length)
            else:
                start_point = body_center
                end_point = body_center + QPointF(0, new_length)
            
            # Update the line
            self.setLine(QLineF(start_point, end_point))
            
            # Update the length in the node state
            self.node_state.set_cur_candle_stick_wick_length(new_length)
            
            self.update()  # Trigger a redraw of the item