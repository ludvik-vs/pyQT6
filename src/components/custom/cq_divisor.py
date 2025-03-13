from PyQt6.QtWidgets import QFrame
from PyQt6.QtCore import Qt

class CQDivisor(QFrame):
    """Crea y configura un QFrame como divisor."""
    def __init__(self, parent=None, orientation=Qt.Orientation.Horizontal, thickness=1, color="gray"):
        super().__init__(parent)
        if orientation == Qt.Orientation.Horizontal:
            self.setFrameShape(QFrame.Shape.HLine)
        else:
            self.setFrameShape(QFrame.Shape.VLine)
        self.setFrameShadow(QFrame.Shadow.Sunken)
        self.setLineWidth(thickness)
        self.setStyleSheet(f"QFrame {{ color: {color}; }}")
        self.setContentsMargins(5, 0, 5, 0) if orientation == Qt.Orientation.Vertical else self.setContentsMargins(0, 5, 0, 5)
