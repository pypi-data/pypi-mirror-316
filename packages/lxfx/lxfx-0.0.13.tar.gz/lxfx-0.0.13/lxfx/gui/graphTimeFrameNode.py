from PySide6.QtCore import QPointF, QRectF
from PySide6.QtWidgets import QGraphicsItemGroup, QTextBrowser, QFrame, QGraphicsProxyWidget
from PySide6.QtGui import Qt, QPen

from lxfx.gui.candleStickState import GraphTimeFrameNodeState
from lxfx.gui.candleBody import CandleBody
from lxfx.gui.candleStickWick import CandleStickWick
from lxfx.gui.pathGraphPoint import PathGraphPoint

class GraphTimeFrameNode(QGraphicsItemGroup):
    def __init__(self, ohlc_data,
                 time_state,
                 id,
                 is_dynamic,
                 node_width,
                 pixels_per_pip,
                 is_first):
        super().__init__()
        
        self.ohlc_data = ohlc_data
        self.is_first = is_first
        self.node_time_state = time_state
        self.is_node_dynamic = is_dynamic
        self.node_id = id
        self.node_width = node_width
        self.pixels_per_pip = pixels_per_pip
        self.node_state = None
        self.is_state_initialized = False
        self.path_graph_point = None
        self.candle_stick_body = None
        self.candle_stick_wick = None
        self.bounding_rect = QRectF()
        
        # Initialize node
        self.set_scale()
        self.set_range()
        self.set_node_height()
        self.node_state = GraphTimeFrameNodeState()
        self.initialize_state()
        self.populate_internal_state()
        
        self.bounding_rect.setTopLeft(QPointF(0, 0))
        self.bounding_rect.setHeight(self.node_height)
        self.bounding_rect.setWidth(self.node_width)

    def get_graph_time_frame_node_state(self):
        return self.node_state
                
    def get_path_graph_point(self):
        return self.path_graph_point
        
    def boundingRect(self):
        return self.bounding_rect
        
    def paint(self, painter, option, widget=None):
        self.candle_stick_body.paint(painter, option, widget)
        self.candle_stick_wick.paint(painter, option, widget)
        painter.drawPoint(self.path_graph_point.toPoint())
        
    def set_graph_time_frame_node_state(self, state):
        self.node_state = state
        
    def set_is_state_initialized(self, state):
        self.is_state_initialized = state
        
    def update_node_geometry(self, current_price):
        if self.is_node_dynamic:
            pass
            
    def value_to_position(self, value):
        PIPS_MULTIPLIER = 10000
        pips_difference = int((self.ohlc_data[1] - value) * PIPS_MULTIPLIER + 0.5)
        pixel_difference = pips_difference * self.get_pixels_per_pip()
        y = pixel_difference + self.node_state.get_prev_candle_stick_wick_end_position().y()
        x = self.node_width / 2
        return QPointF(x, y)
        
    def set_scale(self):
        self.node_scale = 2
        
    def set_range(self):
        self.range = abs(self.ohlc_data[1] - self.ohlc_data[2])
        
    def get_pixels_per_pip(self):
        return self.pixels_per_pip
        
    def set_node_height(self):
        MAX_HEIGHT = 600
        range_pips = int((self.range * 10000) + 0.5)
        MIN_PIXELS_PER_PIP = 0.5
        pixels_per_pip = max(self.pixels_per_pip, MIN_PIXELS_PER_PIP)
        height = range_pips * pixels_per_pip
        height = min(height, MAX_HEIGHT)
        self.node_height = height
        
    def initialize_state(self):
        self.node_state.set_is_dynamic(self.is_node_dynamic)
        self.node_state.set_time_state(self.node_time_state)
        self.node_state.set_id(self.node_id)
        
        if not self.is_node_dynamic:
            self.node_state.set_low(self.ohlc_data[2])
            self.node_state.set_high(self.ohlc_data[1])
            self.node_state.set_close(self.ohlc_data[3])
            self.node_state.set_open(self.ohlc_data[0])
            self.set_range()
            
            if self.ohlc_data[3] > self.ohlc_data[0]:
                self.node_state.set_candle_stick_body_pen(QPen(Qt.green))
                self.node_state.set_candle_stick_body_color(Qt.green)
                self.node_state.set_candle_stick_wick_color(Qt.green)
            else:
                self.node_state.set_candle_stick_body_pen(QPen(Qt.red))
                self.node_state.set_candle_stick_body_color(Qt.red)
                self.node_state.set_candle_stick_wick_color(Qt.red)
                
            self.node_state.set_cur_candle_stick_body_width(self.node_width - 2)
            
            high_position = self.value_to_position(self.ohlc_data[1]).y()
            low_position = self.value_to_position(self.ohlc_data[2]).y()
            open_position = self.value_to_position(self.ohlc_data[0]).y()
            close_position = self.value_to_position(self.ohlc_data[3]).y()
            
            self.node_state.set_cur_candle_stick_wick_start_position(QPointF(self.node_width/2, high_position))
            self.node_state.set_prev_candle_stick_wick_start_position(QPointF(self.node_width/2, high_position))
            self.node_state.set_cur_candle_stick_wick_end_position(QPointF(self.node_width/2, low_position))
            self.node_state.set_prev_candle_stick_wick_end_position(QPointF(self.node_width/2, low_position))
            
            body_top = min(open_position, close_position)
            body_bottom = max(open_position, close_position)
            self.node_state.set_cur_candle_stick_body_top_position(QPointF(0, body_top))
            self.node_state.set_cur_candle_stick_body_bottom_position(QPointF(0, body_bottom))
            
            body_length = abs(body_top - body_bottom)
            self.node_state.set_cur_candle_stick_body_length(body_length)
            self.node_state.set_prev_candle_stick_body_length(body_length)
            self.node_state.set_cur_candle_stick_wick_length(abs(high_position - low_position))
            self.node_state.set_prev_candle_stick_wick_length(abs(high_position - low_position))
            
            self.node_state.set_cur_candle_stick_body_location(QPointF(self.node_width / 2, body_length / 2))
            
        else:
            open_value = self.ohlc_data[0]
            self.node_state.set_low(open_value)
            self.node_state.set_high(open_value)
            self.node_state.set_close(open_value)
            self.node_state.set_open(open_value)
            self.node_state.set_candle_stick_body_pen(QPen(Qt.transparent))
            self.node_state.set_candle_stick_body_color(Qt.transparent)
            self.node_state.set_candle_stick_wick_color(Qt.transparent)
            self.node_state.set_cur_candle_stick_body_width(self.node_width)
            
            center_x = QPointF(self.node_width / 2, 0)
            self.node_state.set_cur_candle_stick_wick_start_position(center_x)
            self.node_state.set_prev_candle_stick_wick_start_position(center_x)
            self.node_state.set_cur_candle_stick_wick_end_position(center_x)
            self.node_state.set_prev_candle_stick_wick_end_position(center_x)
            self.node_state.set_cur_candle_stick_body_top_position(center_x)
            self.node_state.set_cur_candle_stick_body_bottom_position(center_x)
            self.node_state.set_prev_candle_stick_body_top_position(center_x)
            self.node_state.set_prev_candle_stick_body_bottom_position(center_x)
            
            self.node_state.set_cur_candle_stick_body_length(0)
            self.node_state.set_prev_candle_stick_body_length(0)
            self.node_state.set_cur_candle_stick_wick_length(0)
            self.node_state.set_prev_candle_stick_wick_length(0)
            
        self.node_state.is_first = self.is_first
        self.set_is_state_initialized(True)
        
    def populate_internal_state(self):
        self.candle_stick_body = CandleBody(self, self.node_state)
        self.candle_stick_wick = CandleStickWick(self, self.node_state)
        self.path_graph_point = PathGraphPoint()
        self.addToGroup(self.candle_stick_body)
        self.addToGroup(self.candle_stick_wick)
        
    def set_position(self, x, y):
        pass
        
    def merge_node(self):
        candle_pos = self.candle_stick_body.pos()
        self.path_graph_point.setX(candle_pos.x())
        self.path_graph_point.setY(candle_pos.y())
        
    def hoverEnterEvent(self, event):
        scene = self.scene()
        if scene:
            scene_pos = self.mapToScene(event.pos())
            
            info_browser = QTextBrowser()
            info_browser.setReadOnly(True)
            info_browser.setText(f"""Open: {self.node_state.get_open()}
                                High: {self.node_state.get_high()}
                                Low: {self.node_state.get_low()}
                                Close: {self.node_state.get_close()}
                                Date: {self.node_state.get_candle_date_time().toString()}
                                XPosition: {self.pos().x()}
                                YPosition: {self.pos().y()}""")
            
            info_browser.setStyleSheet("background-color: white; color: black; font-size: 10pt;")
            info_browser.setFrameStyle(QFrame.Box | QFrame.Plain)
            info_browser.setLineWidth(1)
            
            proxy = QGraphicsProxyWidget()
            proxy.setWidget(info_browser)
            proxy.setZValue(1)
            proxy.setPos(scene_pos + QPointF(10, 10))
            
            scene.addItem(proxy)
            self.setData(0, proxy)
            
    def hoverLeaveEvent(self, event):
        scene = self.scene()
        if scene:
            info_group = self.data(0)
            if info_group:
                scene.removeItem(info_group)
                info_group.deleteLater()
                self.setData(0, None)
