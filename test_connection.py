# TRYING
import time
from ppadb.client import Client
from PIL import Image
import numpy as np

# Table height/location: 718 - 1763 (1045 pixels) [talvez 717 1764]
# 4x4 first square location: 718 - 964 (245 pixels ~ 247)
# 4x4 separation size: 964 - 984 (20 pixels)

def connect_device() -> Client.device:
    """Return device connected"""
    adb = Client(host="127.0.0.1", port=5037)
    devices = adb.devices()

    if len(devices) == 0:
        print('No devices connected!')
        return None

    return devices[0]

def screen_to_array(dev) -> np.array:
    """Get screen from device and return in array of pixels
    Args:
        dev: connected device
    Returns:
        np.array: printscreen of device in arrays
    """
    temp_img = dev.screencap()

    with open('screen.png', 'wb') as img:
        img.write(temp_img)

    temp_img = Image.open('screen.png')
    return np.array(temp_img, dtype=np.uint8)

def get_table(arr: np.array, mode: int) -> np.array:
    """return array mode x mode
    Args:
        arr (np.array): table array of pixels
        mode (int): game mode (4, 6, 8, 10, 12)
    Returns:
        np.array: array n x n, n=mode
    """
    blue = np.array([0, 89, 190, 255])
    yellow = np.array([255, 213, 0, 255])
    empty = np.array([42, 42, 42, 255])

    if mode not in [4, 6, 8, 10, 12]:
        print('Invalid mode.')
        return None

    convert_dict = {
        4: {'coord': (136, 717+123), 'steps': (269, 267)}
    }

    table_game = np.zeros([mode, mode], dtype=np.uint8)

    values = convert_dict.get(mode)
    ini_x, ini_y = values.get('coord')
    x_step, y_step = values.get('steps')
    aux_x = aux_y = 0

    for i in range(mode):
        pixel_y = ini_y + (aux_y*y_step)

        for j in range(mode):
            pixel_x = ini_x + (aux_x*x_step)
            aux_x += 1

        aux_y += 1
        aux_x = 0
        print("\n")

    return table_game

if __name__=='__main__':
    # device = connect_device()
    device = "ND"
    if device is None:
        quit()

    while True:
        op = input("Game mode (4, 6, 8, 10, 12): ")
        op = 0 if not op.isnumeric() else int(op)

        if op not in [4, 6, 8, 10, 12]:
            print("Game mode invalid. Try again!")
            continue
        break

    image = Image.open('screen.png')
    image = np.array(image, dtype=np.uint8)
    # image = screen_to_array(device)
    # print(image[718:1763])

    print(image[718,1000])

    # with open('screen.txt', 'w') as tfile:
    #     for i in image[840]:  # one square
    #         for j in i:
    #             tfile.write(str(j))
    #             tfile.write(' ')
    #         tfile.write('\n')

    # for i in image[718:1763][50]:
    #     print(i,"/")
        # for j in i[50]:
        #     print(j,"/")

    table = get_table(image, op)

    if table is None:
        quit()

# device.shell("input tap 950 1640")
# time.sleep(0.010)
# device.shell("input tap 950 1640")
