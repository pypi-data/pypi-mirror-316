from PySide6.QtWidgets import (QTableWidget, QTableWidgetItem, QVBoxLayout,
                               QWidget, QPushButton, QHBoxLayout, QMessageBox,
                               QInputDialog, QTabWidget, QMainWindow)
from PySide6.QtCore import Qt
from lxfx.gui.charting import MatplotlibChart

class DataTable(QTableWidget):
    def __init__(self, data_dict, parent=None):
        super().__init__(parent)
        self.data_dict = data_dict
        self.set_data(data_dict)
        self.setEditTriggers(QTableWidget.NoEditTriggers)  # Make table non-editable

    def set_data(self, data_dict):
        self.clear()
        self.setColumnCount(len(data_dict.keys()))
        self.setRowCount(len(next(iter(data_dict.values()))))
        self.setHorizontalHeaderLabels(data_dict.keys())

        for col, (key, values) in enumerate(data_dict.items()):
            for row, value in enumerate(values):
                self.setItem(row, col, QTableWidgetItem(str(value)))

    def delete_column(self, column_name):
        if column_name in self.data_dict:
            col_index = list(self.data_dict.keys()).index(column_name)
            self.removeColumn(col_index)
            del self.data_dict[column_name]
        else:
            QMessageBox.warning(self, "Error", f"Column '{column_name}' does not exist.")

    def delete_row(self, row_index):
        if 0 <= row_index < self.rowCount():
            self.removeRow(row_index)
            for key in self.data_dict.keys():
                del self.data_dict[key][row_index]
        else:
            QMessageBox.warning(self, "Error", f"Row '{row_index}' does not exist.")

class DataTableWidget(QWidget):
    def __init__(self, data_dict, parent=None):
        super().__init__(parent)
        self.data_table = DataTable(data_dict)
        self.layout = QVBoxLayout()
        self.layout.addWidget(self.data_table)

        self.button_layout = QHBoxLayout()
        self.delete_column_button = QPushButton("Delete Column")
        self.delete_column_button.clicked.connect(self.delete_column)
        self.button_layout.addWidget(self.delete_column_button)

        self.delete_row_button = QPushButton("Delete Row")
        self.delete_row_button.clicked.connect(self.delete_row)
        self.button_layout.addWidget(self.delete_row_button)

        self.plot_button = QPushButton("Plot")
        self.plot_button.clicked.connect(self.plot_column)
        self.button_layout.addWidget(self.plot_button)

        self.layout.addLayout(self.button_layout)
        self.setLayout(self.layout)

    def plot_column(self):
        column_name, ok = QInputDialog.getText(self, "Plot Column", "Enter column name to plot:")
        if ok and column_name in self.data_table.data_dict:
            data = self.data_table.data_dict[column_name]
            chart_type, ok = QInputDialog.getItem(self, "Select Chart Type", "Choose chart type:", ["Line", "Bar", "Scatter"], 0, False)
            if ok:
                self.plot_data(column_name, data, chart_type)

    def plot_data(self, column_name, data, chart_type):
        x_data = list(range(len(data)))
        y_data = [data]

        chart = MatplotlibChart(title=f"{column_name} Chart")
        if chart_type == "Line":
            chart.show_line_chart(x_data, y_data, x_label="Index", y_label=column_name)
        elif chart_type == "Bar":
            chart.show_bar_chart(categories=[str(i) for i in x_data], values=y_data, x_label="Index", y_label=column_name)
        elif chart_type == "Scatter":
            chart.show_scatter_chart(x_data, y_data, x_label="Index", y_label=column_name)

    def delete_column(self):
        column_name, ok = QInputDialog.getText(self, "Delete Column", "Enter column name to delete:")
        if ok and column_name:
            self.data_table.delete_column(column_name)

    def delete_row(self):
        row_index, ok = QInputDialog.getInt(self, "Delete Row", "Enter row index to delete:")
        if ok:
            self.data_table.delete_row(row_index)

class TickerDataViewer(QMainWindow):
    def __init__(self, ticker_name, charts, parent=None):
        super().__init__(parent)
        self.ticker_name = ticker_name
        self.charts = charts
        
        self.setWindowTitle(f"Data for {self.ticker_name}")
        self.setGeometry(100, 100, 800, 600)

        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)
        
        self.layout_ = QVBoxLayout()
        self.central_widget.setLayout(self.layout_)
        
        # Create a QTabWidget to hold multiple tables
        self.tab_widget = QTabWidget()
        self.layout_.addWidget(self.tab_widget)
        
    def draw_tables(self):
        # Add a tab for each chart
        for chart_name, chart in self.charts.items():
            data_table = DataTableWidget(chart.GraphingScene.data_dict)
            self.tab_widget.addTab(data_table, chart_name)

    def add_data(self, column_name, data):
        if column_name not in self.data_table.data_dict:
            self.data_table.data_dict[column_name] = data
            self.data_table.setColumnCount(len(self.data_table.data_dict))
            self.data_table.setHorizontalHeaderLabels(self.data_table.data_dict.keys())
            for row, value in enumerate(data):
                self.data_table.setItem(row, len(self.data_table.data_dict) - 1, QTableWidgetItem(str(value)))
        else:
            QMessageBox.warning(self, "Error", f"Column '{column_name}' already exists.")
    