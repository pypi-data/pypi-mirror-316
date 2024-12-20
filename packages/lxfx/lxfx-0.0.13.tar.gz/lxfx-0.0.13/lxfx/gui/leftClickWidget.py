from PySide6.QtWidgets import QWidget, QVBoxLayout, QMenu, QGraphicsScene, QGraphicsProxyWidget
from PySide6.QtGui import QAction
from PySide6.QtCore import QEvent

from lxfx.gui.graph import Graph
from lxfx.gui.figures import supported_figures, supported_indicators

class LeftClickWidget(QWidget):
    def __init__(self,parent = None):
        super().__init__(parent)
        
        self.setFixedSize(300, 300)
        self.leftClickWidgetLayout = QVBoxLayout()
        self.setLayout(self.leftClickWidgetLayout)

        self.initializeMenu()

    def initializeMenu(self):
        self.OptionsMenu = QMenu()
        self.leftClickWidgetLayout.addWidget(self.OptionsMenu)

        self.indicatorsMenu = QMenu("Indicators", self.OptionsMenu)
        self.OptionsMenu.addMenu(self.indicatorsMenu)

        # Use supported_indicators list to create actions
        self.indicator_actions = {}
        for indicator in supported_indicators:
            action = QAction(indicator.replace("_", " ").title(), self)
            self.indicatorsMenu.addAction(action)
            self.indicator_actions[indicator] = action

        self.figuresMenu = QMenu("Figures", self.OptionsMenu)
        self.OptionsMenu.addMenu(self.figuresMenu)

        # Use supported_figures list to create actions
        self.figure_actions = {}
        for figure in supported_figures:
            action = QAction(figure.replace("_", " ").title(), self)
            self.figuresMenu.addAction(action)
            self.figure_actions[figure] = action

    # def leaveEvent(self, event: QEvent):
    #     self.close()
    #     super().leaveEvent(event)
