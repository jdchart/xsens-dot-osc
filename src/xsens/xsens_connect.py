"""
Made following https://medium.com/@protobioengineering/how-to-stream-data-from-multiple-movella-dots-with-a-mac-and-python-afc388f62fa0
"""
import asyncio
from bleak import BleakScanner, BleakClient
import numpy as np

class XSConnect:
    def __init__(self, **kwargs) -> None:
        self.id = kwargs.get("id", None)
        self.short_payload_char_uuid = "15172004-4947-11e9-8646-d663bd873d93"
        self.measurement_char_uuid = "15172001-4947-11e9-8646-d663bd873d93"
        self.measurement_mode = kwargs.get("measurement_mode", "06")
        self.measurement_mode_string = b"\x01\x01\x06"

        # mm_bytearray = bytearray(self.measurement_mode_string)
        # mm_bytearray[2] = self.measurement_mode
        # self.measurement_mode_string = bytes(mm_bytearray)

        self.callback = kwargs.get("callback", None)

    async def get_devices(self):
        print("Searching for Movella devices...")
        ret = []
        devices = await BleakScanner.discover()
        for device in devices:
            if device.name != None:
                if "Movella" in device.name:
                    print(f"Found {len(ret) + 1} devices...")
                    ret.append(device.address)
        return ret
    
    def default_callback(self, sender, data):
        free_acceleration = self.encode_free_acceleration(data)[0]
        free_acceleration = str(free_acceleration)[1:-1]

        print(f"{self.id}: {free_acceleration}")

    def call_callback(self, sender, data):
        self.callback(self, sender, data)
    
    async def connect_device(self):
        async with BleakClient(self.id) as client:
            print(f"{client.address} connection state: {client.is_connected}")

            if self.callback == None:
                await client.start_notify(self.short_payload_char_uuid, self.default_callback)
            else:
                await client.start_notify(self.short_payload_char_uuid, self.call_callback)
            await client.write_gatt_char(self.measurement_char_uuid, self.measurement_mode_string)

            while True:
                await asyncio.sleep(1.0)

    def encode_free_acceleration(self, bytes_):
        data_segments = np.dtype([
            ('timestamp', np.uint32),
            ('x', np.float32),
            ('y', np.float32),
            ('z', np.float32),
            ('zero_padding', np.uint32)
            ])
        formatted_data = np.frombuffer(bytes_, dtype=data_segments)
        return formatted_data