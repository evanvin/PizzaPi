git clone https://github.com/evanvin/PizzaPi.git
sudo pip install tinydb spotipy beautifulsoup4 mutagen youtube_dl musicbrainzngs style flask flask-cors click

cd PizzaPi/storage/
npm install
cd src/Components/
hostname -I | awk '{print "module.exports = {IP:\x27"$1"\x27};"}' > ip.js

cd ~/PizzaPi/downloader/
cp /boot/config.py ~/PizzaPi/downloader

python python usb.py & main.py
