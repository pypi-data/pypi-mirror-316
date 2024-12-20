from PySide6.QtWidgets import QMainWindow, QSlider, QWidget, QVBoxLayout, QHBoxLayout
from PySide6.QtCore import Qt

from lxfx.gui.GraphingView import GraphingView
from lxfx.gui.graph import CandleStickDynamicGraph

class GraphWindow(QMainWindow):
    def __init__(self,
                 parent,
                 pair_name,
                 time_frame,
                 db_manager):
        super().__init__(parent)
        self.GraphingScene = None
        self.pair_name = pair_name
        self.time_frame = time_frame
        self.db_manager = db_manager
        self.slider_value = 500
        self.graphing_view = None
        self.horizontal_slider = None
        self.vertical_slider = None
        # Create the scene and view
        self.graphing_view = GraphingView(self)
        self.GraphingScene = CandleStickDynamicGraph(self,ticker_name=self.pair_name,
                                                     db_manager=self.db_manager,
                                                     time_frame=self.time_frame,
                                                     pixels_per_pip=1,
                                                     graphing_view=self.graphing_view)
        # self.GraphingScene.setBackgroundBrush(Qt.black)
        self.GraphingScene.draw_graph()
        self.GraphingScene.draw_line_graph()
        # self.GraphingScene.draw_volume_graph(start_candle_id=0, end_candle_id=self.GraphingScene.SCENE_MAX_NODES)
        if self.GraphingScene.is_drawn:
            self.graphing_view.setScene(self.GraphingScene)
            # self.graphing_view.setStyleSheet("background-color: black;")
            self.setup_ui()
            self.setup_connections()

        self.is_drawn = self.GraphingScene.is_drawn

    def get_table_name(self):
        table_name = self.pair_name + "_" + self.time_frame
        if table_name.islower():
            table_name = table_name[0].upper() + table_name[1:]
        return table_name

    def __del__(self):
        # Clean up
        del self.GraphingScene
        del self.graphing_view

    def setup_ui(self):
        central_widget = QWidget(self)
        main_layout = QVBoxLayout(central_widget)

        view_layout = QHBoxLayout()
        self.vertical_slider = QSlider(Qt.Vertical, self)
        self.vertical_slider.setRange(50, 10000)  # Adjust range as needed
        self.vertical_slider.setValue(5000)

        view_layout.addWidget(self.graphing_view)
        view_layout.addWidget(self.vertical_slider)

        self.horizontal_slider = QSlider(Qt.Horizontal, self)
        self.horizontal_slider.setRange(50, 10000)  # Adjust range as needed
        self.horizontal_slider.setValue(5000)

        main_layout.addLayout(view_layout)
        main_layout.addWidget(self.horizontal_slider)

        central_widget.setLayout(main_layout)
        self.setCentralWidget(central_widget)

    def setup_connections(self):
        # self.horizontal_slider.valueChanged.connect(self.reset_horizontal_slider)
        self.horizontal_slider.valueChanged.connect(self.graphing_view.set_horizontal_scale)
        self.vertical_slider.valueChanged.connect(self.graphing_view.set_vertical_scale)
