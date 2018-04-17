import sys
import random
import operator

games = {}

def register_game(game):
    games[game.__name__] = game

def get_game(name):
    try:
        return games[name]
    except KeyError:
        print("%s game not found. Choices are: %s" % (name, ", ".join(games.keys())))
        sys.exit(1)

class GameDefinition:
    title = "Title"
    preference_options = []

    def assign(self, player_data):
        """
        Assigns each player to one of the preference options, based on their preference
        and the game rules.

        Input: a dictionary of players, where the key is a unique identifider for the player
        and the values are themselves dictionaries with the key "preference".

        Output: the same dictionary of players, but new keys added to each value:
        * assignment: which of the preference_options this player was assigned to
        * assignment_message: a friendly message describing the assignment
        """
        raise NotImplementedError()

    def shuffled_players(self, players):
        players = list(players)
        random.shuffle(players)
        return players

    def ordered_players(self, players):
        players = list(players)
        players.sort(key=operator.itemgetter("number"))
        return players

class DefaultGame(GameDefinition):
    title = "Secret Team Picker"
    preference_options = ["Team A", "Team B", "Team C"]

    def assign(self, player_data):
        player_count = len(player_data)
        team_count = len(self.preference_options)
        players_per_team = int(player_count / team_count)
        extra_players = player_count % team_count

        team_counts = {preference: 0 for preference in self.preference_options}
        unassigned_players = []

        for player in self.shuffled_players(player_data.values()):
            players_on_team = team_counts[player["preference"]]
            if players_on_team < players_per_team or (players_on_team == players_per_team and extra_players):
                assignment = player["preference"]
            else:
                unassigned_players.append(player)
                continue

            player["assignment"] = assignment
            player["assignment_message"] = "You are on %s" % assignment

            team_counts[player["assignment"]] += 1

        for player in unassigned_players:
            for team, players_on_team in team_counts.items():
                if players_on_team < players_per_team or (players_on_team == players_per_team and extra_players):
                    assignment = team
                    break

            player["assignment"] = assignment
            player["assignment_message"] = "You are on %s" % assignment

            team_counts[player["assignment"]] += 1

        return player_data

    def player_list(self, player_data, for_player):
        players = []

        for player in self.ordered_players(player_data.values()):
            player = player.copy()
            if player.get("key") != for_player.get("key"):
                player["preference"] = "(hidden)"
                if player.get("assignment"):
                    player["assignment"] = "(hidden)"
            players.append(player)

        return players


register_game(DefaultGame)

from games import *