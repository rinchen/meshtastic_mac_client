class NodeListPanel(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.parent = parent
        self.main = parent
        self.layout = QVBoxLayout(self)

        self.table = QTableWidget()
        # Increased to 8 columns
        self.table.setColumnCount(8)
        self.table.setHorizontalHeaderLabels([
            "ID", "Long Name", "Short Name", "SNR", "Battery", "Last Heard", "Lat", "Lon"
        ])
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        self.layout.addWidget(self.table)

    def on_node_update(self, node):
        self.refresh_list()

    def refresh_list(self):
        nodes = self.main.db.get_nodes()
        self.table.setRowCount(len(nodes))
        
        for row, node_data in enumerate(nodes):
            # Map the SQLite row fields to the table columns
            self.table.setItem(row, 0, QTableWidgetItem(str(node_data['id'])))
            self.table.setItem(row, 1, QTableWidgetItem(node_data['long_name'] or "Unknown"))
            self.table.setItem(row, 2, QTableWidgetItem(node_data['short_name'] or "N/A"))
            self.table.setItem(row, 3, QTableWidgetItem(f"{node_data['snr']:.2f}" if node_data['snr'] else "0.00"))
            
            # Battery formatting
            batt = node_data['battery']
            self.table.setItem(row, 4, QTableWidgetItem(f"{batt}%" if batt else "N/A"))
            
            # Last Heard
            self.table.setItem(row, 5, QTableWidgetItem(str(node_data['last_heard'])))
            
            # GPS Coordinates
            lat = node_data['position_lat']
            lon = node_data['position_lon']
            self.table.setItem(row, 6, QTableWidgetItem(f"{lat:.4f}" if lat else "N/A"))
            self.table.setItem(row, 7, QTableWidgetItem(f"{lon:.4f}" if lon else "N/A"))