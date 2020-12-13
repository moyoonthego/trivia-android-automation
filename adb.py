from ppadb.client import Client as AdbClient
from PIL import Image

# connect device via USB, on same network
# adb kill-server
# adb tcpip 5555
# adb connect 192.168.1.7:5555

def connect_device():
    adb = AdbClient(host="127.0.0.1", port=5037)
<<<<<<< Updated upstream
    adb.remote_connect("192.168.1.21", 5555)
=======
    adb.remote_connect("192.168.1.7", 5555)
>>>>>>> Stashed changes
    devices = adb.devices()

    if len(devices) == 0:
        print("No Devices Attached")
        quit()
    return devices[0]

def take_screenshot(device):
    image = device.screencap()
    with open('screen.png', 'wb') as f:
        f.write(image)