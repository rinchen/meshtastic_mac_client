from PyQt6.QtWidgets import QWidget, QVBoxLayout, QLabel
from PyQt6.QtWidgets import QGridLayout
from PyQt6.QtGui import QFont
from PyQt6.QtCore import QTimer
import pyqtgraph as pg
import numpy as np

class TelemetryPanel(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.main = parent
        self.layout = QVBoxLayout(self)

        # Setup Plot
        self.plot_widget = pg.PlotWidget(title="Battery Voltage & RSSI")
        self.plot_widget.showGrid(x=True, y=True)
        self.plot_widget.addLegend()
        self.layout.addWidget(self.plot_widget)
        
        # Data Buffers (50 points)
        self.x_data = np.arange(0, 50)
        self.y_batt = np.zeros(50)
        self.y_rssi = np.zeros(50)
        
        self.curve_batt = self.plot_widget.plot(self.x_data, self.y_batt, pen=pg.mkPen('b', width=2), name="Voltage (V)")
        self.curve_rssi = self.plot_widget.plot(self.x_data, self.y_rssi, pen=pg.mkPen('r', width=2), name="RSSI (dBm)")

    def handle_real_telemetry(self, voltage, rssi):
        """Update the charts with real data from the radio."""
        # Ensure we have valid numbers
        v = voltage if voltage else 0.0
        r = rssi if rssi else -100.0

        # Shift data
        self.y_batt = np.roll(self.y_batt, -1)
        self.y_rssi = np.roll(self.y_rssi, -1)
        
        # Add real data
        self.y_batt[-1] = v
        self.y_rssi[-1] = r
        
        # Update plot
        self.curve_batt.setData(self.y_batt)
        self.curve_rssi.setData(self.y_rssi)

    def update_plots(self):
        # Shift data
        self.y_batt = np.roll(self.y_batt, -1)
        self.y_rssi = np.roll(self.y_rssi, -1)
        
        # Add new random data (Simulated for demo)
        self.y_batt[-1] = np.random.uniform(3.5, 4.2)
        self.y_rssi[-1] = np.random.uniform(-60, -90)
        
        self.curve_batt.setData(self.y_batt)
        self.curve_rssi.setData(self.y_rssi)

