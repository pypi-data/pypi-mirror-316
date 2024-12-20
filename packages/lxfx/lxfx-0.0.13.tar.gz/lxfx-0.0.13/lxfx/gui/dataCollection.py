import os
import time
import json
import logging
import requests
from datetime import datetime
from PySide6.QtCore import QThread, Signal
from concurrent.futures import ThreadPoolExecutor, as_completed

from dbManager import DbManager
from openbb import obb
from lxfx.gui.figures import supported_tickers, supported_timeframes
from lxfx.gui.utils import generate_random_file_path

class DataCollector(QThread):
    update_signal = Signal(str)  # Signal to update the UI with status messages

    def __init__(self, db_manager: DbManager,
                 check_interval: int = 3600,
                 credentials_file:str = None,
                 keep_open_bb_persistent = True):
        super().__init__()
        self.logger = logging.getLogger("dataCollection")
        self.logger.info("DataCollector initialized")
        
        self.db_manager = db_manager
        self.check_interval = check_interval  # Time interval to check for updates in seconds
        self.running = True
        self.credentials_file = credentials_file
        self.keep_open_bb_persistent = keep_open_bb_persistent

    def open_bb_signin(self):
        try:
            with open(self.credentials_file) as cred_file:
                json_str = cred_file.read()
            json_creds = json.loads(json_str)
            obb.account.login(email=json_creds["email"],
                              password=json_creds["password"],
                              remember_me=self.keep_open_bb_persistent)
            self.logger.info("Successfully signed in to OpenBB.")
        except Exception as e:
            self.logger.error(f"Failed to sign in to OpenBB: {e}")

    def run(self):
        while self.running:
            if self.check_internet_connection():
                self.update_signal.emit("Internet connection available. Checking for updates...")
                self.logger.info("Internet connection available.")
                self.collect_data()
            else:
                self.update_signal.emit("No internet connection. Retrying in a while...")
                self.logger.warning("No internet connection.")
            time.sleep(self.check_interval)

    def check_internet_connection(self) -> bool:
        try:
            requests.get("https://www.google.com", timeout=5)
            self.logger.debug("Internet connection check successful.")
            return True
        except requests.ConnectionError:
            self.logger.debug("Internet connection check failed.")
            return False

    def collect_data(self):
        available_tables = self.db_manager.get_available_tables()
        tasks = []
        self.logger.info("Starting data collection process.")

        with ThreadPoolExecutor(max_workers=5) as executor:
            openbb_timeframes = ['1m', '5m', '15m', '30m', '1h', '4h', '1d']
            for ticker_type, tickers in supported_tickers.items():
                for ticker in tickers:
                    for timeframe in openbb_timeframes:
                        table_name = f"{ticker}_{timeframe}"
                        if table_name in available_tables:
                            self.update_signal.emit(f"Updating {table_name}...")
                            self.logger.info(f"Updating table: {table_name}")
                            tasks.append(executor.submit(self.update_table, ticker, timeframe, table_name))
                        else:
                            self.update_signal.emit(f"Creating {table_name}...")
                            self.logger.info(f"Creating table: {table_name}")
                            tasks.append(executor.submit(self.create_table, ticker, timeframe, table_name))

            for future in as_completed(tasks):
                try:
                    future.result()
                except Exception as e:
                    self.update_signal.emit(f"Error during data collection: {e}")
                    self.logger.error(f"Error during data collection: {e}")

    def update_table(self, ticker: str, timeframe: str, table_name: str):
        last_date = self.db_manager.get_most_recent_date(table_name)
        start_date = last_date.strftime("%Y-%m-%d") if last_date else "2023-01-01"
        end_date = datetime.now().strftime("%Y-%m-%d")
        data_filepath = self.fetch_data(ticker, start_date, end_date, timeframe)
        if data_filepath:
            self.db_manager.update_table_from_csv(data_filepath, table_name)
            os.remove(data_filepath)
            self.update_signal.emit(f"{table_name} updated successfully.")
            self.logger.info(f"Table {table_name} updated successfully.")
        else:
            self.update_signal.emit(f"Failed to fetch data for {table_name}.")

    def create_table(self, ticker: str, timeframe: str, table_name: str):
        default_start_date = "2023-01-01"
        end_date = datetime.now().strftime("%Y-%m-%d")
        data_filepath = self.fetch_data(ticker, default_start_date, end_date, timeframe)
        if data_filepath:
            self.db_manager.create_table_from_csv(data_filepath, table_name)
            os.remove(data_filepath)
            self.update_signal.emit(f"{table_name} created and populated successfully.")
            self.logger.info(f"Table {table_name} created and populated successfully.")
        else:
            self.update_signal.emit(f"Failed to fetch data for {table_name}.")

    def fetch_data(self, ticker: str, start_date: str, end_date: str, time_frame: str):
        # ['1m', '5m', '15m', '30m', '1h', '4h', '1d'] supported by openbb
        # Using obb.currency.price.historical returns the following:
        """CurrencyHistorical
        ------------------
        date : Union[date, datetime]
            The date of the data.
        open : float
            The open price.
        high : float
            The high price.
        low : float
            The low price.
        close : float
            The close price.
        volume : Optional[float]
            The trading volume.
        vwap : Optional[Annotated[float, Gt(gt=0)]]
            Volume Weighted Average Price over the period.
        adj_close : Optional[float]
            The adjusted close price. (provider: fmp)
        change : Optional[float]
            Change in the price from the previous close. (provider: fmp)
        change_percent : Optional[float]
            Change in the price from the previous close, as a normalized percent. (provider: fmp)
        transactions : Optional[Annotated[int, Gt(gt=0)]]
            Number of transactions for the symbol in the time period. (provider: polygon)
        """
        try:
            if ticker in supported_tickers["crypto"]:
                data = obb.crypto.price.historical(
                    symbol=ticker,
                    start_date=start_date,
                    end_date=end_date,
                    interval = time_frame
                )
            elif ticker in supported_tickers["forex"]:
                data = obb.currency.price.historical(
                    symbol=ticker,
                    start_date=start_date,
                    end_date=end_date,
                    provider="fmp",
                    interval = time_frame
                )
            elif ticker in supported_tickers["stocks"]:
                data = obb.equity.price.historical(
                    symbol=ticker,
                    start_date=start_date,
                    end_date=end_date,
                    provider="fmp",
                    interval = time_frame
                )
            data = data.to_dataframe()
            # rename the columns to match the expected format
            # format and order : (id, Date, Open, Close, High, Low, Volume)
            data.rename(columns={
                "date": "Date",
                "open": "Open",
                "high": "High",
                "low": "Low",
                "close": "Close",
                "volume": "Volume"
            }, inplace=True)
            # reorder the columns to match the expected format catering for other columns that might exist.
            data = data[["Date", "Open", "Close", "High", "Low", "Volume"]]
            # add an id column if not already present
            if "id" not in data.columns:
                data.insert(0, "id", range(1, len(data) + 1))
            
            # write to a csv file and return the filepath
            filepath = generate_random_file_path("csv")
            data.to_csv(filepath)
            self.logger.info(f"Data fetched successfully for {ticker} from {start_date} to {end_date}.")
            return filepath
        except Exception as e:
            self.update_signal.emit(f"Error fetching data for {ticker}: {e} timeframe: {time_frame}")
            self.logger.error(f"Error fetching data for {ticker}: {e} timeframe: {time_frame}")
            return None

    def stop(self):
        self.running = False
        self.logger.info("DataCollector stopped.")