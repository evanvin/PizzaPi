from __future__ import unicode_literals
import logging, os, re, urllib, urllib2, glob, style
import spotipy, youtube_dl, mutagen, musicbrainzngs

from tinydb import TinyDB, Query
from bs4 import BeautifulSoup
from subprocess import call
from spotipy.oauth2 import SpotifyClientCredentials
from mutagen.easyid3 import EasyID3
from apscheduler.schedulers.blocking import BlockingScheduler
from config import SPOTIFY

sched = None
client_credentials_manager = None
sp = None

def getTrackString(t):
    if 'track' in t:
        track = t['track']
        try:

            recording = clean(track['name'])
            artist = clean(track['artists'][0]['name'])
            cover = track['album']['images']
            cover = (cover[1] if 1 < len(cover) else cover[0])['url']
            return {'recording': recording, 'artist': artist, 'cover': cover}
        except Exception as e:
            error('There was an error with {} when getting the track string for track {}'.format(e, track))
    else:
        error('There was no track attribute in {}.'.format(t))

    return None


def getPlaylistInfo():
    # create folder and flat file if not exists
    if not os.path.exists('downloads/'):
        os.mkdir('downloads')

    table = TinyDB('../storage/db.json').table('tracks')
    Track = Query()

    spotifyUser = SPOTIFY['user']
    spotifyPlaylist = SPOTIFY['playlist']

    playlists = sp.user_playlists(spotifyUser)
    shazam = [d for d in playlists['items'] if d['name'] == spotifyPlaylist]

    if len(shazam) > 0:
        shazam = shazam[0]
        if 'id' in shazam:
            tracks = sp.user_playlist_tracks(spotifyUser, shazam['id'])
            trackInfo = [t for t in [getTrackString(i) for i in tracks['items']] if t is not None]

            tracks_to_download = []
            for ti in trackInfo:
                if not table.search(Track.recording == ti['recording']):
                    tracks_to_download.append(ti)

            ttd_len = len(tracks_to_download)

            print(style.light_green('Found', style.italic.bold(str(len(trackInfo))), 'total tracks.',
                style.italic.bold(str(ttd_len)), 'of them are new and will be downloaded now.\n'))
            getLinks(tracks_to_download)
        else:
            error('There was no id provided from Spotify for that users playlist.')
    else:
        error(style.red('Could not find playlist,', style.bold(spotifyPlaylist) + ', for spotify user,', style.bold(spotifyUser)))

    print(style.light_green('Process done.'))
    if sched is not None:
        sched.remove_job('curr_job')


def getLinks(tracks):
    vids = []
    if len(tracks) > 1:
        step('Finding links for {} tracks...'.format(len(tracks)))
        for t in tracks:
            filename = (t['recording'] + ' ~~ ' + t['artist'])
            query = urllib.quote( filename )
            url = "https://www.youtube.com/results?search_query=" + query
            response = urllib2.urlopen(url)
            html = response.read()
            soup = BeautifulSoup(html, "html.parser")
            vid = soup.findAll(attrs={'class':'yt-uix-tile-link'})[0]
            vids.append( {"filename": filename, "link": 'https://www.youtube.com' + vid['href'], 'trackInfo': t} )
        step('{} links found. Starting the download process...\n'.format(len(vids)))
        download(vids)


def download(links):
    for l in links:
        print(style.light_yellow.on_blue.italic(l['filename']))
        step('\tStarting download...')
        opt = {'outtmpl' : 'downloads/' + l['filename'] + '.%(ext)s', 'quiet': True, 'no_warnings': True}
        youtube_dl.YoutubeDL(opt).download([l['link']])
        step('\tDownload complete. Starting conversion...')
        convert(l)

def convert(l):
    pth = 'downloads/'
    fn = pth + l['filename']

    input = glob.glob(fn + '.*')
    if len(input) > 0:
        input = input[0]
        output =  fn + ".mp3"
        call(['ffmpeg', '-loglevel', 'quiet', '-i', input, '-f', 'mp3', output])

        step('\tConversion done.')
        os.remove(input)
        newOutput = pth + l['trackInfo']['recording'] + '.mp3'
        os.rename(output, newOutput)
        l['filename'] = newOutput
        tag(l)
    else:
        error('\tThere was no input video file found with basename: {}'.format(fn))



def tag(t):
    result = musicbrainzngs.search_recordings(artist=t['trackInfo']['artist'], recording=t['trackInfo']['recording'], limit=1)
    step('\tStarting to tag...')
    if 'recording-list' in result and len(result['recording-list']) > 0:
        r = result['recording-list'][0]

        try:
            tags = EasyID3(t['filename'])

            if 'title' in r:
                tags['title'] = r['title']
            else:
                error('\t\tNo title name found for track.')

            if 'artist-credit-phrase' in r:
                tags['artist'] = r['artist-credit-phrase']
            else:
                error('\t\tNo artist name found for track.')

            if 'release-list' in r and len(r['release-list']) > 0:
                rl = r['release-list'][0]
                if 'title' in rl:
                    tags['album'] = rl['title']
                else:
                    error('\t\tNo album name found for track.')

                if 'date' in rl:
                    tags['date'] = rl['date']
                else:
                    error('\t\tNo release date found for track.')
            else:
                error('\t\tNo release-list attribute found for track.')

            if 'tag-list' in r:
                tags['genre'] = ', '.join([i['name'] for i in r['tag-list'] if i['count'] > 0])
            else:
                error('\t\tNo genres found for track.')


            tags.save(t['filename'])
            table = TinyDB('../storage/db.json').table('tracks')
            table.insert(t['trackInfo'])
        except Exception as e:
            error('\t\tThere was an error during the editing of ID3 tags. Error message: {}'.format(e))
    else:
        error('\t\tNo recording-list attribute found in musicbrainz search results.')
    step('\tTagging done.\n')

def clean(s):
    return re.sub(r'\(.*?\)', '', s)

def error(e):
    print(style.light_red.italic(e))

def step(s):
    print(style.cyan(s))

def startSchedule():
    log = logging.getLogger('apscheduler.executors.default')
    log.setLevel(logging.INFO)
    fmt = logging.Formatter('Scheduled Job (%(asctime)s)')
    h = logging.StreamHandler()
    h.setFormatter(fmt)
    log.addHandler(h)

    sched = BlockingScheduler()
    sched.add_job(getPlaylistInfo, 'interval', seconds=10, id='curr_job')#hours=1)
    sched.start()


if __name__ == '__main__':
    client_credentials_manager = SpotifyClientCredentials(client_id=SPOTIFY['client_id'], client_secret=SPOTIFY['client_secret'])
    sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager)
    musicbrainzngs.set_useragent(
        "python-musicbrainzngs-example",
        "0.1",
        "https://github.com/alastair/python-musicbrainzngs/",
    )

    getPlaylistInfo()
    startSchedule()
