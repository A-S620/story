import os
import time
import sys
import json
from blessed import Terminal


class TextAdventure:
    def __init__(self):
        self.term = Terminal()
        self.player_name = ""
        self.inventory = []
        self.story_flags = {}
        self.locations = {}
        self.current_location = None
        self.easter_eggs_found = 0
        self.game_over = False

    def clear_screen(self):
        """Clear the console screen"""
        print(self.term.clear)

    def type_text(self, text, speed=0.03):
        """Display text with a typewriter effect"""
        for char in text:
            sys.stdout.write(char)
            sys.stdout.flush()
            time.sleep(speed)
        print()

    def display_header(self, title=""):
        """Display a formatted header"""
        self.clear_screen()
        print("=" * 60)
        print(title.center(60))
        print("=" * 60)
        print()

    def get_input(self, prompt, options=None):
        """Get user input with optional validation against provided options"""
        while True:
            self.type_text(prompt)
            if options:
                for i, option in enumerate(options, 1):
                    print(f"{i}. {option}")

            choice = input("> ").strip()

            if options:
                try:
                    choice_num = int(choice)
                    if 1 <= choice_num <= len(options):
                        return choice_num
                    else:
                        print("Invalid option. Please try again.")
                except ValueError:
                    # Handle special commands
                    if choice.lower() == "inventory":
                        self.show_inventory()
                        continue
                    elif choice.lower() == "help":
                        self.show_help()
                        continue
                    else:
                        print("Please enter a number or a valid command.")
            else:
                return choice

    def add_to_inventory(self, item):
        """Add an item to the player's inventory"""
        self.inventory.append(item)
        self.type_text(f"Added to inventory: {item}")
        time.sleep(1)

    def remove_from_inventory(self, item):
        """Remove an item from the player's inventory"""
        if item in self.inventory:
            self.inventory.remove(item)
            self.type_text(f"Removed from inventory: {item}")
            time.sleep(1)
            return True
        return False

    def show_inventory(self):
        """Display the player's inventory"""
        self.display_header("INVENTORY")
        if not self.inventory:
            self.type_text("Your inventory is empty.")
        else:
            self.type_text("Inventory:")
            for item in self.inventory:
                print(f"- {item}")
        self.type_text("\nPress Enter to continue...")
        input()

    def show_help(self):
        """Display help information"""
        self.display_header("HELP")
        self.type_text("Available commands:")
        print("- Enter the number of your chosen option")
        print("- Type 'inventory' to check your items")
        print("- Type 'help' to see this information")
        print("- Some puzzles may have special commands - experiment!")
        self.type_text("\nPress Enter to continue...")
        input()

    def set_flag(self, flag_name, value=True):
        """Set a story flag to track player progress and choices"""
        self.story_flags[flag_name] = value

    def check_flag(self, flag_name, default=False):
        """Check if a story flag is set"""
        return self.story_flags.get(flag_name, default)

    def increment_flag(self, flag_name, amount=1, default=0):
        """Increment a numeric story flag"""
        current_value = self.story_flags.get(flag_name, default)
        self.story_flags[flag_name] = current_value + amount
        return self.story_flags[flag_name]

    def add_location(self, location_id, name, description, connections=None, available_actions=None):
        """Add a location to the game world"""
        if connections is None:
            connections = {}
        if available_actions is None:
            available_actions = {}

        self.locations[location_id] = {
            "name": name,
            "description": description,
            "connections": connections,  # dict of direction: location_id
            "actions": available_actions  # dict of action_name: function
        }

    def go_to(self, location_id):
        """Move player to a new location"""
        if location_id in self.locations:
            self.current_location = location_id
            self.describe_location()
            return True
        return False

    def describe_location(self):
        """Display the current location"""
        if self.current_location and self.current_location in self.locations:
            location = self.locations[self.current_location]
            self.display_header(location["name"])
            self.type_text(location["description"])

            # Show available directions
            if location["connections"]:
                print("\nYou can go:")
                for direction, _ in location["connections"].items():
                    print(f"- {direction}")

            # Show available actions
            if location["actions"]:
                print("\nAvailable actions:")
                for action in location["actions"].keys():
                    print(f"- {action}")

    def process_command(self, command):
        """Process a player command"""
        command = command.lower().strip()

        # Check if it's a movement command
        location = self.locations[self.current_location]
        if command in location["connections"]:
            return self.go_to(location["connections"][command])

        # Check if it's an action command
        if command in location["actions"]:
            return location["actions"][command]()

        # Handle inventory and help commands
        if command == "inventory":
            self.show_inventory()
            return True
        elif command == "help":
            self.show_help()
            return True

        print("I don't understand that command.")
        return False

    def puzzle(self, question, answer, hint=None, incorrect_message="That's not correct."):
        """Present a puzzle to the player"""
        self.type_text(question)
        if hint:
            self.type_text(f"Hint: {hint}")

        attempts = 0
        while attempts < 3:
            user_answer = input("> ").strip().lower()

            if user_answer == answer.lower():
                self.type_text("Correct!")
                return True
            else:
                attempts += 1
                if attempts < 3:
                    self.type_text(incorrect_message)
                    self.type_text(f"You have {3-attempts} attempts remaining.")
                else:
                    self.type_text("You've run out of attempts.")

        return False

    def hidden_command_easter_egg(self, command, message, flag=None):
        """Check for a hidden command and display a special message if found"""
        if command.lower() == command.lower():
            self.easter_eggs_found += 1
            self.type_text("\n=== EASTER EGG FOUND ===")
            self.type_text(message)
            if flag:
                self.set_flag(flag)
            self.type_text("\nPress Enter to continue...")
            input()
            return True
        return False

    def relationship_change(self, character, amount):
        """Update relationship value with a character"""
        flag_name = f"relationship_{character}"
        current = self.story_flags.get(flag_name, 0)
        self.story_flags[flag_name] = current + amount

        if amount > 0:
            self.type_text(f"Your relationship with {character} has improved.")
        elif amount < 0:
            self.type_text(f"Your relationship with {character} has worsened.")

        return self.story_flags[flag_name]

    def save_game(self, filename="save.json"):
        """Save the current game state"""
        save_data = {
            "player_name": self.player_name,
            "inventory": self.inventory,
            "story_flags": self.story_flags,
            "current_location": self.current_location,
            "easter_eggs_found": self.easter_eggs_found
        }

        try:
            with open(filename, 'w') as f:
                json.dump(save_data, f)
            self.type_text(f"Game saved successfully to {filename}")
            return True
        except Exception as e:
            self.type_text(f"Error saving game: {e}")
            return False

    def load_game(self, filename="save.json"):
        """Load a saved game state"""
        try:
            with open(filename, 'r') as f:
                save_data = json.dump(f)

            self.player_name = save_data.get("player_name", "")
            self.inventory = save_data.get("inventory", [])
            self.story_flags = save_data.get("story_flags", {})
            self.current_location = save_data.get("current_location", None)
            self.easter_eggs_found = save_data.get("easter_eggs_found", 0)

            self.type_text(f"Game loaded successfully from {filename}")
            self.describe_location()
            return True
        except Exception as e:
            self.type_text(f"Error loading game: {e}")
            return False

    def start_game(self):
        """Initialize and start the game"""
        self.display_header("YOUR GAME TITLE")
        self.type_text("Welcome to your adventure!")

        # Get player name
        self.player_name = input("What is your name? ").strip()

        # Set up initial location and game state
        # This should be implemented in your game-specific code

        # Main game loop
        while not self.game_over:
            if not self.current_location:
                # Set initial location if not set
                # self.go_to("starting_location")
                pass

            command = input("\nWhat would you like to do? > ").strip()

            if command.lower() == "quit":
                if self.get_input("Are you sure you want to quit?", ["Yes", "No"]) == 1:
                    self.game_over = True
            elif command.lower() == "save":
                self.save_game()
            elif command.lower() == "load":
                self.load_game()
            else:
                self.process_command(command)

        self.display_header("GAME OVER")
        self.type_text("Thank you for playing!")
