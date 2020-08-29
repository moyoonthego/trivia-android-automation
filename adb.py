from ppadb.client import Client as AdbClient
from PIL import Image

def connect_device():
    adb = AdbClient(host="127.0.0.1", port=5037)
    adb.remote_connect("192.168.1.12", 5555)
    devices = adb.devices()

    if len(devices) == 0:
        print("No Devices Attached")
        quit()
    return devices[0]

def take_screenshot(device):
    image = device.screencap()
    with open('screen.png', 'wb') as f:
        f.write(image)