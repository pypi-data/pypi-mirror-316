from math import e
from PySide6.QtCharts import (QChart, QChartView, QLineSeries,
                              QValueAxis, QBarSeries, QCandlestickSeries,
                              QScatterSeries, QCandlestickSet,
                              QDateTimeAxis)
from PySide6.QtGui import QPainter, QMouseEvent, QBrush, QColor, QContextMenuEvent
from PySide6.QtWidgets import (QMainWindow, QMessageBox, QGraphicsView,
                               QFileDialog, QMenu)
from PySide6.QtCore import QDateTime , Qt
import matplotlib
from lxfx.gui.dbManager import DbManager
import matplotlib
matplotlib.use("QtAgg")
import matplotlib.pyplot as plt

class Chart:
    def __init__(self, db_manager:DbManager):
        self.chart = QChart()
        self.chart_view = QChartView(self.chart)
        self.chart_view.setChart(self.chart)
        # self.chart_view.setRubberBand(QChartView.HorizontalRubberBand)
        self.chart_view.setDragMode(QChartView.ScrollHandDrag)
        self.chart_view.setOptimizationFlags(QGraphicsView.DontSavePainterState)
        self.chart_view.setViewportUpdateMode(QGraphicsView.SmartViewportUpdate)
        self.chart_view.setTransformationAnchor(QGraphicsView.AnchorUnderMouse)
        self.chart_view.setBackgroundBrush(QBrush(Qt.white))
        self.chart.setBackgroundBrush(QBrush(Qt.white))
        self.chart_view.setRenderHint(QPainter.Antialiasing)

        self.date_axis = None 
        self.series = None
        self.db_manager = db_manager
        self.ticker_name = None
        self.time_frame = None

        self.is_drawn = False

    def create_date_axis(self):
        self.date_axis = QDateTimeAxis()
        self.date_axis.setFormat("yyyy-MM-dd")
        # self.date_axis.setTickCount(len(self.dates))
        self.date_axis.setTitleText("Date")
        self.date_axis.setRange(QDateTime.fromString(self.dates[-1], "yyyy-MM-dd"), QDateTime.fromString(self.dates[0], "yyyy-MM-dd"))
        self.chart.setAxisX(self.date_axis, self.series)
    
    def update_date_axis(self, dates: list[str]):
        # Update the date axis range if new dates are added
        if self.dates:
            self.dates.extend(dates)
            self.date_axis.setRange(QDateTime.fromString(self.dates[0], "yyyy-MM-dd"), QDateTime.fromString(self.dates[-1], "yyyy-MM-dd"))
        else:
            self.dates = dates
            self.create_date_axis()

    def load_data(self, start_candle_id: int = None,
                  end_candle_id: int = None,
                  column_name: str = None,
                  start_date: str = None,
                  end_date: str = None):
        # try:
        table_name = self.ticker_name+"_"+self.time_frame
        if table_name not in self.db_manager.get_available_tables():
            available_tables = self.db_manager.get_available_tables()
            available_tables = [table for table in available_tables if self.ticker_name in table]
            available_tables_str = "\n".join(available_tables)
            QMessageBox.critical(None, "Error", f"Table {table_name} not found.\nAvailable tables:\n{available_tables_str}")
            return None
        data = self.db_manager.load_data(start_candle_id=start_candle_id, 
                                        end_candle_id=end_candle_id, 
                                        table_name=table_name,
                                        column_name=column_name,
                                        start_date=start_date,
                                        end_date=end_date)
        return data
        # except Exception as e:
        #     QMessageBox.critical(self, "Error", f"Error loading data: {e}")

class LineChart(Chart):
    def __init__(self, x_axis: list[float] = None, 
                 y_axis: list[float] = None,
                 dates: list[str] = None,
                 db_manager: DbManager = None,
                 ticker_name: str = None,
                 time_frame: str = None,
                 column_name: str = None,
                 start_date: str = None,
                 end_date: str = None):
        super().__init__(db_manager)
        self.series = QLineSeries()
        self.chart.addSeries(self.series)
        self.y_axis = x_axis
        self.x_axis = y_axis
        self.dates = dates
        self.ticker_name = ticker_name
        self.time_frame = time_frame
        self.column_name = column_name
        self.start_date = start_date
        self.end_date = end_date

    def draw_chart(self):
        data = self.load_data(start_candle_id=0,
                                end_candle_id=100, 
                                column_name=self.column_name)
        if data:
            y_axis, self.dates = data
            self.load_series(y_axis = y_axis)
            self.chart.setTitle(f"{self.ticker_name} {self.time_frame} {self.column_name}")
            self.is_drawn = True

    def load_series(self, x_axis: list[float] = None, y_axis: list[float] = None):
        if x_axis and y_axis:
            for x, y in zip(x_axis, y_axis):
                self.series.append(x, y)
            x_axis = QValueAxis()
            x_axis.setRange(min(x_axis), max(x_axis))
            self.chart.setAxisX(x_axis, self.series)
        elif self.dates:
            if y_axis:
                for date_str, y in zip(self.dates, y_axis):
                    dt = QDateTime.fromString(date_str, "yyyy-MM-dd")
                    self.series.append(dt.toMSecsSinceEpoch(), y)
                self.create_date_axis()
                # for i, y in enumerate(y_axis):
                #     self.series.append(i, y)
                # x_axis = QValueAxis()
                # x_axis.setRange(0, len(y_axis))
                # self.chart.setAxisX(x_axis, self.series)
        else:
            if y_axis:
                for i, y in enumerate(y_axis):
                    self.series.append(i, y)
            self.chart.setAxisX(QValueAxis(), self.series)
        yAxis = QValueAxis()
        yAxis.setRange(min(y_axis), max(y_axis))
        yAxis.setTitleText(self.column_name)
        self.chart.setAxisY(yAxis, self.series)

class BarChart(Chart):
    def __init__(self, x_axis: list[float], y_axis: list[float]):
        super().__init__()
        self.series = QBarSeries()
        self.chart.addSeries(self.series)
        self.series.append(x_axis, y_axis)
        self.chart.createDefaultAxes()
        self.chart.setAxisX(QValueAxis(x_axis), self.series)
        self.chart.setAxisY(QValueAxis(y_axis), self.series)

class CandleStickChart(Chart):
    def __init__(self, open_prices: list[float] = None,
                 high_prices: list[float] = None,
                 low_prices: list[float] = None,
                 close_prices: list[float] = None,
                 dates: list[str] = None,
                 db_manager: DbManager = None,
                 ticker_name: str = None,
                 time_frame: str = None,
                 start_date: str = None,
                 end_date: str = None):
        super().__init__(db_manager)
        self.series = QCandlestickSeries()
        self.chart.addSeries(self.series)
        self.series.setIncreasingColor(QColor(Qt.green))
        self.series.setDecreasingColor(QColor(Qt.red))

        self.open_prices = open_prices
        self.high_prices = high_prices
        self.low_prices = low_prices
        self.close_prices = close_prices
        self.dates = dates
        self.ticker_name = ticker_name
        self.time_frame = time_frame
        self.start_date = start_date
        self.end_date = end_date

    def initializeChart(self):
        if self.dates:
            self.create_date_axis()
        else:
            x_axis = QValueAxis()
            x_axis.setRange(0, len(self.open_prices))
            self.chart.setAxisX(x_axis, self.series)
        y_axis = QValueAxis()
        y_axis.setRange(min(self.low_prices), max(self.high_prices))
        self.chart.setAxisY(y_axis, self.series)

    def draw_chart(self):
        data = self.load_data(start_candle_id = 0, end_candle_id = 100)
        if data:
            self.open_prices, self.high_prices, self.low_prices, self.close_prices, self.dates = data
            self.load_series(*data)
            self.initializeChart()
            self.is_drawn = True

    def load_series(self, open_prices: list[float], high_prices: list[float], low_prices: list[float], close_prices: list[float], dates: list[str]):
        for i in range(len(open_prices)):
            dt = QDateTime.fromString(dates[i], "yyyy-MM-dd")
            candle_stick_set = QCandlestickSet(open_prices[i], 
                                               high_prices[i],
                                               low_prices[i],
                                               close_prices[i],
                                               timestamp = dt.toMSecsSinceEpoch(),
                                               parent = self.series)
            self.series.append(candle_stick_set)

class CandleStickChartView(QChartView):
    def __init__(self, chart: CandleStickChart):
        super().__init__(chart.chart)
        self.chart = chart
        self.last_mouse_position = None
    # def mouseMoveEvent(self, event: QMouseEvent):

class ScatterChart(Chart):
    def __init__(self, x_axis: list[float], y_axis: list[float]):
        super().__init__()
        self.series = QScatterSeries()
        self.chart.addSeries(self.series)
        self.series.append(x_axis, y_axis)
        self.chart.createDefaultAxes()
        self.chart.setAxisX(QValueAxis(x_axis), self.series)
        self.chart.setAxisY(QValueAxis(y_axis), self.series)

class ChartWindow(QMainWindow):
    def __init__(self,parent = None, chart: Chart = None):
        super().__init__(parent)
        self.chart = chart
        self.setCentralWidget(self.chart.chart_view)

    def contextMenuEvent(self, event: QContextMenuEvent):
        menu = QMenu(self)
        save_chart_action = menu.addAction("Save Chart")
        save_chart_action.setShortcut("Ctrl+S")
        save_chart_action.triggered.connect(self.save_chart)
        exit_action = menu.addAction("Exit")
        exit_action.setShortcut("Ctrl+Q")
        exit_action.triggered.connect(self.close)
        action = menu.exec_(event.globalPos())
        if action == save_chart_action:
            self.save_chart()
        elif action == exit_action:
            self.close()

    def save_chart(self):
        file_path, _ = QFileDialog.getSaveFileName(self, "Save Chart", "", "PNG Files (*.png);;JPEG Files (*.jpg);;All Files (*)")
        if file_path:
            pixmap = self.chart.chart_view.grab()
            pixmap.save(file_path)

class MatplotlibChart:
    def __init__(self, title: str = "Matplotlib Chart"):
        self.title = title

    def show_line_chart(self, x_data: list[float], y_data: list[list[float]], x_label: str = "X", y_label: str = "Y", labels: list[str] = None):
        fig = plt.figure()
        axis = fig.add_subplot(111)
        for i, y_series in enumerate(y_data):
            label = labels[i] if labels else f"Series {i+1}"
            axis.plot(x_data, y_series, label=label)
        axis.set_title(self.title)
        axis.set_xlabel(x_label)
        axis.set_ylabel(y_label)
        axis.legend()
        plt.show()

    def show_bar_chart(self, categories: list[str], values: list[list[float]], x_label: str = "Categories", y_label: str = "Values", labels: list[str] = None):
        fig = plt.figure()
        axis = fig.add_subplot(111)
        bar_width = 0.2
        for i, value_series in enumerate(values):
            label = labels[i] if labels else f"Series {i+1}"
            axis.bar([x + i * bar_width for x in range(len(categories))], value_series, width=bar_width, label=label)
        axis.set_title(self.title)
        axis.set_xlabel(x_label)
        axis.set_ylabel(y_label)
        axis.set_xticks([x + bar_width * (len(values) - 1) / 2 for x in range(len(categories))])
        axis.set_xticklabels(categories)
        axis.legend()
        plt.show()

    def show_scatter_chart(self, x_data: list[float], y_data: list[list[float]], x_label: str = "X", y_label: str = "Y", labels: list[str] = None):
        fig = plt.figure()
        axis = fig.add_subplot(111)
        for i, y_series in enumerate(y_data):
            label = labels[i] if labels else f"Series {i+1}"
            axis.scatter(x_data, y_series, label=label)
        axis.set_title(self.title)
        axis.set_xlabel(x_label)
        axis.set_ylabel(y_label)
        axis.legend()
        plt.show()

# Example usage:
# chart = MatplotlibChart(title="Sample Multicolumn Line Chart")
# chart.show_line_chart(x_data=[1, 2, 3], y_data=[[4, 5, 6], [7, 8, 9]], labels=["Series 1", "Series 2"])