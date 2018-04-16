#!/usr/bin/env
import os
import time
import secrets
import argparse
from flask import Flask, request, session, abort, send_from_directory, render_template
from gevent.wsgi import WSGIServer

from game_definition import get_game

class GlobalState:
    player_data = {}
    started = False
    game = get_game(os.environ.get('SECRET_TEAM_PICKER_GAME','DefaultGame'))()
    player_keys = set()

app = Flask(__name__)
app.secret_key = secrets.token_hex(16)

def generate_session_id():
    player_key = None
    key_length = 2
    while not player_key or player_key in GlobalState.player_keys:
        player_key = secrets.token_hex(key_length)
        key_length += 1 # Just in case we exhaust all permutations of the default key length

    GlobalState.player_keys.add(player_key)
    return player_key

def get_player_key(request):
    if "id" not in session:
        session["id"] = generate_session_id()

    return session["id"]

@app.context_processor
def inject():
    context = {
        "title": GlobalState.game.title,
        "preference_options": GlobalState.game.preference_options,
        "started": GlobalState.started
        }
    player_context = GlobalState.player_data.get(get_player_key(request), {})
    context["player"] = player_context
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
                data["message"] = 'You have selected: %s.' % data["preference"]
            else:
                context["error_message"] = "The game has already started."
        elif "quit" in request.form:
            GlobalState.player_data.pop(get_player_key(request), None)
        elif "start" in request.form:
            if not GlobalState.started:
                GlobalState.started = True
                GlobalState.player_data = GlobalState.game.assign(GlobalState.player_data)
            else:
                context["error_message"] = "The game has already started."
        elif "end" in request.form:
            if GlobalState.started:
                GlobalState.player_data = {}
                GlobalState.started = False
            else:
                context["error_message"] = "The game has already ended."

    if GlobalState.started:
        context["message"] = "The game has started. There are %s players." % len(GlobalState.player_data)
    return render_template("index.html", **context)

@app.route("/players", methods=["GET"])
def players():
    if request.remote_addr not in ["localhost", "127.0.0.1", "::1"]:
        abort(404)

    return render_template("players.html", player_data=GlobalState.player_data)


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("-D", "--debug", action="store_true", default=False, help="Enable flask debug mode.")
    ap.add_argument("-H", "--host", type=str, default="localhost", help="Specify host to listen on.")
    ap.add_argument("-P", "--port", type=int, default=5000, help="Specify port to listen on.")
    ap.add_argument("-G", "--game", type=str, default=None, help="Specify the game to import and run.")
    args = ap.parse_args()

    if args.game:
        GlobalState.game = get_game(args.game)()

    app.debug = args.debug
    server = WSGIServer((args.host, args.port), app)
    print(" Running on http://%s:%s/ (Press CTRL+C to quit)" % (args.host, args.port))
    try:
        server.serve_forever()
    except (KeyboardInterrupt, SystemExit):
        server.stop()
