<h1 align="center">
  <br>
  <img src="https://github.com/evanvin/PizzaPi/blob/master/PizzaPi.png" alt="PizzaPi" width="250">
  <br>
  PizzaPi
</h1>

## Features

* Automatically download songs from spotify playlist(s) (most likely a Shazam connected playlist)
* Transfer of .mp3 files to a USB plugged into a RPI that contains a folder with a specific name
* ~~A web interface for file management~~ Not yet perfected

## Table of Contents

* [Setup](#setup)
* [Tools](#tools)
* [Usage](#usage)
  * [Downloader](#downloader)
  * [USB Transfer](#usb)

---

### Setup

1.  Download [dietpi](https://dietpi.com) and mount to MicroSD card
2.  Plug MicroSD card back into computer, and copy the 'dietpi.txt' file from this git repository into your MicroSD cards /boot folder (This will overwrite the 'dietpi.txt' file that is already present)
3.  Also, copy the 'Automation_Custom_Script.sh' file from this repository into your MicroSD cards /boot folder
4.  Open the 'Automation_Custom_Script.sh' file you just copied into the /boot folder, and edit line 15 with your appropriate Spotify Web API information (client_id, client_secret, your username, and the name of the playlist(s) you wish this program to listen to and download. Save your changes.
    * The playlist property takes a list of strings. Or if you would like to download all songs from every playlist, set the playlist property to ['--all--']. **_You might see some files missing, but that has to do with Spotify's API not sending back up-to-date data for some users_**
5.  Safely eject the MicroSD card, and plug into your RPI/Other device. Plug in an ethernet cord, and power up the device and wait.
    1.  If you have an HDMI cable hooked up and are watching the auto-setup, then you will be able to see the IP address at the end of setup that you can SSH into.
    2.  OTHERWISE... If you are trying to do a headless install, you can run a simple 'arp -a' command from another computer on the same network and figure out which IP address is newer (most likely the RPI)

* **If you haven't used dietpi before, the default login credentials is root:dietpi**

---

## Usage

### Downloader

Once the setup is done, the auto-downloader should start. This will check the specified spotify playlist(s) for new songs to download, and download them automatically and update their ID3 metadata.

### USB

You should be able to insert an USB device into the RPI device and it will automatically copy over any already downloaded songs that have not been copied over to your USB yet.

> **_\* USB drive must have a folder titled 'pizza' for auto transfer to work_**

---

### Todo

* [x] Allow user to input mutliple playlists
* [x] Organize tracks into playlist-specific folders
* [ ] Refactor code
* [x] Comment code
* [ ] Figure out multithreading for downloader and web interface and flask server
* [ ] Hijack the onboard RPI green light to show that USB transfer is in process
* [ ] Add code for potential GPIO button press to trigger a download refresh
* [ ] Add option to startup script to send the IP address to a provided email address
* [ ] Add way for user to update persisted Spotify configuration after initial setup
* [ ] Make config file placeable in the dietpi boot folder
* [ ] Create post-first-time-boot startup script
