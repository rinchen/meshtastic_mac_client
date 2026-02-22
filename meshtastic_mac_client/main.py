import sys
import asyncio
import qasync
from PyQt6.QtWidgets import QApplication

# Update this to use the full package name
from meshtastic_mac_client.ui.main_window import MainWindow
from meshtastic_mac_client.core.database import DatabaseManager

def main():
    app = QApplication(sys.argv)
    loop = qasync.QEventLoop(app)
    asyncio.set_event_loop(loop)

    # Pass the loop to MainWindow
    window = MainWindow(loop)
    window.show()

    with loop:
        loop.run_forever()

if __name__ == "__main__":
    main()