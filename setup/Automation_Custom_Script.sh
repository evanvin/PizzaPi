git clone https://github.com/evanvin/PizzaPi.git
pip install tinydb spotipy beautifulsoup4 mutagen youtube_dl musicbrainzngs style flask flask-cors click

cd ~/PizzaPi/storage/
npm install
cd src/Components/
hostname -I | awk '{print "module.exports = {IP:\x27"$1"\x27};"}' > ip.js

cp /boot/config.py ~/PizzaPi/downloader

chmod +x ~/PizzaPi/setup/.boot
cp ~/PizzaPi/setup/pizza.service /etc/systemd/system/
systemctl enable pizza
systemctl start pizza
systemctl stop pizza

systemctl start pizza
