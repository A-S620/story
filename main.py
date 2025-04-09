from game.engine import TextAdventure
from game.scenes import setup_locations

class Story(TextAdventure):
    def __init__(self):
        super().__init__()
        self.game_title = "Moral Protocol"

    def start_game(self):
        """Initialize and start the game"""
        self.display_header(self.game_title)
        self.type_text("The year is 2052. Megacorporations control most aspects of daily life.")
        self.type_text("You work for Nexus Corp, a leading technology company developing 'humanitarian AI systems'...")
        self.type_text("At least that's what you've been told.")

        # Get player name
        self.player_name = input("What is your name? ").strip()

        # Set up game world
        setup_locations(self)
        self.current_location = "office"

        # Main game loop
        while not self.game_over:
            self.describe_location()

            command = input("\nWhat would you like to do? > ").strip()

            if command.lower() == "quit":
                if self.get_input("Are you sure you want to quit?", ["Yes", "No"]) == 1:
                    self.game_over = True
            elif command.lower() == "save":
                self.save_game("data/saves/savegame.json")
            elif command.lower() == "load":
                self.load_game("data/saves/savegame.json")
            else:
                self.process_command(command)

        self.display_header("GAME OVER")
        self.type_text("Thank you for playing Moral Protocol!")

if __name__ == "__main__":
    game = Story()
    game.start_game()
