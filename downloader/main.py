# -*- coding: utf-8 -*
from __future__ import unicode_literals
import logging, os, re, urllib, urllib2, glob, style, time, click
import spotipy, youtube_dl, mutagen, musicbrainzngs

from tinydb import TinyDB, Query
from bs4 import BeautifulSoup
from subprocess import call
from spotipy.oauth2 import SpotifyClientCredentials
from mutagen.easyid3 import EasyID3
from config import SPOTIFY

try:
    import RPi.GPIO as GPIO
except Exception as e:
    

client_credentials_manager = None
sp = None

def getTrackString(t, playlist_dir):
    if 'track' in t:
        track = t['track']
        # Strip out and clean the track title, artist, and cover image
        try:
            recording = clean(track['name'])
            artist = clean(track['artists'][0]['name'])
            cover = track['album']['images']
            cover = (cover[1] if 1 < len(cover) else cover[0])['url']
            return {'recording': recording, 'artist': artist, 'cover': cover, 'playlist_dir': playlist_dir}
        except Exception as e:
            error('There was an error with {} when getting the track string for track {}'.format(e, track))
    else:
        error('There was no track attribute in {}.'.format(t))

    return None


def getPlaylistInfo():
    try:
        GREEN = 16
        GPIO.setwarnings(False)
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(GREEN, GPIO.OUT)
        GPIO.output(GREEN, True)    
    except Exception as e:
        print e
        
    # Get start time
    start_time = time.time()

    # Get Spotify user and selected playlists from config file
    if 'user' in SPOTIFY and 'playlist' in SPOTIFY:
        user = SPOTIFY['user']
        selected_playlists = SPOTIFY['playlist']

        # Retrieve all user playlists from Spotify
        all_playlists = sp.user_playlists(user)

        # Select all playlists if the first option in the playlist config list is --all--
        # Otherwise, list comprehension get all playlists that match playlists in config list
        playlists = all_playlists['items'] if selected_playlists[0] == '--all--' else [d for d in all_playlists['items'] if d['name'] in selected_playlists]

        if len(playlists) > 0:
            # Create download directory if not exists
            if not os.path.exists('downloads/'):
                os.mkdir('downloads')

            # Create or Open existing tracks table in flat file
            # Create a TinyDB Query object
            table = TinyDB('../storage/db.json').table('tracks')
            track_query = Query()


            # Loop through all playlists
            for playlist in playlists:
                if 'id' in playlist:
                    if 'name' in playlist:
                        # Create playlist directory in download folder if not exists
                        playlist_dir = 'downloads/' + playlist['name']
                        if not os.path.exists(playlist_dir):
                            os.mkdir(playlist_dir)

                        # Retrieve list of tracks in current playlist
                        tracks = sp.user_playlist_tracks(user, playlist['id'])

                        # Strip out the necessary track information from the playlist tracks
                        track_info = [t for t in [getTrackString(i, playlist_dir) for i in tracks['items']] if t is not None]

                        # Loop through the clean track list and check the flat file to see if any of the cleaned tracks have already been added
                        tracks_to_download = []
                        for ti in track_info:
                            # If recording/playlist is not in flat file already, add it to a list of tracks to download
                            if not table.search((track_query.recording == ti['recording']) & (track_query.playlist_dir == playlist_dir)):
                                tracks_to_download.append(ti)

                        # Size of tracks_to_download
                        ttd_len = len(tracks_to_download)

                        # Print out information about how many tracks were found vs. how many have not been downloaded yet
                        print(style.light_green(style.italic.bold(playlist['name']), '- Found', style.italic.bold(str(len(track_info))), 'total tracks for playlist.',
                            style.italic.bold(str(ttd_len)), 'of them are new and will be downloaded now.\n'))

                        # Get YouTube links for the tracks
                        getLinks(tracks_to_download)
                    else:
                        error('There was no name provided from Spotify for that users playlist.')
                else:
                    error('There was no id provided from Spotify for that users playlist.')
        else:
            error(style.red('Could not find playlist,', style.bold(selected_playlists) + ', for spotify user,', style.bold(user)))

        print(style.light_green('Process done.'))
    else:
        error('There was and issue with the user or playlist provided in the config file. Please check config.py for issues.')

    # This process should run one hour after it started
    # Get elapsed time since start of download process
    elapsed_time = time.time() - start_time

    # Calculate how much time process needs to sleep for so it starts again after one hour from the start
    time_left = 3600 - elapsed_time
    time_left = time_left if time_left >= 0 else 0

    # Sleep and then call itself to run again
    time.sleep(time_left)
    GPIO.cleanup()
    getPlaylistInfo()


def getLinks(tracks):
    vids = []
    if len(tracks) > 0:
        step('Finding links for {} tracks...'.format(len(tracks)))

        # Loop through the tracks to figure out their YouTube video link
        with click.progressbar(tracks, length=len(tracks), show_pos=True, show_eta=True, fill_char='█', empty_char=' ') as bar:
            for t in bar:
                # Create filename
                filename = (t['recording'] + ' ~~ ' + t['artist'])

                # Build the search query URL for youtube
                url = filename.encode('utf-8')
                query = urllib.quote( url )
                url = "https://www.youtube.com/results?search_query=" + query
                response = urllib2.urlopen(url)

                # Retrieve and parse the HTML from search query URL to find the YouTube link
                html = response.read()
                soup = BeautifulSoup(html, "html.parser")
                vid = soup.findAll(attrs={'class':'yt-uix-tile-link'})[0]

                # Add the information to a running list
                vids.append( {"filename": filename, "link": 'https://www.youtube.com' + vid['href'], 'track_info': t} )

        step('{} links found. Starting the download process...\n'.format(len(vids)))

        # Send the link list to be downloaded
        download(vids)


def download(links):
    # Loop through the links and download each one
    for l in links:
        print(style.light_yellow.on_magenta.italic(l['filename']))
        step('\tStarting download...')

        # Create the output file structure
        opt = {'outtmpl' : l['track_info']['playlist_dir'] + '/' + l['filename'] + '.%(ext)s', 'quiet': True, 'no_warnings': True}

        # Download the link
        youtube_dl.YoutubeDL(opt).download([l['link']])
        step('\tDownload complete. Starting conversion...')

        # After download is complete, convert the video file to an MP3
        convert(l)

def convert(l):
    # Instantiate the playlist directory path and full filename path
    pth = l['track_info']['playlist_dir'] + '/'
    fn = pth + l['filename']

    # Find the input video file
    input = glob.glob(fn + '.*')
    if len(input) > 0:
        input = input[0]

        # Create the output file path and name
        output =  fn + ".mp3"

        # Execute a FFMPEG video-to-mp3 conversion
        call(['ffmpeg', '-loglevel', 'quiet', '-i', input, '-f', 'mp3', output])
        step('\tConversion done.')

        # Delete the original video file
        os.remove(input)

        # Rename the converted MP3 file to the tracks title name
        new_output = pth + l['track_info']['recording'] + '.mp3'
        os.rename(output, new_output)
        l['filename'] = new_output

        # Search and update the ID3 tags for the song
        tag(l)
    else:
        error('\tThere was no input video file found with basename: {}'.format(fn))



def tag(t):
    # Search MusicBrainz for information on the track
    result = musicbrainzngs.search_recordings(artist=t['track_info']['artist'], recording=t['track_info']['recording'], limit=1)
    step('\tStarting to tag...')

    # Check if there are any results
    if 'recording-list' in result and len(result['recording-list']) > 0:
        r = result['recording-list'][0]

        try:
            # Create the ID3 object
            tags = EasyID3(t['filename'])

            # Start checking and updating the ID3 tags for the track
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

            # Save the tags
            tags.save(t['filename'])

            # Insert this track information into the flat file
            table = TinyDB('../storage/db.json').table('tracks')
            table.insert(t['track_info'])
        except Exception as e:
            error('\t\tThere was an error during the editing of ID3 tags. Error message: {}'.format(e))
    else:
        error('\t\tNo recording-list attribute found in musicbrainz search results.')
    step('\tTagging done.\n')

# Removes any parentheses from a string
def clean(s):
    return re.sub(r'\(.*?\)', '', s)

# Prints out a styled message for errors
def error(e):
    print(style.light_red.italic(e))


# Prints out a styled message for steps in the process
def step(s):
    print(style.light_cyan(s))

if __name__ == '__main__':
    # Check for correct config properties
    if 'client_id' in SPOTIFY and 'client_secret' in SPOTIFY:
        # Setup authentication for Spotify API
        client_credentials_manager = SpotifyClientCredentials(client_id=SPOTIFY['client_id'], client_secret=SPOTIFY['client_secret'])
        sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager)

        # Setup user agent for MusicBrainz API
        musicbrainzngs.set_useragent(
            "python-musicbrainzngs-example",
            "0.1",
            "https://github.com/alastair/python-musicbrainzngs/",
        )

        # Start the download/tagging process
        getPlaylistInfo()
    else:
        error('There was and issue with the client id or secret provided in the config file. Please check config.py for issues.')
