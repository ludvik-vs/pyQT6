from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QLabel, QFrame,
    QPushButton, QGridLayout
)
from PyQt6.QtCore import Qt
from src.config.api import APIConfig
import socket

class ServerStatusForm(QWidget):
    def __init__(self):
        super().__init__()
        self.setup_ui()
        self.update_status()

    def get_local_ip(self):
        try:
            # Get local IP address
            s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            s.connect(("8.8.8.8", 80))
            local_ip = s.getsockname()[0]
            s.close()
            return local_ip
        except:
            return "Unable to get IP"

    def setup_ui(self):
        layout = QVBoxLayout(self)
        
        status_frame = QFrame()
        status_frame.setFrameStyle(QFrame.Shape.StyledPanel | QFrame.Shadow.Raised)
        status_frame.setStyleSheet("""
            QFrame {
                background-color: #f5f5f5;
                border-radius: 5px;
                padding: 10px;
            }
            QLabel {
                padding: 5px;
            }
            .url-label {
                color: #2962ff;
                text-decoration: underline;
            }
        """)
        
        grid_layout = QGridLayout(status_frame)
        
        # Status indicators
        self.server_status_label = QLabel("Server Status:")
        self.status_value = QLabel()
        self.status_value.setStyleSheet("font-weight: bold;")
        
        self.host_label = QLabel("Host:")
        self.host_value = QLabel()
        
        self.port_label = QLabel("Port:")
        self.port_value = QLabel()
        
        # Local URLs
        self.localhost_label = QLabel("Localhost URL:")
        self.localhost_value = QLabel()
        self.localhost_value.setTextInteractionFlags(Qt.TextInteractionFlag.TextSelectableByMouse)
        self.localhost_value.setStyleSheet("color: #2962ff;")
        
        self.network_label = QLabel("Network URL:")
        self.network_value = QLabel()
        self.network_value.setTextInteractionFlags(Qt.TextInteractionFlag.TextSelectableByMouse)
        self.network_value.setStyleSheet("color: #2962ff;")
        
        # Add widgets to grid
        grid_layout.addWidget(self.server_status_label, 0, 0)
        grid_layout.addWidget(self.status_value, 0, 1)
        grid_layout.addWidget(self.host_label, 1, 0)
        grid_layout.addWidget(self.host_value, 1, 1)
        grid_layout.addWidget(self.port_label, 2, 0)
        grid_layout.addWidget(self.port_value, 2, 1)
        grid_layout.addWidget(self.localhost_label, 3, 0)
        grid_layout.addWidget(self.localhost_value, 3, 1)
        grid_layout.addWidget(self.network_label, 4, 0)
        grid_layout.addWidget(self.network_value, 4, 1)
        
        layout.addWidget(status_frame)
        layout.addStretch()

    def update_status(self):
        if APIConfig.SERVER_ENABLED:
            self.status_value.setText("Running")
            self.status_value.setStyleSheet("color: green; font-weight: bold;")
            self.host_value.setText(APIConfig.HOST)
            self.port_value.setText(str(APIConfig.PORT))
            
            # Update URLs
            self.localhost_value.setText(f"http://localhost:{APIConfig.PORT}")
            local_ip = self.get_local_ip()
            self.network_value.setText(f"http://{local_ip}:{APIConfig.PORT}")
        else:
            self.status_value.setText("Disabled")
            self.status_value.setStyleSheet("color: red; font-weight: bold;")
            self.host_value.setText("N/A")
            self.port_value.setText("N/A")
            self.localhost_value.setText("N/A")
            self.network_value.setText("N/A")