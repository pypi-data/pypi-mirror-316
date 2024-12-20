# candleStickState.h

from PySide6.QtCore import QPoint, QPointF, QDateTime
from PySide6.QtGui import QColor, QPen

class GraphTimeFrameNodeState:
    def __init__(self):
        # Private attributes
        self._is_dynamic = False
        self._time_state = QDateTime()
        self._high = 0.0
        self._low = 0.0
        self._open = 0.0
        self._close = 0.0
        self._id = 0  # Position number in the graph
        
        # Colors
        self._candle_stick_body_color = QColor()
        self._candle_stick_body_pen = QPen()
        self._candle_stick_wick_color = QColor()
        
        # Geometry
        self._prev_candle_stick_wick_length = 0
        self._prev_candle_stick_body_length = 0
        self._cur_candle_stick_wick_length = 0
        self._cur_candle_stick_body_length = 0
        self._cur_candle_stick_body_width = 0
        
        # Location
        self._prev_candle_stick_body_location = QPoint()
        self._cur_candle_stick_body_location = QPoint()
        
        self._prev_candle_stick_wick_start_position = QPointF()
        self._prev_candle_stick_wick_end_position = QPointF()
        self._cur_candle_stick_wick_end_position = QPointF()
        self._cur_candle_stick_wick_start_position = QPointF()
        
        # Private positions
        self._cur_candle_stick_body_top_position = QPointF()
        self._cur_candle_stick_body_bottom_position = QPointF()
        self._prev_candle_stick_body_top_position = QPointF()
        self._prev_candle_stick_body_bottom_position = QPointF()
        
        self.is_first = False

    # Body position getters/setters
    def get_cur_candle_stick_body_top_position(self):
        return self._cur_candle_stick_body_top_position
        
    def get_cur_candle_stick_body_bottom_position(self):
        return self._cur_candle_stick_body_bottom_position
        
    def get_prev_candle_stick_body_top_position(self):
        return self._prev_candle_stick_body_top_position
        
    def get_prev_candle_stick_body_bottom_position(self):
        return self._prev_candle_stick_body_bottom_position
        
    def set_cur_candle_stick_body_top_position(self, position):
        self._cur_candle_stick_body_top_position = position
        
    def set_cur_candle_stick_body_bottom_position(self, position):
        self._cur_candle_stick_body_bottom_position = position
        
    def set_prev_candle_stick_body_top_position(self, position):
        self._prev_candle_stick_body_top_position = position
        
    def set_prev_candle_stick_body_bottom_position(self, position):
        self._prev_candle_stick_body_bottom_position = position

    # Main getters
    def get_high(self):
        return self._high
        
    def get_low(self):
        return self._low
        
    def get_open(self):
        return self._open
        
    def get_close(self):
        return self._close
        
    def get_time_state(self):
        return QDateTime()
        
    def get_id(self):
        return self._id
        
    def get_candle_stick_wick_color(self):
        return self._candle_stick_wick_color
        
    def get_candle_stick_body_color(self):
        return self._candle_stick_body_color
        
    def get_candle_stick_body_pen(self):
        return self._candle_stick_body_pen
        
    def get_prev_candle_stick_body_location(self):
        return self._prev_candle_stick_body_location
        
    def get_cur_candle_stick_body_location(self):
        return self._cur_candle_stick_body_location
        
    def get_prev_candle_stick_wick_start_position(self):
        return self._prev_candle_stick_wick_start_position
        
    def get_cur_candle_stick_wick_start_position(self):
        return self._cur_candle_stick_wick_start_position
        
    def get_cur_candle_stick_wick_end_position(self):
        return self._cur_candle_stick_wick_end_position
        
    def get_prev_candle_stick_wick_end_position(self):
        return self._prev_candle_stick_wick_end_position
        
    def get_prev_candle_stick_length(self):
        return self._prev_candle_stick_wick_length
        
    def get_cur_candle_stick_wick_length(self):
        return self._cur_candle_stick_wick_length
        
    def get_prev_candle_stick_wick_length(self):
        return self._prev_candle_stick_wick_length
        
    def get_prev_candle_stick_body_length(self):
        return self._prev_candle_stick_body_length
        
    def get_cur_candle_stick_body_width(self):
        return self._cur_candle_stick_body_width
        
    def get_cur_candle_stick_body_length(self):
        return self._cur_candle_stick_body_length

    # Main setters
    def set_id(self, id):
        self._id = id
        
    def set_time_state(self, time_state):
        self._time_state = time_state
        
    def set_is_dynamic(self, is_dynamic):
        self._is_dynamic = is_dynamic
        
    def set_high(self, value):
        self._high = value
        
    def set_low(self, value):
        self._low = value
        
    def set_open(self, value):
        self._open = value
        
    def set_close(self, value):
        self._close = value
        
    def set_candle_stick_wick_color(self, color):
        self._candle_stick_wick_color = color
        
    def set_candle_stick_body_color(self, color):
        self._candle_stick_body_color = color
        
    def set_candle_stick_body_pen(self, pen):
        self._candle_stick_body_pen = pen
        
    def set_cur_candle_stick_wick_length(self, length):
        self._cur_candle_stick_wick_length = length
        
    def set_prev_candle_stick_wick_length(self, length):
        self._prev_candle_stick_wick_length = length
        
    def set_cur_candle_stick_body_length(self, length):
        self._cur_candle_stick_body_length = length
        
    def set_prev_candle_stick_body_location(self, location):
        self._prev_candle_stick_body_location = location
        
    def set_cur_candle_stick_body_location(self, location):
        self._cur_candle_stick_body_location = location
        
    def set_prev_candle_stick_wick_start_position(self, position):
        self._prev_candle_stick_wick_start_position = position
        
    def set_cur_candle_stick_wick_start_position(self, position):
        self._cur_candle_stick_wick_start_position = position
        
    def set_cur_candle_stick_wick_end_position(self, position):
        self._cur_candle_stick_wick_end_position = position
        
    def set_prev_candle_stick_wick_end_position(self, position):
        self._prev_candle_stick_wick_end_position = position
        
    def set_prev_candle_stick_body_length(self, length):
        self._prev_candle_stick_body_length = length
        
    def set_cur_candle_stick_body_width(self, width):
        self._cur_candle_stick_body_width = width

    # Additional methods
    def get_ohlc_data(self):
        return [self._open, self._high, self._low, self._close]
        
    def get_candle_date_time(self):
        return self._time_state
        
    def is_bull(self):
        return self.get_high() > self.get_open()
