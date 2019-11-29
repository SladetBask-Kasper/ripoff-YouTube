from flask import Flask, escape, request, render_template, Markup
import re, os

VIDEOS_FOLDER = "static/videos"
FILE_IO_ERROR = "UNABLETOREADFILEFILEIOERROR"

app = Flask(__name__)

def getFile(filename):
    if os.path.exists(filename):
        f = open(filename, "r")
        return str(f.read())
    else:
        return FILE_IO_ERROR
@app.route('/')
@app.route('/index')
def index():
    i = 0
    html = ""
    while True:
        meta = getFile(f"{VIDEOS_FOLDER}/id{i}/meta.txt")
        if meta == FILE_IO_ERROR:
            break
        else:
            result = re.search('TITLE : (.*)\n', meta)
            title = result.group(1)
            # <img src="" alt="" width="5%" height="5%">
            src = "/static/videos/id"+str(i)+"/thumbnail.png"
            alt = f"Video ID${i} thumbnail"
            width = "256"
            height = width
            html += f'<div class="vidItem"><a href="play?id={i}"><img src={src} alt="{alt}" width="{width}" height="{height}">{title}</a></div>'
        i += 1
    return render_template("index.html", videos=Markup(html))

@app.route('/play')
def play():
    id = "id" + str(request.args.get('id'))
    return render_template("play.html", id=id)
app.run(host='0.0.0.0', debug=True, port=80)
