import random
from game_definition import GameDefinition, register_game

class SecretHitler(GameDefinition):
    """
    http://secrethitler.com/
    https://boardgamegeek.com/boardgame/188834/secret-hitler
    """
    title = "Secret Hitler Picker"

    preference_options = ["Liberal", "Fascist"]

    def assign(self, player_data):
        player_count = len(player_data)

        liberal_count = int(player_count / 2) + 1
        fascist_count = player_count - liberal_count

        current_liberals = 0
        current_fascists = 0
        hitler_chosen = False

        for player in self.shuffled_players(player_data.values()):
            if (player["preference"] == "Liberal" and current_liberals < liberal_count) or fascist_count == current_fascists:
                player["assignment"] = "Liberal"
                player["assignment_message"] = "Your are a liberal."
                current_liberals += 1
            else:
                if hitler_chosen is False:
                    player["assignment"] = "Hitler"
                    player["assignment_message"] = "Your are Hitler."
                    hitler_chosen = True
                else:
                    player["assignment"] = "Fascist"
                    player["assignment_message"] = "Your are a fascist."
                current_fascists += 1

        return player_data

register_game(SecretHitler)