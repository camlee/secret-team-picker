from game_definition import GameDefinition, register_game

class TheResistance(GameDefinition):
    """
    https://boardgamegeek.com/boardgame/41114/resistance
    """
    title = "The Resistance"

    preference_options = ["Resistance", "Spy"]

    def assign(player_data):
        raise NotImplementedError()

register_game(TheResistance)