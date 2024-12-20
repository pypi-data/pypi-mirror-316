from PySide6.QtWidgets import (QWidget, QVBoxLayout,
                               QLabel, QPushButton,
                               QListWidget, QListWidgetItem,
                               QHBoxLayout, QMessageBox)
from PySide6.QtCore import Qt

from lxfx.gui.data import DataTableWidget

class ModelsWidget(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("AI Models for Price Prediction")
        self.setGeometry(100, 100, 400, 300)
        self.model_input_data = None
        
        self.layout = QVBoxLayout()
        
        self.models_list = QListWidget()
        self.models = [
            {"name": "FxFCModel", "description": """This can only give a single future prediction.
             It uses RNNs, LSTMs, GRUs"""},
            {"name": "FxFCAutoEncoder", "description": """This also uses RNNs, LSTMs, GRUs but it is an encoder
             decoder architecture and so it has support for more than a single future time step prediction"""},
            {"name": "FxFCWavenet", "description": """Uses a Wavenet architecture (CNNs) with dilations to provide an autoregressive
             nature and so able to predict more than a single future time step"""}
        ]
        
        for model in self.models:
            item = QListWidgetItem(model["name"])
            item.setToolTip(model["description"])
            self.models_list.addItem(item)
        
        self.layout.addWidget(QLabel("Select a model to predict prices:"))
        self.layout.addWidget(self.models_list)
        
        # self.data_selection_button = QPushButton("Select Data on Graph")
        # self.data_selection_button.clicked.connect(self.select_data_on_graph)
        # self.layout.addWidget(self.data_selection_button)
        
        # self.show_data_button = QPushButton("Show Model Input Data")
        # self.show_data_button.clicked.connect(self.show_model_input_data)
        # self.layout.addWidget(self.show_data_button)
        
        self.predict_button = QPushButton("Predict Prices")
        self.predict_button.clicked.connect(self.predict_prices)
        self.layout.addWidget(self.predict_button)
        
        # self.results_label = QLabel("Prediction Results will be shown here.")
        # self.results_label.setAlignment(Qt.AlignCenter)
        # self.layout.addWidget(self.results_label)
        
        self.setLayout(self.layout)

        self.setMinimumWidth(400)
        self.setMinimumHeight(400)
    
    def set_model_input_data(self, data_dict:dict):
        # the data dict is in the form of {"column_name": []}
        self.model_input_data = data_dict

    def select_data_on_graph(self):
        # Placeholder for data selection logic
        pass
    
    def show_model_input_data(self):
        if self.model_input_data:
            self.data_viewer = DataTableWidget(self.model_input_data)
            self.data_viewer.setWindowTitle("Model Input Data")
            # self.data_viewer.show()
            self.layout.addWidget(self.data_viewer)
        else:
            QMessageBox.warning(self, "No Data", "No model input data available.")

    def predict_prices(self):
        selected_model_item = self.models_list.currentItem()
        if selected_model_item:
            selected_model_name = selected_model_item.text()
            # Placeholder for prediction logic
            self.results_label.setText(f"Predicted prices using {selected_model_name} will be shown here.")
        else:
            self.results_label.setText("Please select a model first.")
