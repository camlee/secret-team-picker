Simple web app to allow players of a game to anonymously pick their
team. Allows players to specify a preference and then assigns each
player to a team according to the rules of the game but attempting
to respect everyone's preference.

Setup:

1. Install Python 3.6
2. `pip install -r requirements.txt`

Run development server (should reload on code changes):
```
export FLASK_APP=server.py
flask run
```

Run production server (uses an event loop to handle multiple clients simultaneously):
```
python server.py
```

Add new games:
1. Make a new file in the `games/` folder.
2. Define a class for your game, inheriting from `game_definition.GameDefinition`
3. Call `game_definition.register_game()` with your class as an argument to register your game.
4. Specify which game by either defining the `SECRET_TEAM_PICKER_GAME` environment variable
   or using the `--game` command line option when running `server.py` directly.

Run the tests:
```
python test.py
```

(or feel free to write some real ones)

Docs for libraries used:
* http://flask.pocoo.org/docs/
* http://jinja.pocoo.org/docs/
* http://beauter.outboxcraft.com/


TODO (remove once implemented):
* Add more games (ex. The Resistance)
* List total players, especially before game has started
* List teammates (as applicable) once game has started