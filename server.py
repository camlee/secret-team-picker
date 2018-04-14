#!/usr/bin/env python3
import time
from flask import Flask, request, abort, send_from_directory, render_template
from gevent.wsgi import WSGIServer

from game_definition import title, preference_options, assign

class GlobalState:
    player_data = {}
    started = False

app = Flask(__name__)

@app.context_processor
def inject():
    context = {
        "title": title,
        "preference_options": preference_options,
        "started": GlobalState.started
        }
    player_context = GlobalState.player_data.get(request.remote_addr, {})
    context.update(player_context)
    return context

@app.route("/", methods=["POST", "GET"])
def index():
    context = {}
    if request.method == "POST":
        if "submit" in request.form:
            data = GlobalState.player_data.setdefault(request.remote_addr, {})
            if not GlobalState.started:
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


@app.route("/static/<path:filename>")
def static_files(filename):
    return send_from_directory("static", filename)

if __name__ == "__main__":
    host = "0.0.0.0"
    port = 80
    server = WSGIServer((host, port), app)
    print(" Running on http://%s:%s/ (Press CTRL+C to quit)" % (host, port))
    try:
        server.serve_forever()
    except (KeyboardInterrupt, SystemExit):
        server.stop()
