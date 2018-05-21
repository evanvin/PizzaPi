git clone https://github.com/evanvin/PizzaPi.git
sudo pip install tinydb spotipy beautifulsoup4 mutagen apscheduler youtube_dl musicbrainzngs style flask flask-cors
cd PizzaPi/
rm -rf dietpi.txt
cd downloader/
echo "SPOTIFY={'client_id':'{client_id}','client_secret':'{client_secret}','user':'{user}','playlist':'{playlist}'}" > config.py
