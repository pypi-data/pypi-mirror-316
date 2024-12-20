from PySide6.QtCore import QObject, QTimer, QUrl, Signal
from PySide6.QtWebSockets import QWebSocket
from PySide6.QtCore import QUrlQuery
from PySide6.QtCore import QDebug

class CandleDataStreamer(QObject):
    # Signal to notify data update
    dataUpdated = Signal(bytes)

    def __init__(self):
        super().__init__()
        self.webSocket = QWebSocket()
        self.apiKey = ""
        self.pingTimer = QTimer()

        # Connect signals
        self.webSocket.connected.connect(self.onConnected)
        self.webSocket.textMessageReceived.connect(self.onTextMessageReceived) 
        self.webSocket.pong.connect(self.onPongReceived)

        # Initialize and configure ping timer
        self.pingTimer.timeout.connect(self.onPingTimeout)
        self.pingTimer.setInterval(30000) # Ping every 30 seconds

    def __del__(self):
        self.pingTimer.stop()
        self.webSocket.close()

    def connectToServer(self, url, apiKey):
        # Connect to WebSocket server with API key
        urlWithKey = QUrl(url)
        query = QUrlQuery()
        query.addQueryItem("api_key", apiKey)
        urlWithKey.setQuery(query)
        self.webSocket.open(urlWithKey)

    def startDataStream(self):
        # Start the data stream
        if self.webSocket.isValid():
            self.webSocket.sendTextMessage("Start Data Stream")

    def onConnected(self):
        # Handle connection established
        print("WebSocket connected")
        self.webSocket.sendTextMessage(self.apiKey) # Send API key
        self.startDataStream()
        self.pingTimer.start() # Start the ping timer

    def onTextMessageReceived(self, message):
        # Handle incoming data
        print(f"Received message: {message}")
        self.dataUpdated.emit(message.encode('utf-8'))

    def onPingTimeout(self):
        # Send a ping message
        if self.webSocket.isValid():
            self.webSocket.ping()
        else:
            # Attempt to reconnect if WebSocket is not valid
            print("WebSocket is not valid, attempting to reconnect...")
            self.webSocket.open(self.webSocket.requestUrl())

    def onPongReceived(self, elapsedTime, payload):
        # Handle pong response
        print(f"Pong received, elapsed time: {elapsedTime} ms, payload: {payload}")
