import asyncio
import logging
from bleak import BleakScanner
from pubsub import pub
from meshtastic.ble_interface import BLEInterface
from meshtastic_mac_client.core.database import DatabaseManager

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class MeshtasticManager:
    def __init__(self, db_manager, loop):
        self.db = db_manager
        self.loop = loop
        self.client = None
        self.is_connected = False
        self.on_message_received_cb = None
        self.on_node_updated_cb = None

    async def scan_devices(self):
        """Scan for Meshtastic BLE devices with a cache warm-up."""
        # Warm up the macOS BLE cache
        await BleakScanner.discover(timeout=2.0)
        # Actual scan
        devices = await BleakScanner.discover(timeout=5.0) # 5s is usually plenty after a warmup
        return [d for d in devices if d.name]

    async def connect(self, device_address):
        """Connect to a specific device without blocking the UI."""
        try:
            # We run the synchronous BLEInterface constructor in a thread
            # to prevent it from clashing with the UI event loop.
            def _init_ble():
                return BLEInterface(address=device_address, noProto=False)

            self.client = await self.loop.run_in_executor(None, _init_ble)
            
            pub.subscribe(self.on_receive, "meshtastic.receive")
            pub.subscribe(self.on_node_update, "meshtastic.node.updated")
            
            self.is_connected = True
            return True
        except Exception as e:
            logger.error(f"Failed to connect: {e}")
            return False

    async def disconnect(self):
        if self.client:
            # BLEInterface close is typically synchronous in the library
            self.client.close()
            self.is_connected = False
            self.client = None

    def on_receive(self, packet, interface):
        node_id = packet.get("fromId", packet.get("from", "Unknown"))
        decoded = packet.get("decoded", {})
        payload = decoded.get("text", "")
        channel = packet.get("channel", 0)
        self.db.save_message(node_id, "REMOTE", payload, channel)
        if self.on_message_received_cb:
            self.loop.call_soon_threadsafe(
                self.on_message_received_cb, node_id, "REMOTE", payload, channel
            )

    def on_node_update(self, node, interface):
        self.db.save_node(node)
        if self.on_node_updated_cb:
            # Pass both node and interface to match the signal signature
            self.loop.call_soon_threadsafe(self.on_node_updated_cb, node, interface)