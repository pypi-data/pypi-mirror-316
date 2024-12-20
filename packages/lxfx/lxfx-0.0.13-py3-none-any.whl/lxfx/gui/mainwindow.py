from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QMainWindow, QSplitter, QTabWidget, QMenuBar, QMenu,
    QMessageBox, QFileDialog, QInputDialog, QDialog, QDialogButtonBox, QComboBox, QLabel, QLabel
)
from PySide6.QtCore import Qt
from PySide6.QtGui import QAction, QMouseEvent

from lxfx.gui.dbManager import DbManager
from lxfx.gui.tickerInstance import TickerInstance
from lxfx.gui.leftClickWidget import LeftClickWidget

class MainWindow(QMainWindow):
    supported_tickers = {
        "currencies": ["EURUSD", "GBPUSD", "USDCHF", "USDJPY", "AUDUSD", "NZDUSD", "USDCAD"],
        "coins": ["BTCUSD", "ETHUSD"]
    }

    def __init__(self, parent=None):
        super().__init__(parent)
        
        self.db_manager = DbManager("QTRADINGVIEWFXDATA")
        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)
        
        self.main_layout = QVBoxLayout()
        self.central_widget.setLayout(self.main_layout)
        
        self.main_tab_widget = QTabWidget()
        self.main_layout.addWidget(self.main_tab_widget)
        
        self.setup_menu_bar()
        # main_instance_window = TickerInstance(self, "EURUSD_D1", "EURUSD", "D1", self.db_manager)
        # self.main_tab_widget.addTab(main_instance_window, main_instance_window.instance_name)
        self.current_ticker_index = 0
        self.ticker_instances = []

        self.setMinimumHeight(600)
        self.setMinimumWidth(800)

    def setup_menu_bar(self):
        self.menu_bar = QMenuBar(self)

        file_menu = QMenu("App", self.menu_bar)
        self.menu_bar.addMenu(file_menu)
        exit_action = QAction("Exit", file_menu)
        file_menu.addAction(exit_action)
        
        data_menu = QMenu("Data", self.menu_bar)
        self.menu_bar.addMenu(data_menu)
        load_data_action = QAction("Load Data", data_menu)
        data_menu.addAction(load_data_action)
        load_data_action.triggered.connect(self.load_data_from_csv)
        collect_data_action = QAction("Collect Data", data_menu)
        collect_data_action.triggered.connect(self.collect_data)
        data_menu.addAction(collect_data_action)
        
        tickers_menu = QMenu("Tickers", self.menu_bar)
        self.menu_bar.addMenu(tickers_menu)
        for ticker_type, tickers in self.supported_tickers.items():
            ticker_type_menu = QMenu(ticker_type, tickers_menu)
            tickers_menu.addMenu(ticker_type_menu)
            for ticker in tickers:  
                ticker_action = QAction(ticker, ticker_type_menu)
                ticker_action.triggered.connect(lambda checked, t=ticker: self.open_ticker_instance(t))
                ticker_type_menu.addAction(ticker_action)

        account_action = QAction("Account")
        self.menu_bar.addAction(account_action)
        self.setMenuBar(self.menu_bar)

    def collect_data(self):
        pass

    def open_ticker_instance(self, ticker):
        available_tables = self.db_manager.get_available_tables()
        tables_for_ticker_available = False 
        for table in available_tables:
            if ticker in table:
                tables_for_ticker_available = True
                break
        if tables_for_ticker_available:
            ticker_instance = TickerInstance(self,
                                            instance_name=ticker,
                                            ticker_name=ticker, 
                                            db_manager=self.db_manager,
                                            ticker_index=self.current_ticker_index
                                            )
            self.main_tab_widget.addTab(ticker_instance, ticker_instance.instance_name)
            self.ticker_instances.append(ticker_instance)
            ticker_instance.close_ticker_signal.connect(self.close_ticker_instance)
            ticker_instance.add_chart()
            self.current_ticker_index += 1
        else:
            QMessageBox.critical(self, "Error", f"Tables for ticker: {ticker} not found")

    def close_ticker_instance(self, ticker_index):
        self.ticker_instances[ticker_index].close()
        self.ticker_instances.pop(ticker_index)
        self.main_tab_widget.removeTab(ticker_index)

    def load_data_from_csv(self):
        filepath, _ = QFileDialog.getOpenFileName(self, "Open CSV File", "/", "CSV files (*.csv)")
        if filepath and filepath.endswith('.csv'):
            tickers = [ticker for ticker_list in self.supported_tickers.values() for ticker in ticker_list]
            ticker_combo = QComboBox()
            ticker_combo.addItems(tickers)
            timeframe_combo = QComboBox()
            timeframes = ["D1", "H1", "M1", "W1", "MN1", "H4", "M5", "M15", "M30", "H2", "H3", "H6", "H8", "H12"]
            timeframe_combo.addItems(timeframes)

            dialog = QDialog(self)
            dialog.setWindowTitle("Select Ticker and Timeframe")
            layout = QVBoxLayout(dialog)
            layout.addWidget(QLabel("Select Ticker:"))
            layout.addWidget(ticker_combo)
            layout.addWidget(QLabel("Select Timeframe:"))
            layout.addWidget(timeframe_combo)
            buttons = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel, Qt.Horizontal, dialog)
            layout.addWidget(buttons)

            def on_accept():
                ticker = ticker_combo.currentText()
                timeframe = timeframe_combo.currentText()
                table_name = f"{ticker}_{timeframe}"
                if self.db_manager.create_table_from_csv(filepath, table_name):
                    QMessageBox.information(self, "Success", f"Table {table_name} loaded successfully")
                dialog.accept()

            buttons.accepted.connect(on_accept)
            buttons.rejected.connect(dialog.reject)

            if dialog.exec() == QDialog.Accepted:
                pass
            else:
                QMessageBox.critical(self, "Error", "Table name is required.")
        else:
            QMessageBox.critical(self, "Error", "Invalid file format. Please select a CSV file.")

    # def mousePressEvent(self, event:QMouseEvent):
    #     if event.button() == Qt.RightButton:
    #         mouse_pos = event.pos()
    #         left_click_widget = LeftClickWidget(self)
    #         left_click_widget.move(mouse_pos)
    #         left_click_widget.show()
    #     super().mousePressEvent(event)