from subprocess import call
cmds = [
        'sudo add-apt-repository ppa:mc3man/trusty-media',
        'sudo apt-get update',
        'sudo apt-get install ffmpeg',
        'sudo apt install python-pip',
        'sudo pip install tinydb spotipy beautifulsoup4 mutagen apscheduler youtube_dl musicbrainzngs style gpiozero'
        ]

if __name__ == '__main__':
    for cmd in cmds:
        call(cmd)
