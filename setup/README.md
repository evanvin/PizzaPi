### Setup

1.  Download [dietpi](https://dietpi.com) and mount to MicroSD card
2.  Plug MicroSD card back into computer, and copy the *dietpi.txt* file from this git repository into your MicroSD cards /boot folder (This will overwrite the *dietpi.txt* file that is already present)
3.  Copy the *Automation_Custom_Script.sh* file from this repository into your MicroSD cards /boot folder
4.  Edit the *config.py* file from this folder with your appropriate Spotify Web API information (client_id, client_secret, your username, and the name of the playlist(s) you wish this program to listen to and download. Save your changes. Then copy the file into your MicroSD cards /boot folder
    * The playlist property takes a list of strings. Or if you would like to download all songs from every playlist, set the playlist property to ['--all--']. **_You might see some files missing, but that has to do with Spotify's API not sending back up-to-date data for some users_**
5.  Safely eject the MicroSD card, and plug into your RPI/Other device. Plug in an ethernet cord, and power up the device and wait.
    1.  If you have an HDMI cable hooked up and are watching the auto-setup, then you will be able to see the IP address at the end of setup that you can SSH into.
    2.  OTHERWISE... If you are trying to do a headless install, you can run a simple 'arp -a' command from another computer on the same network and figure out which IP address is newer (most likely the RPI)

* **If you haven't used dietpi before, the default login credentials is root:dietpi**
