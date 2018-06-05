git clone https://github.com/evanvin/PizzaPi.git
sudo pip install tinydb spotipy beautifulsoup4 mutagen youtube_dl musicbrainzngs style flask flask-cors click

cd ~/PizzaPi/storage/
npm install
cd src/Components/
hostname -I | awk '{print "module.exports = {IP:\x27"$1"\x27};"}' > ip.js

cd ~/PizzaPi/downloader/
cp /boot/config.py ~/PizzaPi/downloader

sudo chmod 774 ~/PizzaPi/setup/boot.sh
cp ~/PizzaPi/setup/pizza.service /etc/systemd/system/
sudo chmod 664 /etc/systemd/system/pizza.service
systemctl daemon-reload
systemctl enable pizza.service

cd ~/PizzaPi/downloader/
python python usb.py & main.py
