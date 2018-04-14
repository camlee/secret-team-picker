#!/usr/bin/env python3
import time
import argparse
from flask import Flask, request, abort, send_from_directory, render_template
from gevent.wsgi import WSGIServer

from game_definition import title, preference_options, assign

class GlobalState:
    player_data = {}
    started = False

app = Flask(__name__)

def get_player_key(request):
    return (request.remote_addr, request.environ.get('REMOTE_PORT'))

@app.context_processor
def inject():
    context = {
        "title": title,
        "preference_options": preference_options,
        "started": GlobalState.started
        }
    player_context = GlobalState.player_data.get(get_player_key(request), {})
    context.update(player_context)
    return context

@app.route("/", methods=["POST", "GET"])
def index():
    context = {}
    if request.method == "POST":
        if "submit" in request.form:
            data = GlobalState.player_data.setdefault(get_player_key(request), {})
            if not GlobalState.started:
                data["ip"] = request.remote_addr
                data["port"] = request.environ.get('REMOTE_PORT')
                data["name"] = request.form["name"]
                data["preference"] = request.form["preference"]
                data["message"] = 'You have selected: %s' % request.form["preference"]
            else:
                context["error_message"] = "The game has already started."
        elif "start" in request.form:
            if not GlobalState.started:
                GlobalState.started = True
                GlobalState.player_data = assign(GlobalState.player_data)
            else:
                context["error_message"] = "The game has already started."
        elif "end" in request.form:
            GlobalState.player_data = {}
            GlobalState.started = False

    if GlobalState.started:
        context["message"] = "The game has started."
    return render_template("index.html", **context)

@app.route("/players", methods=["GET"])
def players():
    if request.remote_addr not in ["localhost", "127.0.0.1", "::1"]:
        abort(404)

    return render_template("players.html", player_data=GlobalState.player_data)


@app.route("/favicon.ico")
def favicon():
    return send_from_directory("static", "favicon.ico")

@app.route("/static/<path:filename>")
def static_files(filename):
    return send_from_directory("static", filename)


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("-D", "--debug", action="store_true", default=False, help="Enable flask debug mode.")
    ap.add_argument("-H", "--host", type=str, default="localhost", help="Specify host to listen on.")
    ap.add_argument("-P", "--port", type=int, default=5000, help="Specify port to listen on.")
    args = ap.parse_args()

    server = WSGIServer((args.host, args.port), app)
    print(" Running on http://%s:%s/ (Press CTRL+C to quit)" % (args.host, args.port))
    try:
        server.serve_forever()
    except (KeyboardInterrupt, SystemExit):
        server.stop()
