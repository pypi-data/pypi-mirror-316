# dbManager.py
from PySide6.QtWidgets import QWidget, QFileDialog, QProgressDialog, QMessageBox, QInputDialog
from PySide6.QtCore import Qt, QDateTime, QCoreApplication
import mysql.connector
from mysql.connector import Error
from typing import List, Tuple, Optional
import csv

class DbManager(QWidget):
    def __init__(self, db_name: str):
        super().__init__()
        self.db_name = db_name
        self.connection = None
        self.open_db()

        self.cache = {} # TODO 

    def __del__(self):
        self.close_db()

    def open_db(self) -> bool:
        try:
            self.connection = mysql.connector.connect(
                host="localhost",
                user="program",
                password="program",
                database=self.db_name
            )
            if self.connection.is_connected():
                return True
        except Error as e:
            print(f"Error: connection with database failed: {e}")
            return False
        return False

    def close_db(self):
        if self.connection and self.connection.is_connected():
            self.connection.close()

    def get_max_value(self, column_name: str, table_name: str) -> float:
        if not self.connection or not self.connection.is_connected():
            print("Database not open")
            return -1

        cursor = self.connection.cursor()
        query_str = f"SELECT MAX({column_name}) FROM {table_name}"
        
        try:
            cursor.execute(query_str)
            result = cursor.fetchone()
            return float(result[0]) if result[0] is not None else -1
        except Error as e:
            print(f"getMaxValue error: {e}")
            return -1
        finally:
            cursor.close()

    def get_last_date(self, table_name: str) -> str:
        if not self.connection or not self.connection.is_connected():
            print("Database not open")
            return ""
    
        cursor = self.connection.cursor()
        query_str = f"SELECT MIN(Date) FROM {table_name}"
        try:
            cursor.execute(query_str)
            result = cursor.fetchone()
            return str(result[0]) if result[0] is not None else ""
        except Error as e:
            print(f"getLastDate error: {e}")
            return ""
        finally:
            cursor.close()

    def get_most_recent_date(self, table_name: str) -> str:
        if not self.connection or not self.connection.is_connected():
            print("Database not open")
            return ""

        cursor = self.connection.cursor()
        query_str = f"SELECT MAX(Date) FROM {table_name}"

        try:
            cursor.execute(query_str)
            result = cursor.fetchone()
            return str(result[0]) if result[0] is not None else ""
        except Error as e:
            print(f"getLastDate error: {e}")
            return ""
        finally:
            cursor.close()

    def get_min_value(self, column_name: str, table_name: str) -> float:
        if not self.connection or not self.connection.is_connected():
            print("Database not open")
            return -1

        cursor = self.connection.cursor()
        query_str = f"SELECT MIN({column_name}) FROM {table_name}"
        
        try:
            cursor.execute(query_str)
            result = cursor.fetchone()
            return float(result[0]) if result[0] is not None else -1
        except Error as e:
            print(f"getMinValue error: {e}")
            return -1
        finally:
            cursor.close()

    def make_table_from_csv(self):
        filepath, _ = QFileDialog.getOpenFileName(self, "Open CSV File", "/", "CSV files (*.csv)")
        if filepath and filepath.endswith('.csv'):
            # table_name = filepath.split('/')[-1].rsplit('.', 1)[0]
            table_name, ok = QInputDialog.getText(self, "Table Name", "Enter the table name (format: TICKER_TIMEFRAME):\nExamples: EURUSD_D1, BTCUSD_H1")
            if not ok or not table_name:
                QMessageBox.critical(self, "Error", "Table name is required.")
                return
            self.create_table_from_csv(filepath, table_name)
        else:
            QMessageBox.critical(self, "Error", "Invalid file format. Please select a CSV file.")

    def create_table_from_csv(self, csv_file_path: str, table_name: str):
        if not self.connection or not self.connection.is_connected():
            print("Database not open")
            return False

        progress_dialog = QProgressDialog("Creating table...", "Cancel", 0, 100, self)
        progress_dialog.setWindowModality(Qt.WindowModal)
        progress_dialog.show()

        cursor = self.connection.cursor()
        try:
            # Create table
            create_table_query = f"""
                CREATE TABLE {table_name} (
                    id INT,
                    Date DATETIME,
                    Open DECIMAL(10, 4),
                    Close DECIMAL(10, 4),
                    Low DECIMAL(10, 4),
                    High DECIMAL(10, 4),
                    Volume INT
                )
            """
            cursor.execute(create_table_query)

            # Read and insert data line by line instead of LOAD DATA INFILE
            with open(csv_file_path, 'r') as file:
                csv_reader = csv.reader(file)
                total_rows = sum(1 for _ in csv_reader) - 1  # Get total number of rows, excluding header
                file.seek(0)  # Reset file pointer to the beginning
                next(csv_reader)  # Skip header row
                
                insert_query = f"""
                    INSERT INTO {table_name} 
                    (id, Date, Open, Close, High, Low, Volume)
                    VALUES (%s, %s, %s, %s, %s, %s, %s)
                """
                
                # Read all rows and insert in batches
                batch_size = 1000
                rows = []
                processed_rows = 0
                for row in csv_reader:
                    rows.append(row)
                    if len(rows) >= batch_size:
                        cursor.executemany(insert_query, rows)
                        rows = []
                        self.connection.commit()
                        processed_rows += batch_size
                        progress_dialog.setValue(int((processed_rows / total_rows) * 100))
                        if progress_dialog.wasCanceled():
                            cursor.execute(f"DROP TABLE IF EXISTS {table_name}")
                            return
                        
                # Insert any remaining rows
                if rows:
                    cursor.executemany(insert_query, rows)
                    self.connection.commit()
                    processed_rows += len(rows)
                    progress_dialog.setValue(int((processed_rows / total_rows) * 100))

        except Error as e:
            print(f"Failed to create/load table {table_name}: {e}")
            QMessageBox.critical(self, "Error", f"Failed to create/load table {table_name}: {e}") 
            cursor.execute(f"DROP TABLE IF EXISTS {table_name}")
        finally:
            progress_dialog.setValue(100)
            progress_dialog.close()
            cursor.close()
        return True

    def get_table_details(self, table_name: str) -> dict:
        if not self.connection or not self.connection.is_connected():
            print("Database not open")
            return {}

        cursor = self.connection.cursor()
        table_details = {}

        try:
            # Get column names
            cursor.execute(f"DESCRIBE {table_name}")
            columns = cursor.fetchall()
            column_names = [column[0] for column in columns]
            table_details['columns'] = column_names

            # Get number of rows
            cursor.execute(f"SELECT COUNT(*) FROM {table_name}")
            num_rows = cursor.fetchone()[0]
            table_details['num_rows'] = num_rows

            # Get table name
            table_details['table_name'] = table_name

        except Error as e:
            print(f"Failed to get table details for {table_name}: {e}")
            return {}
        finally:
            cursor.close()

        return table_details

    def get_ohlc_data(self, candle_id: int, table_name: str) -> List[float]:
        if not self.connection or not self.connection.is_connected():
            print("Database not open")
            return []

        cursor = self.connection.cursor()
        query_str = f"SELECT Open, High, Low, Close FROM {table_name} WHERE id = %s"
        
        try:
            cursor.execute(query_str, (candle_id,))
            result = cursor.fetchone()
            return [float(result[i]) for i in range(4)] if result else []
        except Error as e:
            print(f"getOHLCData error: {e}")
            return []
        finally:
            cursor.close()

    def get_volume_data(self, table_name: str,
                        start_candle_id: int = None,
                        end_candle_id: int = None,
                        start_date: str = None, 
                        end_date: str = None) -> List[int]:
        return self.get_column_data(table_name, "Volume", start_candle_id, end_candle_id, start_date, end_date)

    def get_column_data(self, table_name: str, column_name: str,
                        start_candle_id: int = None, end_candle_id: int = None,
                        start_date: str = None, end_date: str = None) -> List:
        if not self.connection or not self.connection.is_connected():
            print("Database not open")
            return []

        cursor = self.connection.cursor()
        query_str = f"SELECT {column_name} FROM {table_name} WHERE 1=1"
        params = []

        if start_candle_id is not None and end_candle_id is not None:
            query_str += " AND id BETWEEN %s AND %s"
            params.extend([start_candle_id, end_candle_id])
        
        if start_date is not None and end_date is not None:
            query_str += " AND Date BETWEEN %s AND %s"
            params.extend([start_date, end_date])
        
        try:
            cursor.execute(query_str, params)
            result = cursor.fetchall()
            return [row[0] for row in result] if result else []
        except Error as e:
            print(f"get_column_data error: {e}")
            return []
        finally:
            cursor.close()

    def get_n_nodes(self, table_name: str) -> int:
        if not self.connection or not self.connection.is_connected():
            print("Database not open")
            return -1

        cursor = self.connection.cursor()
        query_str = f"SELECT COUNT(*) FROM {table_name}"
        
        try:
            cursor.execute(query_str)
            result = cursor.fetchone()
            return int(result[0]) if result[0] is not None else -1
        except Error as e:
            print(f"getnNodes error: {e}")
            return -1
        finally:
            cursor.close()

    def load_data(self,
                  table_name: str,
                  column_name: str = None,
                  start_candle_id: int = None,
                  end_candle_id: int = None,
                  start_date: str = None,
                  end_date: str = None,
                  dynamic = False):
        if not self.connection or not self.connection.is_connected():
            print("Database not open")
            return []

        cursor = self.connection.cursor()
        if column_name:
            columns_str = f"{column_name}, Date"
        else:
            columns_str = "Open, High, Low, Close, Date"

        query_str = f"""
            SELECT {columns_str} 
            FROM {table_name} 
            WHERE id BETWEEN %s AND %s 
            ORDER BY id DESC
        """

        if start_date and end_date:
            query_str = f"""
                SELECT {columns_str} 
                FROM {table_name} 
                WHERE Date BETWEEN %s AND %s 
                ORDER BY id DESC
            """

        data = []
        open_prices = []
        high_prices = []
        low_prices = []
        close_prices = []
        column_prices = []
        dates = []
        try:
            cursor.execute(query_str, (start_candle_id, end_candle_id))
            for row in cursor.fetchall():
                if column_name:
                    column_prices.append(float(row[0]))
                    dates.append(str(row[1]))
                else:
                    if dynamic:
                        ohlc_data = [float(row[i]) for i in range(4)]
                        date_time = QDateTime.fromString(str(row[4]), Qt.ISODate)
                        date_time = str(row[4])
                        data.append((ohlc_data, date_time))
                    else:
                        open_prices.append(float(row[0]))
                        high_prices.append(float(row[1]))
                        low_prices.append(float(row[2]))
                        close_prices.append(float(row[3]))
                        dates.append(str(row[4]))
            if column_name:
                return column_prices, dates
            else:
                if dynamic:
                    return data
                else:
                    return open_prices, high_prices, low_prices, close_prices, dates
        except Error as e:
            print(f"loadData error: {e}")
            return []
        finally:
            cursor.close()

    def get_available_tables(self) -> List[str]:
        if not self.connection or not self.connection.is_connected():
            print("Database not open")
            return []

        cursor = self.connection.cursor()
        cursor.execute("SHOW TABLES")
        return [row[0] for row in cursor.fetchall()]
