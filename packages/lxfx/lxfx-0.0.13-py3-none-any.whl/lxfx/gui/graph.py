from PySide6.QtWidgets import (QGraphicsScene, QGraphicsSceneContextMenuEvent, QGraphicsSceneDragDropEvent, QMessageBox, QGraphicsPathItem,
                               QGraphicsLineItem, QGraphicsRectItem,
                               QGraphicsView, QGraphicsItemGroup,
                               QGraphicsEllipseItem,
                               QGraphicsPolygonItem,
                               QGraphicsItem, QColorDialog, QMenu,
                               QWidget, QVBoxLayout, QLabel, QSlider,
                               QFileDialog, QCheckBox, QLineEdit, QPushButton, QHBoxLayout,
                               QDialog
                               )
from PySide6.QtCore import QPointF, QRectF, Qt, QLineF
from PySide6.QtGui import QPen, QPainterPath, QBrush, QPolygonF, QAction
import logging
from lxfx.gui.graphTimeFrameNode import GraphTimeFrameNode
from lxfx.gui.tViewLine import TViewLine
from lxfx.gui.dbManager import DbManager
from lxfx.gui.figures import (DrawableRangeSelector, supported_figures,
                     supported_indicators,
                     DrawableCircle,
                     DrawableEllipse,
                     DrawableFibonacciRetracement,
                     DrawableLine,
                     DrawableRay,
                     DrawableRectangle)
from lxfx.gui.indicators import DrawableBollingerBands, DrawableMovingAverage, MovingAveragesDialog
from lxfx.gui.modelsWidget import ModelsWidget

class Graph(QGraphicsScene):
    def __init__(self, parent = None, 
                 pixels_per_pip: int = 1,
                 ticker_name: str = None,
                 db_manager:DbManager = None,
                 time_frame: str = None,
                 graphing_view:QGraphicsView = None):
        super().__init__(parent)
        self.PRICE_MULTIPLIER = 10000
        self.PIXELS_PER_PIP = pixels_per_pip
        self.SCENE_MAX_NODES = 5365
        self.SCENE_BATCH_NODES = 10
        self.DUMMY_SPACE_NODES = 50 # in terms of nodes
        self.moving_average_dialog = None 
        self.graphing_view = graphing_view
        self.rel_position = 0
        self.first_high = 0
        self.last_node_id = 0
        self.num_nodes = 0
        self.mouse_pos = QPointF()
        self.node_positions = None
        self.graph_nodes = []
        self.batch_nodes = []
        self.node_width = 10
        self.scene_width = 0
        self.scene_height = 0
        self.max_value = 0
        self.min_value = 0
        self.max_position = 0
        self.min_position = 0
        self.grid_items = []
        self.db_manager = db_manager
        self.ticker_name = ticker_name 
        self.time_frame = time_frame
        self.db_table_name = self.ticker_name + "_" + self.time_frame
        self.is_drawing = False
        self.first_point = None 
        self.second_point = None

        # Initialize graph
        self.min_value = self.db_manager.get_min_value("Low", self.db_table_name)
        self.max_value = self.db_manager.get_max_value("High", self.db_table_name)
        self.num_nodes = self.db_manager.get_n_nodes(self.db_table_name)
        self.compute_scene_rect_dimensions()
        self.draw_grid()

        self.supported_graph_modes = ["candles", "curve"]

        self.is_drawn = False

        self.replay_timer = None
        self.replay_speed = 1000  # Default speed in milliseconds
        self.replay_index = 0
        self.is_replaying = False
        self.replay_data = []
        self.current_candle = None
        self.target_timeframe = '1D'  # Example: target timeframe for replay
        self.grid_items = []

        self.is_showing_grid = True
        self.is_showing_candles = True
        self.is_showing_line_graph = True
        self.line_graph_path_item = None
        self.indicator_view_states = {}
        self.initialize_indicators()
        self.initialize_indicator_view_states()

        self.range_selectors = []

    def get_node_data_dict(self, ids:list):
        nodes = self.graph_nodes[int(ids[0]): int(ids[-1])+1]
        highs = []
        lows = []
        opens = []
        closes = []

        for node in nodes:
            highs.append(node.node_state.get_high())
            lows.append(node.node_state.get_low())
            opens.append(node.node_state.get_open())
            closes.append(node.node_state.get_close())

        data_dict = {
            "High": highs,
            "Low": lows,
            "Open": opens,
            "Close": closes
        }
        return data_dict

    @property
    def data_dict(self):
        return self.get_node_data_dict(ids = [node.id for node in self.graph_nodes])

    def contextMenuEvent(self, event: QGraphicsSceneContextMenuEvent) -> None:
        menu = QMenu()

        self.indicatorsMenu = QMenu("Indicators", menu)
        menu.addMenu(self.indicatorsMenu)
        # Use supported_indicators list to create actions
        self.indicator_actions = {}
        for indicator in supported_indicators:
            action = QAction(indicator.replace("_", " ").title(), self)
            action.triggered.connect(lambda checked, i= indicator:self.draw_indicator(i))
            if not indicator == "moving_averages":
                action.setCheckable(True) 
                action.setChecked(self.indicator_view_states[indicator])
            action.toggled.connect(lambda checked, i=indicator: self.toggle_indicator(i, checked))
            self.indicatorsMenu.addAction(action)
            self.indicator_actions[indicator] = action

        self.figuresMenu = QMenu("Figures", menu)
        # Use supported_figures list to create actions
        self.figure_actions = {}
        for figure in supported_figures:
            action = QAction(figure.replace("_", " ").title(), self)
            action.triggered.connect(lambda checked, f=figure: self.draw_figure(f))
            self.figuresMenu.addAction(action)
            self.figure_actions[figure] = action
        menu.addMenu(self.figuresMenu)
        menu.addSeparator()

        modelsAction = QAction("Models", menu)
        modelsAction.triggered.connect(self.showModelsWidget)
        menu.addAction(modelsAction)
        menu.addSeparator()

        # graph settings menu
        graph_settings_menu = QMenu("Settings", menu)
        menu.addMenu(graph_settings_menu)
        # graph settings menu actions
        if self.is_showing_grid:
            show_grid_action = graph_settings_menu.addAction("Hide Grid")
        else:
            show_grid_action = graph_settings_menu.addAction("Show Grid")
        if self.is_showing_candles:
            show_candles_action = graph_settings_menu.addAction("Hide Candles")
        else:
            show_candles_action = graph_settings_menu.addAction("Show Candles")
        if self.is_showing_line_graph:
            show_line_graph_action = graph_settings_menu.addAction("Hide Line Graph")
        else:
            show_line_graph_action = graph_settings_menu.addAction("Show Line Graph") 
        show_line_graph_action.triggered.connect(self.toggle_line_graph)
        show_grid_action.triggered.connect(self.toggle_grid)
        show_grid_action.setShortcut("Ctrl+G")
        show_candles_action.triggered.connect(self.toggle_candles)

        save_chart_action = menu.addAction("Save portion")
        save_chart_action.setShortcut("Ctrl+S")
        save_chart_action.triggered.connect(self.save_chart)
        exit_action = menu.addAction("Exit")
        exit_action.setShortcut("Ctrl+Q")
        exit_action.triggered.connect(self.close)
        menu.exec_(event.screenPos())
        super().contextMenuEvent(event)

    def initialize_indicator_view_states(self):
        for indicator in supported_indicators:
            self.indicator_view_states[indicator] = False

    def initialize_indicators(self):
        self.bbands = None 
        self.volume = None 
        self.sma = None 
        self.ema = None 
        self.rsi = None 
        self.macd = None 
        self.stoch = None 

    def draw_line(self):
        logging.debug("draw line has been called")
        t_view_line = TViewLine(self.mouse_pos)
        self.addItem(t_view_line)
        logging.debug(t_view_line.boundingRect())
        logging.debug(t_view_line.isVisible())
        self.update()

    def setup_connections(self):
        pass

    def compute_scene_rect_dimensions(self):
        self.max_position = self.max_value * self.PRICE_MULTIPLIER
        self.min_position = self.min_value * self.PRICE_MULTIPLIER
        self.scene_width = (self.num_nodes+self.DUMMY_SPACE_NODES) * self.node_width
        self.scene_height = self.max_position - self.min_position
        self.setSceneRect(QRectF(0, self.min_position, self.scene_width, self.scene_height))

    def hideLineGraph(self):
        if self.line_path:
            self.line_graph_path_item.hide()

    def showLineGraph(self):
        if self.line_path:
            self.line_graph_path_item.show()

    def hideCandles(self):
        for item in self.graph_nodes:
            item.hide()

    def showCandles(self):
        for item in self.graph_nodes:
            item.show()

    def toggle_line_graph(self):
        if self.is_showing_line_graph:
            self.is_showing_line_graph = False
            self.hideLineGraph()
        else:
            self.is_showing_line_graph = True
            self.showLineGraph()

    def toggle_candles(self):
        if self.is_showing_candles:
            self.is_showing_candles = False
            self.hideCandles()
        else:
            self.is_showing_candles = True
            self.showCandles()

    def toggle_grid(self):
        if self.is_showing_grid:
            self.is_showing_grid = False
            self.hideGrid()
        else:
            self.is_showing_grid = True
            self.showGrid()

    def toggle_indicator(self, indicator_name, checked):
        self.indicator_view_states[indicator_name] = checked
        if checked:
            self.draw_indicator(indicator_name)
        else:
            self.remove_indicator(indicator_name)

    def remove_indicator(self, indicator_name):
        if indicator_name == "volume":
            self.remove_volume_graph()
        elif indicator_name == "sma":
            self.remove_sma()
        elif indicator_name == "bbands":
            self.remove_bbands()
        elif indicator_name == "macd":
            self.remove_macd()
        elif indicator_name == "rsi":
            self.remove_rsi()
        elif indicator_name == "ema":
            self.remove_ema()

    def remove_bbands(self):
        if self.bbands:
            for item in self.bbands_items:
                self.removeItem(item)
            self.bbands = None
            self.bbands_items = []

    def hide_bbands(self):
        if self.bbands:
            for item in self.bbands_items:
                item.hide()

    def show_bbands(self):
        if self.bbands:
            for item in self.bbands_items:
                item.show()

    def showGrid(self):
        for item in self.grid_items:
            item.show()
        self.update()

    def hideGrid(self):
        for item in self.grid_items:
            item.hide()
        self.update()

    def draw_grid(self):
        grid_size = self.node_width  # Size of the grid squares
        pen = QPen(Qt.lightGray, 1, Qt.SolidLine)
        # Draw vertical lines
        for x in range(0, int(self.scene_width), grid_size):
            pen = QPen(Qt.gray)
            line_item = QGraphicsLineItem(QLineF(x, self.min_position, x, self.max_position))
            line_item.setPen(pen)
            self.addItem(line_item)
            self.grid_items.append(line_item)

        # Draw horizontal lines
        for y in range(int(self.min_position), int(self.max_position), grid_size):
            pen = QPen(Qt.gray)
            line_item = QGraphicsLineItem(QLineF(0, y, self.scene_width, y))
            line_item.setPen(pen)
            self.addItem(line_item)
            self.grid_items.append(line_item)
            
    def set_mouse_pos(self, pos: QPointF):
        self.mouse_pos = pos

    def draw_indicator(self, indicator_name):
        if indicator_name == "volume":
            self.draw_volume_graph(start_candle_id=0, end_candle_id=self.SCENE_MAX_NODES)
        elif indicator_name == "moving_averages":
            self.draw_moving_averages()
        elif indicator_name == "sma":
            self.draw_sma()
        elif indicator_name == "ema":
            self.draw_ema()
        elif indicator_name == "rsi":
            self.draw_rsi()
        elif indicator_name == "macd":
            self.draw_macd()
        elif indicator_name == "bbands":
            self.draw_bbands()
        elif indicator_name == "stoch":
            self.draw_stoch()
        else:
            print(f"Unsupported indicator: {indicator_name}")

    def draw_moving_averages(self):
        if self.moving_average_dialog is None:
            self.moving_average_dialog = MovingAveragesDialog()
            if self.moving_average_dialog.exec_():
                self.moving_average_dialog.apply_moving_averages(self)
        else:
            if self.moving_average_dialog.exec_():
                self.moving_average_dialog.apply_moving_averages(self)

    def draw_sma(self):
        # Implement the logic to draw Simple Moving Average (SMA)
        pass

    def draw_ema(self):
        # Implement the logic to draw Exponential Moving Average (EMA)
        pass

    def draw_rsi(self):
        # Implement the logic to draw Relative Strength Index (RSI)
        pass

    def draw_macd(self):
        # Implement the logic to draw Moving Average Convergence Divergence (MACD)
        pass

    def draw_bbands(self):
        data= []
        for node in self.graph_nodes:
            high_pos= node.pos()
            data.append(high_pos)
            # data.append(node.node_state.get_cur_candle_stick_wick_start_position().y())
        self.bbands = DrawableBollingerBands(data=data, 
                                             period=20, 
                                             num_std_dev=2, 
                                             pen_width=2)
        # self.bbands.setPos(0, self.min_position)
        # self.addItem(self.bbands)
        self.bbands_items = self.bbands.draw_bands()
        for item in self.bbands_items:
            self.addItem(item)

    def draw_stoch(self):
        pass

    def draw_figure(self, figure):
        self.initialize_drawing_states(figure=figure)
        self.initialize_temp_shapes()
        self.is_drawing = True
        if figure == "line":
            self.draw_trend_line()
        elif figure == "rectangle":
            self.draw_rectangle()
        elif figure == "ellipse":
            self.draw_ellipse()
        elif figure == "circle":
            self.draw_circle()
        elif figure == "ray":
            self.draw_ray()
        elif figure == "fibonacci":
            self.draw_fibonacci()
        elif figure == "self.range_selector":
            self.draw_range_selector()
        elif figure == "horizontal_ray":
            self.draw_horizontal_ray()

    def initialize_temp_shapes(self):
        self.temp_line = None 
        self.temp_circle = None 
        self.temp_rectangle = None 
        self.temp_circle = None 
        self.temp_ellipse = None
        self.temp_ray = None
        self.temp_fibonacci = None
        self.temp_range_selector = None

    def initialize_drawing_states(self, figure: str):
        self.is_drawing_line = (figure == "line")
        self.is_drawing_rectangle = (figure == "rectangle")
        self.is_drawing_circle = (figure == "circle")
        self.is_drawing_ellipse = (figure == "ellipse")
        self.is_drawing_ray = (figure == "ray")
        self.is_drawing_fibonacci = (figure == "fibonacci")
        self.is_drawing_range_selector = (figure == "range_selector")
        self.is_drawing_horizontal_ray = (figure == "horizontal_ray")

    def draw_trend_line(self):
        self.first_point = None
        self.is_drawing_line = True

    def draw_rectangle(self):
        self.first_point = None
        self.is_drawing_rectangle = True

    def draw_circle(self):
        self.first_point = None
        self.is_drawing_circle = True

    def draw_ellipse(self):
        self.first_point = None
        self.is_drawing_ellipse = True

    def draw_ray(self):
        self.ray_points = []
        self.first_point= None
        self.temp_ray = None
        self.is_drawing_ray = True

    def draw_fibonacci(self):
        self.first_point = None
        self.is_drawing_fibonacci = True
        self.temp_fibonacci = None  # Temporary Fibonacci retracement

    def draw_range_selector(self):
        self.first_point = None 
        self.is_drawing_range_selector = True 
        self.temp_range_selector = True

    def draw_horizontal_ray(self):
        self.first_point = None 
        self.is_drawing_horizontal_ray = True

    def close(self):
        self.graphing_view.close()
        self.parent().close()

    def save_chart(self):
        
        file_path, _ = QFileDialog.getSaveFileName(caption="Save Chart",
                                                   dir="",
                                                   filter="PNG Files (*.png);;JPEG Files (*.jpg);;All Files (*)")
        if file_path:
            pixmap = self.graphing_view.grab()
            pixmap.save(file_path)

    def load_replay_data(self, lower_timeframe: str):
        # Load data for the lower timeframe
        self.replay_data = self.db_manager.load_data_for_timeframe(self.db_table_name, lower_timeframe)
        self.replay_index = 0

    def start_replay(self, lower_timeframe: str, target_timeframe: str):
        self.target_timeframe = target_timeframe
        if not self.replay_data:
            self.load_replay_data(lower_timeframe)
        self.is_replaying = True
        self.replay_timer = self.startTimer(self.replay_speed)

    def stop_replay(self):
        self.is_replaying = False
        if self.replay_timer:
            self.killTimer(self.replay_timer)
            self.replay_timer = None

    def timerEvent(self, event):
        if self.is_replaying and self.replay_index < len(self.replay_data):
            self.update_candle(self.replay_data[self.replay_index])
            self.replay_index += 1
        else:
            self.stop_replay()

    def update_candle(self, lower_timeframe_data):
        # Aggregate data to form a candle for the target timeframe
        if self.current_candle is None:
            self.current_candle = self.create_new_candle(lower_timeframe_data)
            self.addItem(self.current_candle)
        else:
            self.update_existing_candle(lower_timeframe_data)

    def create_new_candle(self, lower_timeframe_data):
        # Create a new candle from the first data point
        open_price = lower_timeframe_data['open']
        high_price = lower_timeframe_data['high']
        low_price = lower_timeframe_data['low']
        close_price = lower_timeframe_data['close']
        return DrawableCandle(open_price, high_price, low_price, close_price)

    def update_existing_candle(self, lower_timeframe_data):
        # Update the high, low, and close prices of the current candle
        self.current_candle.high_price = max(self.current_candle.high_price, lower_timeframe_data['high'])
        self.current_candle.low_price = min(self.current_candle.low_price, lower_timeframe_data['low'])
        self.current_candle.close_price = lower_timeframe_data['close']
        self.current_candle.update()  # Redraw the candle with updated values

class DrawableCandle(QGraphicsItem):
    def __init__(self, open_price, high_price, low_price, close_price):
        super().__init__()
        self.open_price = open_price
        self.high_price = high_price
        self.low_price = low_price
        self.close_price = close_price

    def paint(self, painter, option, widget):
        # Draw the candle using the open, high, low, and close prices
        pass

    def boundingRect(self):
        # Return the bounding rectangle for the candle
        pass

class CandleStickDynamicGraph(Graph):
    def __init__(self, parent = None,
                 ticker_name: str = None,
                 db_manager = None,
                 time_frame: str = None,
                 pixels_per_pip = 1,
                 graphing_view:QGraphicsView = None):
        super().__init__(parent, pixels_per_pip, ticker_name, db_manager, time_frame, graphing_view)
        self.graph_mode = "candles"
        self.cur_selector_id = 0

    def mousePressEvent(self, event):
        if self.is_drawing:
            self.graphing_view.setCursor(Qt.CrossCursor)  # Set cursor to cross
            if event.button() == Qt.LeftButton:
                point = event.scenePos()
                if self.is_drawing_ray:
                    self.ray_points.append(point)
                    if len(self.ray_points) > 1:
                        self.update_ray()
                elif self.is_drawing_horizontal_ray:
                    self.add_horizontal_ray(point)
                    self.is_drawing_horizontal_ray = False
                if self.first_point is None:
                    self.first_point = point
                else:
                    second_point = point
                    # add figure
                    if self.is_drawing_line:
                        self.add_trend_line(self.first_point, second_point)
                        self.is_drawing_line = False
                    elif self.is_drawing_rectangle:
                        self.add_rectangle(self.first_point, second_point)
                        self.is_drawing_rectangle = False
                    elif self.is_drawing_circle:
                        self.add_circle(self.first_point, second_point)
                        self.is_drawing_circle = False
                    elif self.is_drawing_ellipse:
                        self.add_ellipse(self.first_point, second_point)
                        self.is_drawing_ellipse = False
                    elif self.is_drawing_fibonacci:
                        self.add_fibonacci_retracement(self.first_point, second_point)
                        self.is_drawing_fibonacci = False
                    elif self.is_drawing_range_selector:
                        self.add_range_selector(self.first_point, second_point)
                        self.is_drawing_range_selector = False
                    self.first_point = None
                    # remove temp_figure
                    if self.temp_line:
                        self.removeItem(self.temp_line)
                        self.temp_line = None
                    if self.temp_rectangle:
                        self.removeItem(self.temp_rectangle)
                        self.temp_rectangle = None
                    if self.temp_circle:
                        self.removeItem(self.temp_circle)
                        self.temp_circle = None
                    if self.temp_ellipse:
                        self.removeItem(self.temp_ellipse)
                        self.temp_ellipse = None
                    if self.temp_fibonacci:
                        self.removeItem(self.temp_fibonacci)
                        self.temp_fibonacci = None
                    if self.temp_range_selector:
                        self.removeItem(self.temp_range_selector)
                        self.temp_range_selector = None
            else:
                self.graphing_view.setCursor(Qt.ArrowCursor)  # Reset cursor to default if not drawing
        super().mousePressEvent(event)

    def mouseMoveEvent(self, event):
        if self.is_drawing:
            self.graphing_view.setCursor(Qt.CrossCursor)  # Set cursor to cross
            if self.first_point is not None or (self.is_drawing_ray and self.ray_points):
                second_point = event.scenePos()
                if self.is_drawing_line:
                    if self.temp_line:
                        self.removeItem(self.temp_line)
                    self.temp_line = self.create_temp_line(self.first_point, second_point)
                    self.addItem(self.temp_line)
                elif self.is_drawing_rectangle:
                    if self.temp_rectangle:
                        self.removeItem(self.temp_rectangle)
                    self.temp_rectangle = self.create_temp_rectangle(self.first_point, second_point)
                    self.addItem(self.temp_rectangle)
                elif self.is_drawing_circle:
                    if self.temp_circle:
                        self.removeItem(self.temp_circle)
                    self.temp_circle = self.create_temp_circle(self.first_point, second_point)
                    self.addItem(self.temp_circle)
                elif self.is_drawing_ellipse:
                    if self.temp_ellipse:
                        self.removeItem(self.temp_ellipse)
                    self.temp_ellipse = self.create_temp_ellipse(self.first_point, second_point)
                    self.addItem(self.temp_ellipse)
                elif self.is_drawing_ray:
                    if self.temp_ray:
                        self.removeItem(self.temp_ray)
                    self.temp_ray = self.create_temp_ray(self.ray_points[-1], second_point)
                    self.addItem(self.temp_ray)
                elif self.is_drawing_fibonacci:
                    if self.temp_fibonacci:
                        self.removeItem(self.temp_fibonacci)
                    self.temp_fibonacci = self.create_temp_fibonacci(self.first_point, second_point)
                    self.addItem(self.temp_fibonacci)
                elif self.is_drawing_range_selector:
                    if self.temp_range_selector:
                        self.removeItem(self.temp_range_selector)
                    self.temp_range_selector = self.create_temp_range_selector(self.first_point, second_point)
                    self.addItem(self.temp_range_selector)
        else:
            self.graphing_view.setCursor(Qt.ArrowCursor)  # Reset cursor to default if not drawing
        super().mouseMoveEvent(event)

    def keyPressEvent(self, event):
        if event.key() == Qt.Key_Escape:
            if self.is_drawing_ray:
                self.is_drawing_ray = False
                self.ray_points.clear()
                if self.temp_ray:
                    self.removeItem(self.temp_ray)
                    self.temp_ray = None
                self.graphing_view.setCursor(Qt.ArrowCursor)
                  # Reset cursor to default
            else:
                self.stop_drawing()
        super().keyPressEvent(event)

    def draw_graph(self):
        if self.load_nodes():
            self.populate_nodes()
            self.center_on_last_candle()
            self.is_drawn = True

    def transform_y_coordinate(self, y: float) -> float:
        qt_graph_min = self.max_position
        qt_graph_max = self.min_position
        n_graph_min = self.min_position
        n_graph_max = self.max_position

        qt_transform = qt_graph_min + (qt_graph_max - qt_graph_min) * ((y - n_graph_min) / (n_graph_max - n_graph_min))
        return qt_transform

    def set_node_position(self, node) -> QPointF:
        node_state = node.get_graph_time_frame_node_state()
        node_position = QPointF()

        # Calculate the y-coordinate based on the node's high value
        y_coordinate = self.transform_y_coordinate(node_state.get_high() * self.PRICE_MULTIPLIER)
        node_position.setY(y_coordinate)

        # Calculate the x-coordinate based on the node's ID
        node_position.setX(node_state.get_id() * self.node_width)

        return node_position

    def load_nodes(self, batch: bool = False, start_date: str = None, end_date: str = None):
        id_count = 1
        table_name = self.ticker_name+"_"+self.time_frame
        if table_name not in self.db_manager.get_available_tables():
            available_tables = self.db_manager.get_available_tables()
            available_tables = [table for table in available_tables if self.ticker_name in table]
            available_tables_str = "\n".join(available_tables)
            QMessageBox.critical(None, "Error", f"Table {table_name} not found.\nAvailable tables:\n{available_tables_str}")
            return None
        if not batch:
            nodes_data = self.db_manager.load_data(self.db_table_name,
                                                   start_candle_id=0,
                                                   end_candle_id=self.SCENE_MAX_NODES,
                                                   start_date = start_date,
                                                   end_date = end_date,
                                                   dynamic = True)
        else:
            nodes_data = self.db_manager.load_data(start_candle_id=self.last_node_id + 1,
                                                   end_candle_id=self.last_node_id + self.SCENE_BATCH_NODES,
                                                   table_name=self.db_table_name,
                                                   dynamic = True)

        nodes = []
        count = 0
        is_first = False
        follow_candle_state = None
        nodes_data.reverse()
        
        for node_data in nodes_data:
            is_first = count == 0
            node = GraphTimeFrameNode(node_data[0], node_data[1], id_count, False, 
                                    self.node_width, self.PIXELS_PER_PIP, is_first)
            nodes.append(node)
            id_count += 1
            count += 1

        if not batch:
            self.graph_nodes = nodes
        else:
            self.batch_nodes = nodes
        return True

    def draw_line_graph(self):
        self.line_path = QPainterPath()
        high_positions = []
        for node in self.graph_nodes:
            # Get the actual position including the node's position in the scene
            pos = node.pos()
            high_pos = node.node_state.get_cur_candle_stick_wick_start_position()
            scene_pos = pos
            # scene_pos = QPointF(pos.x() + high_pos.x(), pos.y() + high_pos.y())
            high_positions.append(scene_pos)
        
        # Create a QPainterPath to draw a smooth curve
        if high_positions:
            self.line_path.moveTo(high_positions[0])
            for i in range(1, len(high_positions) - 1):
                # Use quadratic Bezier curve for smoother transitions
                mid_point = (high_positions[i] + high_positions[i + 1]) / 2
                self.line_path.quadTo(high_positions[i], mid_point)
            self.line_path.lineTo(high_positions[-1])
        
        # Create a QGraphicsPathItem to add the path to the scene
        self.line_graph_path_item = QGraphicsPathItem(self.line_path)
        pen = QPen(Qt.blue)
        pen.setWidth(2)
        self.line_graph_path_item.setPen(pen)
        self.addItem(self.line_graph_path_item)

    def populate_nodes(self, batch: bool = False):
        nodes = self.batch_nodes if batch else self.graph_nodes
        for node in nodes:
            node.setPos(self.set_node_position(node))
            self.addItem(node)

    def create_temp_line(self, start_point, end_point):
        line = QLineF(start_point, end_point)
        line_item = QGraphicsLineItem(line)
        pen = QPen(Qt.red, 2, Qt.DashLine)
        line_item.setPen(pen)
        return line_item

    def create_temp_rectangle(self, start_point, end_point):
        rect = QRectF(start_point, end_point)
        rect_item = QGraphicsRectItem(rect)
        pen = QPen(Qt.red, 2, Qt.DashLine)
        rect_item.setPen(pen)
        return rect_item

    def create_temp_circle(self, start_point, end_point):
        radius = (end_point - start_point).manhattanLength() / 2
        center = (start_point + end_point) / 2
        rect = QRectF(center.x() - radius, center.y() - radius, radius * 2, radius * 2)
        circle_item = QGraphicsEllipseItem(rect)
        pen = QPen(Qt.red, 2, Qt.DashLine)
        circle_item.setPen(pen)
        return circle_item

    def create_temp_ellipse(self, start_point, end_point):
        rect = QRectF(start_point, end_point)
        ellipse_item = QGraphicsEllipseItem(rect)
        pen = QPen(Qt.red, 2, Qt.DashLine)
        ellipse_item.setPen(pen)
        return ellipse_item

    def create_temp_ray(self, start_point, end_point):
        line = QLineF(start_point, end_point)
        line_item = QGraphicsLineItem(line)
        pen = QPen(Qt.red, 2, Qt.DashLine)
        line_item.setPen(pen)
        return line_item

    def create_temp_fibonacci(self, start_point, end_point):
        # Create a temporary DrawableFibonacciRetracement for preview
        return DrawableFibonacciRetracement(start_point, end_point)

    def create_temp_range_selector(self, start_point: QPointF, end_point: QPointF):
        height = abs(self.scene_height)
        width = abs(start_point.x() - end_point.x())
        top_left_x = min(start_point.x(), end_point.x())
        rect = QRectF(top_left_x, self.sceneRect().top(), width, height)
        rect_item = QGraphicsRectItem(rect)
        pen = QPen(Qt.red, 2, Qt.DashLine)
        rect_item.setPen(pen)
        return rect_item

    def update_ray(self):
        if self.temp_ray:
            self.removeItem(self.temp_ray)
            self.temp_ray = None

        # Create a QPainterPath to draw the ray
        path = QPainterPath(self.ray_points[0])
        for point in self.ray_points[1:]:
            path.lineTo(point)

        # Create a QGraphicsPathItem to add the path to the scene
        path_item = QGraphicsPathItem(path)
        pen = QPen(Qt.blue, 2)
        path_item.setPen(pen)
        self.addItem(path_item)

        # Draw arrowhead on the last segment of the ray
        if len(self.ray_points) > 1:
            self.draw_arrowhead(self.ray_points[-2], self.ray_points[-1])

    def draw_arrowhead(self, start_point, end_point):
        # Calculate the direction vector
        direction = end_point - start_point
        length = direction.manhattanLength()
        if length == 0:
            return

        # Normalize the direction vector
        direction /= length

        # Define the size of the arrowhead
        arrow_size = 10

        # Calculate the points for the arrowhead
        left_point = end_point - direction * arrow_size + QPointF(-direction.y(), direction.x()) * arrow_size / 2
        right_point = end_point - direction * arrow_size + QPointF(direction.y(), -direction.x()) * arrow_size / 2

        # Create a polygon for the arrowhead
        arrow_head = QPolygonF([end_point, left_point, right_point])

        # Create a QGraphicsPolygonItem to add the arrowhead to the scene
        arrow_item = QGraphicsPolygonItem(arrow_head)
        arrow_item.setBrush(Qt.blue)
        self.addItem(arrow_item)

    def add_trend_line(self, start_point, end_point):
        line_item = DrawableLine(start_point, end_point)
        self.addItem(line_item)

    def add_horizontal_ray(self, start_point:QPointF):
        end_point_x = (len(self.graph_nodes)+self.DUMMY_SPACE_NODES)*self.node_width
        end_point_y = start_point.y()
        end_point = QPointF(end_point_x, end_point_y)
        self.add_trend_line(start_point, end_point)

    def add_rectangle(self, start_point, end_point):
        rect = QRectF(start_point, end_point)
        rect_item = DrawableRectangle(rect)
        self.addItem(rect_item)

    def add_circle(self, start_point, end_point):
        radius = (end_point - start_point).manhattanLength() / 2
        center = (start_point + end_point) / 2
        circle_item = DrawableCircle(center, radius)
        self.addItem(circle_item)

    def add_ellipse(self, start_point, end_point):
        rect = QRectF(start_point, end_point)
        ellipse_item = DrawableEllipse(rect)
        self.addItem(ellipse_item)

    def add_fibonacci_retracement(self, start_point, end_point):
        fibonacci_item = DrawableFibonacciRetracement(start_point, end_point)
        self.addItem(fibonacci_item)

    def add_range_selector(self, start_point, end_point):
        range_selector_item = DrawableRangeSelector(scene_height=self.scene_height,
                                                    start_point = start_point,
                                                    end_point = end_point,
                                                    scene_top_left_y_pos=self.sceneRect().topRight().y(),
                                                    node_width=self.node_width,
                                                    id = self.cur_selector_id)
        self.addItem(range_selector_item)
        self.range_selectors.append(range_selector_item)
        self.cur_selector_id += 1

    def showModelsWidget(self):
        self.models_widget = ModelsWidget()
        ids = self.range_selectors[0].get_selected_candle_ids()
        self.models_widget.set_model_input_data(self.get_node_data_dict(ids=ids))
        self.models_widget.show()

    def draw_volume_graph(self,start_candle_id = None, 
                          end_candle_id = None, 
                          start_date = None, 
                          end_date = None):
        self.volume_group = QGraphicsItemGroup()

        # Assuming you have a method to get volume data for each node
        volume_data = self.db_manager.get_volume_data(
            self.db_table_name,
            start_candle_id=start_candle_id,
            end_candle_id=end_candle_id,
            start_date=start_date,
            end_date=end_date,
        )

        if not volume_data:
            print("No volume data available.")
            return

        # Define the maximum height for the volume bars
        max_volume_height = 100  # Adjust as needed
        max_volume = max(volume_data) if volume_data else 1  # Avoid division by zero

        # Define a pen and brush for the volume bars
        pen = QPen(Qt.NoPen)
        brush = QBrush(Qt.red)  # You can choose any color

        for i, volume in enumerate(volume_data):
            # Calculate the height of the bar based on the volume
            bar_height = (volume / max_volume) * max_volume_height

            # Calculate the position of the bar
            x_position = i * self.node_width
            y_position = self.graphing_view.viewport().height() - bar_height  # Align to the bottom of the view
            # y_position = self.graphing_view.viewport().rect().bottomLeft().y()

            # Create and add the volume bar to the group
            volume_bar = QGraphicsRectItem(x_position, y_position, self.node_width, bar_height)
            volume_bar.setPen(pen)
            volume_bar.setBrush(brush)
            self.volume_group.addToGroup(volume_bar)
        self.volume_group.setPos(QPointF(0.0, self.graphing_view.viewport().rect().bottomLeft().y()))
        self.addItem(self.volume_group)

    # def dragMoveEvent(self, event: QGraphicsSceneDragDropEvent) -> None:
    #     return super().dragMoveEvent(event)

    def resizeEvent(self, event):
        self.update_volume_position()
        super().resizeEvent(event)

    def update_volume_position(self):
        # Update the position of the volume group to stay at the bottom of the view
        self.volume_group.setPos(self.mapToScene(0, self.graphing_view.viewport().height() - 100))  # Adjust height as needed
    
    def stop_drawing(self):
        # Reset all drawing states except for the ray
        self.is_drawing = False
        self.is_drawing_line = False
        self.is_drawing_rectangle = False
        self.is_drawing_circle = False
        self.is_drawing_ellipse = False
        self.is_drawing_fibonacci = False
        # self.is_drawing_ray = False  # Keep ray drawing state

        # Remove any temporary shapes from the scene except for the ray
        if self.temp_line:
            self.removeItem(self.temp_line)
            self.temp_line = None
        if self.temp_rectangle:
            self.removeItem(self.temp_rectangle)
            self.temp_rectangle = None
        if self.temp_circle:
            self.removeItem(self.temp_circle)
            self.temp_circle = None
        if self.temp_ellipse:
            self.removeItem(self.temp_ellipse)
            self.temp_ellipse = None
        # Do not remove temp_ray

        # Reset cursor to default
        self.graphing_view.setCursor(Qt.ArrowCursor)

    def center_on_last_candle(self):
        # Calculate the position of the last candle
        if self.graph_nodes:
            last_node = self.graph_nodes[-1]
            last_node_pos = last_node.pos()

            # Calculate the center position for the view
            view_center_x = last_node_pos.x() + self.node_width / 2
            view_center_y = last_node_pos.y()

            # Center the view on the last candle
            self.graphing_view.centerOn(view_center_x, view_center_y)
