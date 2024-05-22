import xsens
import utils

# setup osc server
osc_server = xsens.OSCSender()
osc_server.start_server()

# create a callback function that will send data over osc:
def callback_func(obj, sender, data):
    free_acceleration = utils.encode_free_acceleration(data)[0]
    free_acceleration = str(free_acceleration)[1:-1]
    osc_server.send(f"/{obj.id}", free_acceleration.replace(",", ""))

# connect to devices:
utils.quick_connect(['862864A5-5BA3-690E-AFAB-F2BD319A1B44', '2F7BC272-B4C1-9972-593F-A156037F1712'], callback_func)