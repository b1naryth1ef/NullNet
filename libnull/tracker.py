from flask import Flask, jsonify, request

from libnull.db import DB

app = Flask(__name__)

# Change this later
GLOB_HASH = "f12ac849dd89417d8241ff362018793a"
db = DB(GLOB_HASH)

try:
    db.create()
except: pass

@app.route("/")
def stats_route():
    print request.values.items()
    # return jsonify({
    #         "globhash": GLOB_HASH,
    #         "num_articles": db.get_num_articles(),
    #         "num_peers": db.get_num_peers()
    #     })

@app.route("/post", methods=["POST"])
def post_route():
    print request.values.items()
    return "", 200

@app.route("/announce")
def announce_route():
    print request.values.items()
    return db.get_peers(request.values.get("info_hash"), count=request.values.get("num_want"), compact=bool(int(request.values.get("compact"))))

@app.route("/scrape")
def scrape_route():
    return "", 200
