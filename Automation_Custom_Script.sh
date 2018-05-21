git clone https://github.com/evanvin/PizzaPi.git
sudo pip install tinydb spotipy beautifulsoup4 mutagen apscheduler youtube_dl musicbrainzngs style
cd PizzaPi/downloader
echo "SPOTIFY={'client_id':'94d6737b743e469fa8d190ae0899c317','client_secret':'0ee3084d44a94814a1270115f731e601','user':'zaaking','playlist':'My Shazam Tracks'}" > config.py
