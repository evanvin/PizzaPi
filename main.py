from __future__ import unicode_literals
import spotipy, logging, os, re, urllib, urllib2, youtube_dl, glob, musicbrainzngs, style

from tinydb import TinyDB, Query
from bs4 import BeautifulSoup
from subprocess import call
from spotipy.oauth2 import SpotifyClientCredentials
from mutagen.easyid3 import EasyID3
from apscheduler.schedulers.blocking import BlockingScheduler

client_credentials_manager = SpotifyClientCredentials(client_id='94d6737b743e469fa8d190ae0899c317', client_secret='0ee3084d44a94814a1270115f731e601')
sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager)
musicbrainzngs.set_useragent(
    "python-musicbrainzngs-example",
    "0.1",
    "https://github.com/alastair/python-musicbrainzngs/",
)


def getTrackString(t):
    try:
        track = t['track']
        recording = clean(track['name'])
        artist = clean(track['artists'][0]['name'])
        cover = track['album']['images']
        cover = (cover[1] if 1 < len(cover) else cover[0])['url']
        return {'recording': recording, 'artist': artist, 'cover': cover}
    except Exception as e:
        print(style.red(e))


def getPlaylistInfo():
    # create folder and flat file if not exists
    if not os.path.exists('downloads/'):
        os.mkdir('downloads')
        os.mkdir('downloads/music')

    table = TinyDB('downloads/done.json').table('tracks')
    Track = Query()

    playlists = sp.user_playlists('zaaking')
    shazam = [d for d in playlists['items'] if d['name'] == 'My Shazam Tracks'][0]

    tracks = sp.user_playlist_tracks('zaaking', shazam['id'])
    trackInfo = [getTrackString(i) for i in tracks['items']]

    tracks_to_download = []
    for ti in trackInfo:
        if not table.search(Track.recording == ti['recording']):
            tracks_to_download.append(ti)

    print(style.green('Found {} total tracks. {} of them are new to download.'.format(len(trackInfo), len(tracks_to_download))))
    getLinks(tracks_to_download)


def getLinks(tracks):
    vids = []
    for t in tracks:
        filename = (t['recording'] + ' ~~ ' + t['artist'])
        query = urllib.quote( filename )
        url = "https://www.youtube.com/results?search_query=" + query
        response = urllib2.urlopen(url)
        html = response.read()
        soup = BeautifulSoup(html, "html.parser")
        vid = soup.findAll(attrs={'class':'yt-uix-tile-link'})[0]
        vids.append( {"filename": filename, "link": 'https://www.youtube.com' + vid['href'], 'trackInfo': t} )
    download(vids)


def download(links):
    for l in links:
        print(style.blue(l['filename']))
        print(style.yellow('\tStarting download...'))
        opt = {'outtmpl' : 'downloads/music/' + l['filename'] + '.%(ext)s', 'quiet': True, 'no_warnings': True}
        youtube_dl.YoutubeDL(opt).download([l['link']])
        print(style.yellow('\tDownload complete. Starting conversion...'))
        convert(l)

def convert(l):
    pth = 'downloads/music/'
    fn = pth + l['filename']
    input = glob.glob(fn + '.*')[0]
    output =  fn + ".mp3"
    call(['ffmpeg', '-loglevel', 'quiet', '-i', input, '-f', 'mp3', output])

    print(style.yellow('\tConversion done for ' + l['filename']))
    os.remove(input)
    newOutput = pth + l['trackInfo']['recording'] + '.mp3'
    os.rename(output, newOutput)
    l['filename'] = newOutput
    tag(l)



def tag(t):
    result = musicbrainzngs.search_recordings(artist=t['trackInfo']['artist'], recording=t['trackInfo']['recording'], limit=1)
    r = result['recording-list'][0]

    try:
        tags = EasyID3(t['filename'])

        if 'title' in r:
            tags['title'] = r['title']

        if 'artist-credit-phrase' in r:
            tags['artist'] = r['artist-credit-phrase']

        if 'release-list' in r and len(r['release-list']) > 0:
            rl = r['release-list'][0]
            if 'title' in rl:
                tags['album'] = rl['title']

            if 'date' in rl:
                tags['date'] = rl['date']

        if 'tag-list' in r:
            tags['genre'] = ', '.join([i['name'] for i in r['tag-list'] if i['count'] > 0])


        tags.save(t['filename'])
        table = TinyDB('downloads/done.json').table('tracks')
        table.insert(t['trackInfo'])
    except Exception as e:
        print(style.red(e))

def checkProps(r, prop):
    return r[prop] if prop in r else ''

def clean(s):
    return re.sub(r'\(.*?\)', '', s)



def startSchedule():
    log = logging.getLogger('apscheduler.executors.default')
    log.setLevel(logging.INFO)
    fmt = logging.Formatter('Scheduled Job (%(asctime)s)')
    h = logging.StreamHandler()
    h.setFormatter(fmt)
    log.addHandler(h)

    sched = BlockingScheduler()
    sched.add_job(getPlaylistInfo, 'interval', hours=1)
    sched.start()


if __name__ == '__main__':
    getPlaylistInfo()
    startSchedule()
