title = "Secret Team Picker"

preference_options = ["Team A", "Team B", "Team C"]


def assign(player_data):
    """
    Assigns each player to one of the preference options, based on their preference
    and the game rules.

    Input: a dictionary of players, where the values are themselves dictionaries with
    the key "preference".

    Output: the same dictionary of players, but new keys added to each value:
    * assignment: which of the preference_options this player was assigned to
    * assignment_message: a friendly message describing the assignment
    """
    player_count = len(player_data)
    team_count = len(preference_options)
    players_per_team = int(player_count / team_count)
    extra_players = player_count % team_count

    team_counts = {preference: 0 for preference in preference_options}
    unassigned_players = []

    for player in player_data.values():
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


try:
    from custom_game_definition import *
except ImportError:
    pass

