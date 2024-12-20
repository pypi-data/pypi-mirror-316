from PySide6.QtWidgets import (QMainWindow, QVBoxLayout, QWidget, QSplitter, 
                            QMenuBar, QMenu, QMessageBox, QDockWidget,
                            QComboBox, QDateEdit, QPushButton, QLabel, QDialog, QCheckBox, QSizePolicy)
from PySide6.QtGui import QAction
from PySide6.QtCore import Qt, Signal

from lxfx.gui.graphWindow import GraphWindow
from lxfx.gui.charting import LineChart, CandleStickChart, ScatterChart, BarChart, ChartWindow
from lxfx.gui.graphWindow import GraphWindow
from lxfx.gui.figures import supported_indicators, supported_figures, supported_strategies
from lxfx.gui.data import TickerDataViewer

class TickerInstance(QMainWindow):
    close_ticker_signal = Signal(int)
    timeframe_map = {
                    "1min": "1M",
                    "3min": "3M",
                    "5min": "5M", 
                    "15min": "15M",
                    "30min": "30M",
                    "1hour": "H1",
                    "4hour": "4H",
                    "1day": "D1",
                    "1week": "W1",
                    "1month": "M1",
                    "1year": "Y1"}

    def __init__(self, parent=None, instance_name=None, 
                 ticker_name=None, 
                 time_frame=None,
                 db_manager=None, 
                 ticker_index=None):
        super().__init__(parent)
        self.ticker_index = ticker_index
        self.instance_name = instance_name
        self.ticker_name = ticker_name 
        self.time_frame = time_frame
        self.db_manager = db_manager
        self.default_time_frame = "D1"

        # Initialize UI elements
        self.graph_window = None
        self.main_layout = None
        self.central_widget = None
        self.main_splitter = None
        self.upper_splitter = None
        self.lower_splitter = None
        self.menu_bar = None
        
        # Splitter states
        self.splitter_states = {}  # if 0 then free, if 1 then busy (index, state)
        self.initialize_splitter_states()
        #Docker states
        self.dock_states = {}
        self.initialize_dock_states()

        # Setup UI
        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)
        self.main_layout = QVBoxLayout()
        self.central_widget.setLayout(self.main_layout)
        self.setup_window_menu()
        self.setup_splitters()

        self.charts = {}
        self.dynamic_chart = None

        # self.initialize_data_viewer()

    # def initialize_data_viewer(self):
    #     self.data_viewer = TickerDataViewer(ticker_name = self.ticker_name, 
    #                                         charts = self.charts,
    #                                         parent=self)

    def initialize_splitter_states(self):
        self.splitter_states = {
            0: 0,
            1: 0,
            2: 0,
            3: 0
        }

    def initialize_dock_states(self):
        self.dock_states = {
            0: 0,
            1: 0,
            2: 0,
            3: 0
        }

    def setup_docks(self):
        self.left_dock = QDockWidget("Left Dock")
        self.right_dock = QDockWidget("Right Dock")
        self.bottom_dock = QDockWidget("Bottom Dock")
        
        self.addDockWidget(Qt.LeftDockWidgetArea, self.left_dock)
        self.addDockWidget(Qt.RightDockWidgetArea, self.right_dock)
        self.addDockWidget(Qt.BottomDockWidgetArea, self.bottom_dock)

        self.left_dock.setVisible(False)
        self.right_dock.setVisible(False)
        self.bottom_dock.setVisible(False)

    def setup_splitters(self):
        # Setup main splitter
        self.main_splitter = QSplitter()
        self.main_splitter.setOrientation(Qt.Vertical)
        self.main_layout.addWidget(self.main_splitter)

        # Setup initial graph window
        # self.graph_window = GraphWindow(self, self.pair_name, self.default_time_frame, self.db_manager)
        self.upper_splitter = QSplitter()
        self.upper_splitter.setOrientation(Qt.Horizontal)
        self.main_splitter.addWidget(self.upper_splitter)
        # self.upper_splitter.addWidget(self.graph_window)
        # self.splitter_states[0] = 1

        # Setup lower splitter
        self.lower_splitter = QSplitter()
        self.lower_splitter.setOrientation(Qt.Horizontal)
        self.main_splitter.addWidget(self.lower_splitter)

    def add_timeframe_as_tab(self, time_frame):
        pass

    def add_currency(self):
        pass

    def close_ticker(self):
        self.close_ticker_signal.emit(self.ticker_index)

    def setup_window_menu(self):
        self.menu_bar = QMenuBar(self)
        ticker_menu = QMenu("Ticker", self.menu_bar)
        exit_action = QAction("Exit", ticker_menu)
        exit_action.triggered.connect(self.close_ticker)
        timeframe_menu = QMenu("Timeframe", self.menu_bar)
        timeframes = {
            "1min": "1min",
            "3min": "3min", 
            "5min": "5min",
            "15min": "15min",
            "30min": "30min",
            "1hour": "1hour",
            "4hour": "4hour",
            "1day": "1day",
            "1week": "1week",
            "1month": "1month",
            "1year": "1year"
        }
        for name, value in timeframes.items():
            action = QAction(value, timeframe_menu)
            timeframe_menu.addAction(action)
            action.triggered.connect(lambda checked, a=action: self.on_timeframe_changed(a))
        ticker_menu.addAction(exit_action)

        self.charts_menu = QMenu("Charts", self.menu_bar)
        add_chart_action = QAction("Add Chart", self.charts_menu)
        add_chart_action.triggered.connect(self.add_chart)
        self.charts_menu.addAction(add_chart_action)
        self.charts_menu.addAction("Edit Chart")

        # Indicators menu
        self.indicators_menu = QMenu("Indicators", self.menu_bar)
        for indicator in supported_indicators:
            action = QAction(indicator, self.indicators_menu)
            self.indicators_menu.addAction(action)
            action.triggered.connect(lambda checked, i=indicator: self.on_indicator_selected(i))

        # Shapes menu
        self.shapes_menu = QMenu("Shapes", self.menu_bar)
        for shape in supported_figures:
            action = QAction(shape, self.shapes_menu)
            self.shapes_menu.addAction(action)
            action.triggered.connect(lambda checked, s=shape: self.on_shape_selected(s))

        # Strategies menu
        self.strategies_menu = QMenu("Strategies", self.menu_bar)
        for strategy in supported_strategies:
            action = QAction(strategy, self.strategies_menu)
            self.strategies_menu.addAction(action)
            action.triggered.connect(lambda checked, s=strategy: self.on_strategy_selected(s))

        # data menu
        self.data_menu = QMenu("Data", self.menu_bar)
        add_data_action = QAction("Add Data", self.data_menu)
        show_data_action = QAction("Data", self.data_menu)
        show_data_action.triggered.connect(self.show_data)
        add_data_action.triggered.connect(self.add_data)
        self.data_menu.addAction(add_data_action)
        self.data_menu.addAction(show_data_action)

        self.menu_bar.addMenu(ticker_menu)
        self.menu_bar.addMenu(timeframe_menu)
        self.menu_bar.addMenu(self.strategies_menu)
        self.menu_bar.addMenu(self.indicators_menu)
        self.menu_bar.addMenu(self.shapes_menu)
        self.menu_bar.addMenu(self.charts_menu)
        self.menu_bar.addMenu(self.data_menu)
        self.setMenuBar(self.menu_bar)

    def show_data(self):
        self.data_viewer = TickerDataViewer(ticker_name = self.ticker_name, 
                                            charts = self.charts,
                                            parent=self)
        self.data_viewer.draw_tables()
        self.data_viewer.show()

    def add_data(self):
        pass

    def on_strategy_selected(self, strategy):
        pass

    def on_indicator_selected(self, indicator):
        pass

    def on_shape_selected(self, shape):
        if self.dynamic_chart is not None:
            self.dynamic_chart.graphing_view.draw_figure(shape)

    def add_chart(self):
        dialog = QDialog(self)
        dialog.setWindowTitle("Add Chart")

        layout = QVBoxLayout(dialog)

        # Graph type selection
        graph_type_label = QLabel("<b>Select Graph Type:</b>")
        layout.addWidget(graph_type_label)
        graph_type_combo = QComboBox()
        graph_type_combo.addItems(["Candlestick", "Line", "Bar", "Scatter"])
        layout.addWidget(graph_type_combo)

        # Column selection
        column_label = QLabel("<b>Select Column:</b>")
        layout.addWidget(column_label)
        column_combo = QComboBox()
        column_combo.addItems(["Open", "High", "Low", "Close"])
        layout.addWidget(column_combo)

        # Initially hide the column selection combo box
        column_label.setVisible(False)
        column_combo.setVisible(False)

        # Show column selection only if Line chart is selected
        def on_graph_type_changed():
            if graph_type_combo.currentText() == "Line":
                column_label.setVisible(True)
                column_combo.setVisible(True)
            else:
                column_label.setVisible(False)
                column_combo.setVisible(False)

        graph_type_combo.currentIndexChanged.connect(on_graph_type_changed)

        # Timeframe selection
        timeframe_label = QLabel("<b>Select Timeframe:</b>")
        layout.addWidget(timeframe_label)
        timeframe_combo = QComboBox()
        timeframes = ["1min", "3min", "5min", "15min", "30min", "1hour", "4hour", "1day", "1week", "1month", "1year"]
        timeframe_combo.addItems(timeframes)
        layout.addWidget(timeframe_combo)

        # dynamic chart checkbox
        dynamic_chart_checkbox = QCheckBox("Dynamic Chart")
        layout.addWidget(dynamic_chart_checkbox)

        # Placement selection
        placement_label = QLabel("<b>Select Placement:</b>")
        layout.addWidget(placement_label)
        placement_combo = QComboBox()
        placement_combo.addItems(["Upper Splitter", "Lower Splitter", "Dock Left", "Dock Bottom", "Dock Right", "New Window"])
        layout.addWidget(placement_combo)

        # Date range selection toggle
        date_range_toggle = QCheckBox("Enable Date Range Selection")
        layout.addWidget(date_range_toggle)

        # Date range selection
        date_range_label = QLabel("<b>Select Date Range:</b>")
        layout.addWidget(date_range_label)
        start_date_label = QLabel("Start Date:")
        layout.addWidget(start_date_label)
        start_date_edit = QDateEdit()
        start_date_edit.setCalendarPopup(True)
        layout.addWidget(start_date_edit)
        end_date_label = QLabel("End Date:")
        layout.addWidget(end_date_label)
        end_date_edit = QDateEdit()
        end_date_edit.setCalendarPopup(True)
        layout.addWidget(end_date_edit)

        # Initially hide the date range selection widgets
        date_range_label.setVisible(False)
        start_date_label.setVisible(False)
        start_date_edit.setVisible(False)
        end_date_label.setVisible(False)
        end_date_edit.setVisible(False)

        # Toggle visibility of date range selection based on checkbox
        def on_date_range_toggle_changed():
            is_checked = date_range_toggle.isChecked()
            date_range_label.setVisible(is_checked)
            start_date_label.setVisible(is_checked)
            start_date_edit.setVisible(is_checked)
            end_date_label.setVisible(is_checked)
            end_date_edit.setVisible(is_checked)

        date_range_toggle.stateChanged.connect(on_date_range_toggle_changed)

        # Add button
        add_button = QPushButton("Add Chart")
        layout.addWidget(add_button)

        def on_add_button_clicked():
            graph_type = graph_type_combo.currentText()
            timeframe = self.timeframe_map.get(timeframe_combo.currentText(), "Unknown")
            placement = placement_combo.currentText()
            start_date = start_date_edit.date().toString("dd/MM/yyyy") if date_range_toggle.isChecked() else None
            end_date = end_date_edit.date().toString("dd/MM/yyyy") if date_range_toggle.isChecked() else None

            if not dynamic_chart_checkbox.isChecked():
                # Create the appropriate chart based on the selected graph type
                if graph_type == "Candlestick":
                    chart = CandleStickChart(db_manager=self.db_manager, ticker_name=self.ticker_name, time_frame=timeframe)
                    chart.draw_chart()
                elif graph_type == "Line":
                    chart = LineChart(db_manager=self.db_manager, ticker_name=self.ticker_name, time_frame=timeframe, column_name=column_combo.currentText())
                    chart.draw_chart()
                elif graph_type == "Bar":
                    chart = BarChart(x_values=[], y_values=[])
                elif graph_type == "Scatter":
                    chart = ScatterChart(x_values=[], y_values=[])
            else:
                self.dynamic_chart = GraphWindow(self, self.ticker_name, timeframe, self.db_manager)
                chart = self.dynamic_chart
            self.charts[f"{self.ticker_name}_{timeframe}"] = chart
            if chart.is_drawn:
                # Create the chart window
                if not dynamic_chart_checkbox.isChecked():
                    chart_window = ChartWindow(self, chart)
                else:
                    chart_window = chart
                    
                if "Dock" in placement:
                    chart_dock = QDockWidget(f"{self.ticker_name} - {timeframe}", parent=self)
                    chart_dock.setWidget(chart_window)
                else:
                    chart_window.setWindowTitle(f"{graph_type} Chart - {timeframe}")

                # Place the chart window in the selected location
                if placement == "Upper Splitter":
                    self.upper_splitter.addWidget(chart_window)
                elif placement == "Lower Splitter":
                    self.lower_splitter.addWidget(chart_window)
                elif placement == "Dock Left":
                    self.addDockWidget(Qt.LeftDockWidgetArea, chart_dock)
                elif placement == "Dock Bottom":
                    self.addDockWidget(Qt.BottomDockWidgetArea, chart_dock)
                elif placement == "Dock Right":
                    self.addDockWidget(Qt.RightDockWidgetArea, chart_dock)
                elif placement == "New Window":
                    chart_window.setWindowTitle(f"{graph_type} Chart - {timeframe}")
                    chart_window.setMinimumHeight(300)
                    chart_window.setMinimumWidth(800)
                    chart_window.show()

            dialog.accept()

        add_button.clicked.connect(on_add_button_clicked)
        # layout.addStretch(0.1)
        # dialog.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        dialog.exec()

    def add_timeframe_to_tab(self, time_frame):        
        # Find empty splitter
        graph_window = GraphWindow(self, self.ticker_name, time_frame, self.db_manager)
        graph_window.setWindowTitle(time_frame)
        if graph_window.is_drawn:
            for i in range(4):
                if self.splitter_states[i] == 0:
                    if i <= 1:
                        self.upper_splitter.addWidget(graph_window)
                    else:
                        self.lower_splitter.addWidget(graph_window)
                    self.splitter_states[i] = 1
                    break

    def on_timeframe_changed(self, action):
        reply = QMessageBox.question(self, "Timeframe", "Open as new Instance in new Tab?",
                                   QMessageBox.Ok | QMessageBox.Cancel,
                                   QMessageBox.Cancel)
                                   
        if reply == QMessageBox.Ok:
            timeframe = action.text()
        else:
            reply = QMessageBox.question(self, "TimeFrame", "Open in same tab",
                                       QMessageBox.Ok | QMessageBox.Cancel,
                                       QMessageBox.Cancel)
            if reply == QMessageBox.Ok:
                timeframe = action.text()
                new_timeframe = self.timeframe_map.get(timeframe, "Unknown")
                if new_timeframe == "Unknown":
                    QMessageBox.warning(self, "Timeframe Error", "The chosen timeframe has no database available.")
                else:
                    self.add_timeframe_to_tab(new_timeframe)
