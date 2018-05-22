import os, glob, shutil
import time

USB = '/media/eevinciguerra/'
DOWNLOAD = 'downloads/'

def checkUSB():
    disks = [dI for dI in os.listdir(USB) if os.path.isdir(os.path.join(USB,dI))]
    for d in disks:
        usb_pizza = USB + d + '/pizza/'
        if os.path.exists(usb_pizza):
            downloaded = [g.replace(DOWNLOAD, "") for g in glob.glob(DOWNLOAD + '*.mp3')]
            pizzas = [g.replace(usb_pizza, "") for g in glob.glob(usb_pizza + '*.mp3')]
            need_to_move = list(set(downloaded) - set(pizzas))
            for f in need_to_move:
                shutil.copy(DOWNLOAD+f, usb_pizza)
            os.system('sudo eject "' + USB+d + '"')
    time.sleep(5)
    checkUSB()


if __name__ == '__main__':
    checkUSB()
