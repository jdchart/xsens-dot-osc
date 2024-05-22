import numpy as np
import xsens
import asyncio

def encode_free_acceleration(bytes_):
    data_segments = np.dtype([
        ('timestamp', np.uint32),
        ('x', np.float32),
        ('y', np.float32),
        ('z', np.float32),
        ('zero_padding', np.uint32)
        ])
    formatted_data = np.frombuffer(bytes_, dtype=data_segments)
    return formatted_data

def quick_connect(ids, callback):
    devices = []
    for id in ids:
        devices.append(xsens.XSConnect(id = id, callback = callback))
    async def connect_all():
        await asyncio.gather(*(device.connect_device() for device in devices))
    asyncio.run(connect_all())