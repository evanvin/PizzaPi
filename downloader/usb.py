import os, shutil, time, style

try:
    from gpiozero import LED
    red = LED(35)
    green = LED(47)
    les_loaded = True
except Exception as e:
    leds_loaded = False
    print(style.light_red.italic('Error importing gpiozero!'))

USB = '/media/'
DOWNLOAD = 'downloads/'

def checkUSB():
    # Find all directories in media folder (USB's)
    disks = [dI for dI in os.listdir(USB) if os.path.isdir(os.path.join(USB,dI))]

    # Loop through all the directories
    for d in disks:
        # Find out if any of the directories have a folder named 'pizza'
        usb_pizza = USB + d + '/pizza/'
        if os.path.exists(usb_pizza):
            # If LED is possible, start blinking the green on-board LED
            if leds_loaded:
                green.blink(0.5, 0.5)

            # Find all directories in download folder from the SBC, and pizza folder from the USB
            download_folders = next(os.walk(DOWNLOAD + '.'))[1]
            pizza_folders = next(os.walk(usb_pizza + '.'))[1]
            # Find the difference between download_folders and pizza_folders
            folders_needed = list(set(download_folders) - set(pizza_folders))

            # Loop through new directories and files and copy them to the USB
            for d in folders_needed:
                shutil.copy(DOWNLOAD + d, usb_pizza + d)

            # Loop through pizza folders and update their contents
            for d in download_folders:
                # Find all files in each directory from the SBC, and from the USB
                downloaded = next(os.walk(DOWNLOAD + d + '/.'))[2]
                pizzas = next(os.walk(usb_pizza + d + '/.'))[2]
                # Find the dfference between downloaded and pizzas
                need_to_move = list(set(downloaded) - set(pizzas))

                # Loop through the files and copy them over to their respective directory on the USB
                for f in need_to_move:
                    shutil.copy(DOWNLOAD + d + '/' + f, usb_pizza + d + '/')

                # Attempt to eject the USB device
                os.system('sudo eject "' + USB + d + '"')

            # If LED is possible, turn off the green on-board LED
            if leds_loaded:
                green.off()

    # The check/transfer is over, so we sleep for 5 seconds and check again to see if a USB has been inserted into the SBC
    time.sleep(5)
    checkUSB()


# Run the check process at start
if __name__ == '__main__':
    checkUSB()
