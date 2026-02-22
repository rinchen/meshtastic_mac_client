import os
import folium
from PyQt6.QtCore import QUrl
from PyQt6.QtWidgets import QWidget, QVBoxLayout
from PyQt6.QtWebEngineWidgets import QWebEngineView
from PyQt6.QtWebEngineCore import QWebEngineSettings

class MapPanel(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.layout = QVBoxLayout(self)
        self.web_view = QWebEngineView()
        
        # Security: Allow the local HTML to fetch Leaflet/OpenStreetMap CSS and JS
        settings = self.web_view.settings()
        settings.setAttribute(QWebEngineSettings.WebAttribute.LocalContentCanAccessRemoteUrls, True)
        settings.setAttribute(QWebEngineSettings.WebAttribute.JavascriptEnabled, True)
        
        self.layout.addWidget(self.web_view)

    def update_map(self, nodes):
        # Default to Longmont, CO
        center_lat, center_lon = 40.1672, -105.1019
        
        valid_nodes = []
        for n in nodes:
            # Handle both dictionary objects and database row objects
            lat = getattr(n, 'position_lat', None) or (n.get('position_lat') if isinstance(n, dict) else None)
            lon = getattr(n, 'position_lon', None) or (n.get('position_lon') if isinstance(n, dict) else None)
            
            if lat and lon:
                valid_nodes.append(n)

        if valid_nodes:
            # Center on the first valid node
            first = valid_nodes[0]
            center_lat = getattr(first, 'position_lat', None) or first.get('position_lat')
            center_lon = getattr(first, 'position_lon', None) or first.get('position_lon')

        m = folium.Map(
            location=[center_lat, center_lon],
            zoom_start=12,
            tiles="OpenStreetMap"
        )
        
        for node in valid_nodes:
            # Extract name safely
            if isinstance(node, dict):
                name = node.get('user', {}).get('longName') or node.get('id', "Unknown")
                lat, lon = node['position_lat'], node['position_lon']
            else:
                name = getattr(node, 'long_name', "Unknown")
                lat, lon = node.position_lat, node.position_lon

            folium.Marker(
                [lat, lon],
                popup=f"Node: {name}",
                tooltip=name
            ).add_to(m)

        # Use setHtml with a baseUrl to avoid file permission/path issues
        data = m.get_root().render()
        self.web_view.setHtml(data, QUrl("file://"))