git clone https://github.com/evanvin/PizzaPi.git
sudo pip install tinydb spotipy beautifulsoup4 mutagen apscheduler youtube_dl musicbrainzngs style flask flask-cors

cd downloader/
echo "SPOTIFY={'client_id':'{client_id}','client_secret':'{client_secret}','user':'{user}','playlist':'{playlist}'}" > config.py
cd ../

cd storage/
npm install
cd src/Components/
hostname -I | awk '{print "module.exports = {IP:\x27"$1"\x27};"}' > ip.js
cd ../../../

rm -rf dietpi.txt
rm -rf Automation_Custom_Script.sh

python downloader/main.py &
python storage/dataservice.py &
npm start --prefix storage/
