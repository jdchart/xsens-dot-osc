import xsens
import asyncio
import utils

# movella ids (found using the first example):
ids = ['862864A5-5BA3-690E-AFAB-F2BD319A1B44', '2F7BC272-B4C1-9972-593F-A156037F1712']

# create a callback function that will handle the data:
def callback_func(obj, sender, data):
    free_acceleration = utils.encode_free_acceleration(data)[0]
    free_acceleration = str(free_acceleration)[1:-1]
    print(f"{obj.id}: {free_acceleration}")

# create connector instance for each id:
devices = []
for id in ids:
    devices.append(xsens.XSConnect(id = id, callback = callback_func))

# connect to each device:
async def connect_all():
    await asyncio.gather(*(device.connect_device() for device in devices))
asyncio.run(connect_all())

# to quit, use ctrl+c