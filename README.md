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
* [Usage](#usage)
  * [Downloader](#downloader)
  * [USB Transfer](#usb)

---

### Setup

Please navigate to [setup](https://github.com/evanvin/PizzaPi/tree/master/setup) folder in this project

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
* [ ] Add log files for processes
