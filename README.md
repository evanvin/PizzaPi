# PizzaPi

### Features

* Automatically download songs from a spotify playlist (most likely a Shazam connected playlist)
* Transfer of .mp3 files to a USB plugged into a RPI that contains a folder with a specific name
* ~~A web interface for file management~~ Not yet perfected

### Setup

1. Download dietpi and mount to MicroSD card
2. Plug MicroSD card back into computer, and copy the 'dietpi.txt' file from this git repository into your MicroSD cards /boot folder (This will overwrite the 'dietpi.txt' file that is already present
3. Also, copy the 'Automation_Custom_Script.sh' file from this repository into your MicroSD cards /boot folder
4. Open the 'Automation_Custom_Script.sh' file you just copied into the /boot folder, and edit line 4 with your appropriate Spotify Web API information (client_id, client_secret, your username, and the name of the playlist you wish this program to listen to and download. Save your changes.
5. Safely eject the MicroSD card, and plug into your RPI/Other device. Plug in an ethernet cord, and power up the device and wait.

- If you have an HDMI cable hooked up and are watching the auto-setup, then you will be able to see the IP address at the end of setup that you can SSH into.
- OTHERWISE... If you are trying to do a headless install, you can run a simple 'arp -a' command from another computer on the same network and figure out which IP address is newer (most likely the RPI)

* **If you haven't used dietpi before, the default login credentials is root:dietpi**

### Todo

* Allow user to input mutliple playlists
