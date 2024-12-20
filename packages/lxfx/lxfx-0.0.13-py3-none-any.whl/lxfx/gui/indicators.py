from PySide6.QtCore import QRectF, Qt
from PySide6.QtGui import QPen, QPainterPath
from PySide6.QtWidgets import (QWidget, QGraphicsPathItem,
                               QGraphicsScene, QGraphicsView,
                               QPushButton, QLabel, QDialog, 
                               QCheckBox, QHBoxLayout, QVBoxLayout, QLineEdit, 
                               QColorDialog, QSlider)
from PySide6.QtGui import QPainter

from lxfx.gui.figures import DrawableFigure
# from ta import volatility, trend # for practice lets us use our own functions

class IndicatorScene(QGraphicsScene):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setSceneRect(QRectF(0, 0, 800, 600))
        self.indicators = []

    def add_indicator(self, indicator):
        self.indicators.append(indicator)
        self.update()

    def remove_indicator(self, indicator):
        if indicator in self.indicators:
            self.indicators.remove(indicator)
            self.update()

    def drawBackground(self, painter, rect):
        super().drawBackground(painter, rect)
        for indicator in self.indicators:
            indicator.draw(painter)

class IndicatorView(QGraphicsView):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setFixedSize(800, 600)
        self.scene = IndicatorScene(self)
        self.setScene(self.scene)

    def add_indicator(self, indicator):
        self.scene.add_indicator(indicator)

    def remove_indicator(self, indicator):
        self.scene.remove_indicator(indicator)

    def clear_indicators(self):
        self.scene.indicators.clear()
        self.scene.update()

class DrawableBollingerBands():
    def __init__(self, data, period=20, num_std_dev=2, pen_width=2):
        # super().__init__(Qt.blue, pen_width, True)
        self.data = data
        self.period = period
        self.num_std_dev = num_std_dev
        self.pen_width = pen_width
        self.upper_band = []
        self.middle_band = []
        self.lower_band = []
        self.x_positions = []
        self.y_positions = []
        self.get_x_y_positions()
        self.calculate_bands()

    def get_x_y_positions(self):
        for position in self.data:
            self.x_positions.append(position.x())
            self.y_positions.append(position.y())

    def calculate_bands(self):
        if len(self.y_positions) != 0:
            for i in range(len(self.y_positions)):
                if i < self.period - 1:
                    self.upper_band.append(None)
                    self.middle_band.append(None)
                    self.lower_band.append(None)
                else:
                    window = self.y_positions[i - self.period + 1:i + 1]
                    mean = sum(window) / self.period
                    variance = sum((x - mean) ** 2 for x in window) / self.period
                    std_dev = variance ** 0.5
                    self.middle_band.append(mean)
                    self.upper_band.append(mean + self.num_std_dev * std_dev)
                    self.lower_band.append(mean - self.num_std_dev * std_dev)

    def draw_bands(self):
        # Create paths for each band
        upper_path = QPainterPath()
        middle_path = QPainterPath()
        lower_path = QPainterPath()

        # Initialize paths
        if self.upper_band[0] is not None:
            upper_path.moveTo(0, self.upper_band[0])
        if self.middle_band[0] is not None:
            middle_path.moveTo(0, self.middle_band[0])
        if self.lower_band[0] is not None:
            lower_path.moveTo(0, self.lower_band[0])

        # Construct paths
        for i in range(1, len(self.upper_band)):
            if self.upper_band[i] is not None:
                upper_path.lineTo(self.x_positions[i], self.upper_band[i])
            if self.middle_band[i] is not None:
                middle_path.lineTo(self.x_positions[i], self.middle_band[i])
            if self.lower_band[i] is not None:
                lower_path.lineTo(self.x_positions[i], self.lower_band[i])

        upper_graphics_path = QGraphicsPathItem(upper_path)
        middle_graphics_path = QGraphicsPathItem(middle_path)
        lower_graphics_path = QGraphicsPathItem(lower_path)

        pen = QPen(Qt.green)
        pen.setWidth(self.pen_width)
        upper_graphics_path.setPen(pen)
        middle_graphics_path.setPen(pen)
        lower_graphics_path.setPen(pen)
        return upper_graphics_path, middle_graphics_path, lower_graphics_path

class DrawableMACD():
    def __init__(self, data, period=20, pen_width=2):
        self.data = data
        self.period = period
        self.pen_width = pen_width
        self.macd = []
        self.macd_signal = []
        self.macd_histogram = []
        self.calculate_macd()

    def calculate_macd(self):
        short_period = 12
        long_period = 26
        signal_period = 9

        # Calculate short-term EMA
        short_ema = self.calculate_ema(self.data, short_period)

        # Calculate long-term EMA
        long_ema = self.calculate_ema(self.data, long_period)

        # Calculate MACD line
        self.macd = [short - long for short, long in zip(short_ema, long_ema)]

        # Calculate MACD signal line
        self.macd_signal = self.calculate_ema(self.macd, signal_period)

        # Calculate MACD histogram
        self.macd_histogram = [macd - signal for macd, signal in zip(self.macd, self.macd_signal)]

    def calculate_ema(self, data, period):
        ema = []
        multiplier = 2 / (period + 1)
        for i in range(len(data)):
            if i < period:
                ema.append(None)
            elif i == period:
                ema.append(sum(data[:period]) / period)
            else:
                ema.append((data[i] - ema[-1]) * multiplier + ema[-1])
        return ema
    
class DrawableRSI():
    def __init__(self, data, period=14, pen_width=2):
        self.data = data
        self.period = period
        self.pen_width = pen_width
        self.rsi = []
        self.calculate_rsi()

    def calculate_rsi(self):
        gains = []
        losses = []

        for i in range(1, len(self.data)):
            change = self.data[i] - self.data[i - 1]
            if change > 0:
                gains.append(change)
                losses.append(0)
            else:
                gains.append(0)
                losses.append(abs(change))

        average_gain = sum(gains[:self.period]) / self.period
        average_loss = sum(losses[:self.period]) / self.period

        if average_loss == 0:
            self.rsi = [100] * len(self.data)
            return

        rs = average_gain / average_loss
        self.rsi = [100 - (100 / (1 + rs))]

        for i in range(self.period, len(self.data)):
            gain = gains[i]
            loss = losses[i]

            average_gain = ((average_gain * (self.period - 1)) + gain) / self.period
            average_loss = ((average_loss * (self.period - 1)) + loss) / self.period

            if average_loss == 0:
                self.rsi.append(100)
            else:
                rs = average_gain / average_loss
                self.rsi.append(100 - (100 / (1 + rs)))

    def draw_rsi(self):
        pass

class MovingAveragePathItem(QGraphicsPathItem):
    def __init__(self, path, period):
        super().__init__(path)
        self.period = period

class DrawableMovingAverage():
    def __init__(self, data, period=20, pen_width=2):
        self.data = data
        self.period = period
        self.pen_width = pen_width
        self.moving_average = []
        self.x_positions = []
        self.y_positions = []
        self.get_x_y_positions()
        self.calculate_moving_average()

    def get_x_y_positions(self):
        for position in self.data:
            self.x_positions.append(position.x())
            self.y_positions.append(position.y())

    def calculate_moving_average(self):
        if len(self.y_positions) < self.period:
            return
        self.moving_average = [sum(self.y_positions[:self.period]) / self.period] * self.period
        for i in range(self.period, len(self.data)):
            self.moving_average.append((self.y_positions[i] + self.moving_average[-1] * (self.period - 1)) / self.period)

    def draw_moving_average(self):
        path = QPainterPath()
        if self.moving_average and self.moving_average[0] is not None:
            path.moveTo(self.x_positions[0], self.moving_average[0])
        for i in range(1, len(self.moving_average)):
            if self.moving_average[i] is not None:
                path.lineTo(self.x_positions[i], self.moving_average[i])

        pen = QPen(Qt.blue)
        pen.setWidth(self.pen_width)
        graphics_path = MovingAveragePathItem(path, self.period)
        graphics_path.setPen(pen)

        return [graphics_path]
    
class MovingAveragesDialog:
    def __init__(self, parent=None):
        self.moving_averages_dialog = QDialog(parent)
        self.moving_averages_dialog.setWindowTitle("Select Moving Averages")
        self.moving_averages_dialog.setFixedSize(350, 500)  # Adjusted size for better fit
        self.layout = QVBoxLayout()
        self.moving_averages_dialog.setLayout(self.layout)

        self.label = QLabel("Select or enter custom moving averages (comma separated):", self.moving_averages_dialog)
        self.layout.addWidget(self.label)

        self.standard_periods = [20, 50, 100, 200]
        self.checkboxes = []
        self.colors = {}
        self.thicknesses = {}
        self.widgets = {}  # Dictionary to keep track of widgets for each period

        for period in self.standard_periods:
            vertical_layout = QVBoxLayout()
            
            checkbox = QCheckBox(f"{period} periods", self.moving_averages_dialog)
            vertical_layout.addWidget(checkbox)
            self.checkboxes.append(checkbox)
            
            color_button = QPushButton("Select Color", self.moving_averages_dialog)
            color_button.setFlat(False)  # Make the button not flat
            initial_color = self.colors.get(period, Qt.blue)
            color_button.setStyleSheet(f"background-color: {initial_color.name}")
            color_button.clicked.connect(lambda _, p=period, btn=color_button: self.choose_color(p, btn))
            vertical_layout.addWidget(color_button)
            
            thickness_slider = QSlider(Qt.Horizontal, self.moving_averages_dialog)
            thickness_slider.setRange(1, 10)
            thickness_slider.setValue(2)
            thickness_slider.valueChanged.connect(lambda value, p=period: self.set_thickness(p, value))
            vertical_layout.addWidget(thickness_slider)
            
            self.layout.addLayout(vertical_layout)

            # Store the widgets for each period
            self.widgets[period] = {
                'checkbox': checkbox,
                'color_button': color_button,
                'thickness_slider': thickness_slider
            }

        self.custom_input = QLineEdit(self.moving_averages_dialog)
        self.custom_input.setPlaceholderText("Enter custom periods (e.g., 30, 60)")
        self.layout.addWidget(self.custom_input)

        self.button_layout = QVBoxLayout()  # Changed to vertical layout for buttons
        self.ok_button = QPushButton("OK", self.moving_averages_dialog)
        self.ok_button.clicked.connect(self.moving_averages_dialog.accept)
        self.button_layout.addWidget(self.ok_button)

        self.cancel_button = QPushButton("Cancel", self.moving_averages_dialog)
        self.cancel_button.clicked.connect(self.moving_averages_dialog.reject)
        self.button_layout.addWidget(self.cancel_button)

        self.layout.addLayout(self.button_layout)

        self.selected_periods = []
        self.moving_average_states = {}

    def choose_color(self, period, color_button):
        color = QColorDialog.getColor()
        if color.isValid():
            self.colors[period] = color
            color_button.setStyleSheet(f"background-color: {color.name()}")

    def set_thickness(self, period, value):
        self.thicknesses[period] = value

    def exec_(self):
        if self.moving_averages_dialog.exec_():
            self.selected_periods = []
            for period, widgets in self.widgets.items():
                checkbox = widgets['checkbox']
                if checkbox.isChecked():
                    self.selected_periods.append(period)
                    self.moving_average_states[period] = {
                        'color': self.colors.get(period, Qt.blue),
                        'thickness': self.thicknesses.get(period, 2)
                    }
            custom_periods = self.custom_input.text()
            if custom_periods:
                custom_periods = [int(period.strip()) for period in custom_periods.split(",")]
                self.selected_periods.extend(custom_periods)
                for period in custom_periods:
                    if period not in self.moving_average_states:
                        self.moving_average_states[period] = {
                            'color': Qt.blue,
                            'thickness': 2
                        }
            return True
        return False

    def apply_moving_averages(self, graph):
        # Remove unchecked moving averages
        for period, widgets in self.widgets.items():
            checkbox = widgets['checkbox']
            if not checkbox.isChecked() and period in self.moving_average_states:
                # Find and remove the moving average items from the graph
                for item in graph.items():
                    if isinstance(item, MovingAveragePathItem) and item.period == period:
                        graph.removeItem(item)
                del self.moving_average_states[period]

        # Draw new moving averages if selected
        if self.selected_periods:
            data = [node.pos() for node in graph.graph_nodes]
            for s_p in self.selected_periods:
                state = self.moving_average_states.get(s_p, {'color': Qt.blue, 'thickness': 2})
                color = state['color']
                thickness = state['thickness']
                moving_average = DrawableMovingAverage(data=data, period=s_p, pen_width=thickness)
                moving_average_items = moving_average.draw_moving_average()
                for item in moving_average_items:
                    item.setPen(QPen(color, thickness))
                    graph.addItem(item)