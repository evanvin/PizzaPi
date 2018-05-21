from flask import Flask
from flask import jsonify
from flask import send_file
from flask import request as req
from flask_cors import CORS
import os
from tinydb import TinyDB

app = Flask(__name__)
CORS(app)


@app.route("/tracks", methods=["GET"])
def tracks():
    if os.path.exists('downloader/downloads/'):
        table = TinyDB('downloader/downloads/done.json').table('tracks')
        data = table.all()
    else:
        data = None

    return jsonify(data)


@app.route("/download", methods=['GET'])
def download():
    recording = req.args.get('recording')
    fl = 'downloader/downloads/music/' + recording + '.mp3'
    print fl
    return send_file(fl, mimetype="audio/mp3", attachment_filename=(recording + '.mp3'), as_attachment=True)


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=8008)
