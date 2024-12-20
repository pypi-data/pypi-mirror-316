from PySide6.QtCore import QPointF

class Axes:
    def __init__(self, width=100, height=100):
        self.scene_height = height
        self.scene_width = width
        
    def drawAxes(self, painter):
        pass
        
    def valueToPosition(self, xValue, yValue):
        # Assuming the bounding rect's top is 0 and bottom is the height of the scene
        sceneHeight = self.scene_height
        sceneWidth = self.scene_width
        
        # Convert the yValue to a position within the scene
        y = sceneHeight - (yValue * sceneHeight) # Invert the value to match screen coordinates
        
        # Convert the xValue to a position within the scene
        x = xValue * sceneWidth # Scale the xValue to match the scene width

        return QPointF(x, y)
