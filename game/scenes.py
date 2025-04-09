from game.engine import TextAdventure

def setup_locations(game):
    """Set up all game locations"""
    # Office area
    game.add_location("office", "Your Office",
                      "Your small office at Nexus Corp. A computer terminal sits on your desk.",
                      {"north": "hallway"},
                      {"use terminal": lambda: use_terminal(game)})

    game.add_location("hallway", "Hallway",
                      "A sterile corporate hallway with fluorescent lighting.",
                      {"south": "office", "east": "lab", "west": "break_room"},
                      {"talk to colleague": lambda: colleague_conversation(game)})

    # Add more locations as needed

def use_terminal(game):
    """Handle terminal interaction scene"""
    game.display_header("Terminal")
    game.type_text("You sit down at the terminal. The screen glows with the Nexus Corp logo.")
    # Implement scene logic
    return True

def colleague_conversation(game):
    """Handle conversation with colleague"""
    game.display_header("Conversation")
    game.type_text("Your colleague looks nervous as you approach.")
    # Implement conversation logic
    return True
