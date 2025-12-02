"""
COMP 163 - Project 3: Quest Chronicles
Main Game Module - Starter Code

Name: [Tashe Graham]

AI Usage: [Document any AI assistance used]

This is the main game file that ties all modules together.
Demonstrates module integration and complete game flow.
"""

# Import all our custom modules
import character_manager
import inventory_system
import quest_handler
import combat_system
import game_data
from custom_exceptions import *

# ============================================================================
# GAME STATE
# ============================================================================

# Global variables for game data
current_character = None
all_quests = {}
all_items = {}
game_running = False

# ============================================================================
# MAIN MENU
# ============================================================================

def main_menu():
    while True:
        # Show options
        print("\n=== MAIN MENU ===")
        print("1. New Game")
        print("2. Load Game")
        print("3. Exit")
        
        try:
            # Get user input
            choice = int(input("\nEnter choice (1-3): "))
            if 1 <= choice <= 3:
                return choice
            # Validate input (1-3)
            else:
                print("Invalid choice. Please choose 1-3.")
        except ValueError:
            print("Please enter a valid number.")
    
   
    
    pass

def new_game():
    
    global current_character
    
    # TODO: Implement new game creation
    # Get character name from user
    name = input("Enter character name: ")
    # Get character class from user
    while True:
        print("\nChoose a Class:")
        print("1. Warrior")
        print("2. Mage")
        print("3. Rogue")
        class_input = input("Enter class name or number: ")
    # Try to create character with character_manager.create_character()
        if class_input in ['1', 'warrior']:
            char_class = "Warrior"
            break
        elif class_input in ['2', 'mage']:
            char_class = "Mage"
            break
        elif class_input in ['3', 'rogue']:
            char_class = "Rogue"
            break
        else:
            print("Invalid class selection.")
    # Handle InvalidCharacterClassError
    try:
        # Save character
        print(f"\nCharacter {name} the {char_class} created successfully!")
        
        current_character = {"name": name, "class": char_class, "level": 1, "gold": 0} 
         # Start game loop
        game_loop()
        
    except InvalidCharacterClassError: # Replace with InvalidCharacterClassError later
        print(f"Error creating character")
    pass

def load_game():
    """
    Load an existing saved game
    
    Shows list of saved characters
    Prompts user to select one
    """
    global current_character
    
    # TODO: Implement game loading
    # Get list of saved characters
    print("\n--- LOAD GAME ---")
    saves = ["Save1.json", "Save2.json"] 
    
    if not saves:
        print("No saved games found.")
        return
    # Display them to user
    for i, save in enumerate(saves, 1):
        print(f"{i}. {save}")
    # Get user choice
    # Try to load character with character_manager.load_character()
    try:
        choice = int(input("Select save file number: ")) - 1
        if 0 <= choice < len(saves):
            
            print(f"Loaded {saves[choice]}...")
            game_loop()
    # Handle CharacterNotFoundError and SaveFileCorruptedError
        else:
            print("Invalid selection.")
    except CharacterNotFoundError:
        print("Couldn't find character")
    except SaveFileCorruptedError: 
        print(f"Failed to load save")
    # Start game loop
    pass

# ============================================================================
# GAME LOOP
# ============================================================================

def game_loop():
    """
    Main game loop - shows game menu and processes actions
    """
    global game_running, current_character
    print("\nWelcome to the Adventure!")
    
    game_running = True
    
    # TODO: Implement game loop
    # While game_running:
    # Display game menu
    # Execute chosen action
    while game_running:
        choice = game_menu()
         # Get player choice
        if choice == 1:
            view_character_stats()
        elif choice == 2:
            view_inventory()
        elif choice == 3:
            quest_menu()
        elif choice == 4:
            explore()
        elif choice == 5:
            shop()
        elif choice == 6:
            save_game()
            print("Thanks for playing!")
            game_running = False
    #   Save game after each action
    pass

def game_menu():
    """
    Display game menu and get player choice
    

    """
    print("\n--- GAME MENU ---")
    print("1. View Character Stats")
    print("2. View Inventory")
    print("3. Quest Menu")
    print("4. Explore (Find Battles)")
    print("5. Shop")
    print("6. Save and Quit")
    
    while True:
        try:
            choice = int(input("\nWhat would you like to do? (1-6): "))
            if 1 <= choice <= 6:
                return choice
            print("Please enter a number between 1 and 6.")
        except ValueError:
            print("Invalid input.")
    # TODO: Implement game menu
    pass

# ============================================================================
# GAME ACTIONS
# ============================================================================

def view_character_stats():
    """Display character information"""
    global current_character

    
    # TODO: Implement stats display
    if not current_character:
        print("No character loaded.")
        return
    # Show: name, class, level, health, stats, gold, etc.

    print("\n=== CHARACTER STATS ===")
    print(f"Name: {current_character['name']}")
    print(f"Class: {current_character['class']}")
    print(f"Level: {current_character['level']}")
    print(f"XP: {current_character['experience']}")
    print(f"Gold: {current_character['gold']}")
    print(f"Health: {current_character['health']}/{current_character['max_health']}")
    print(f"Strength: {current_character['strength']}")
    print(f"Magic: {current_character['magic']}")

    # Show quest progress using quest_handler

    active = current_character.get("active_quests", [])
    completed = current_character.get("completed_quests", [])

    print("\nActive Quests:")
    if active:
        for q in active:
            print(f" - {q}")
    else:
        print(" (None)")

    print("\nCompleted Quests:")
    if completed:
        for q in completed:
            print(f" - {q}")
    else:
        print(" (None)")

    
    pass

def view_inventory():
    """Display and manage inventory"""
    global current_character, all_items
    
    # TODO: Implement inventory menu
    # Handle exceptions from inventory_system
    inv = current_character["inventory"]

    print("\n=== INVENTORY ===")
    if not inv:
        print("Inventory is empty.")
        return

    for idx, item_id in enumerate(inv, 1):
        # Show current inventory
        item_info = all_items.get(item_id, {"name": "UNKNOWN"})
        print(f"{idx}. {item_info['name']} ({item_info.get('type', 'unknown')})")

    # Options: Use item, Equip weapon/armor, Drop item
    print("\nOptions:")
    print("1. Use Item")
    print("2. Equip Item")
    print("3. Drop Item")
    print("4. Back")

    try:
        choice = int(input("Select an option: "))
    except ValueError:
        print("Invalid input.")
        return

    if choice == 4:
        return

    try:
        item_choice = int(input("Which item number? ")) - 1
        item_id = inv[item_choice]
        item_data = all_items[item_id]
    except:
        print("Invalid item selection.")
        return

    # Use item
    if choice == 1:
        try:
            result = inventory_system.use_item(current_character, item_id, item_data)
            print(result)
        except Exception as e:
            print(f"Error: {e}")

    # Equip item
    elif choice == 2:
        try:
            t = item_data["type"]
            if t == "weapon":
                print(inventory_system.equip_weapon(current_character, item_id, item_data))
            elif t == "armor":
                print(inventory_system.equip_armor(current_character, item_id, item_data))
            else:
                print("This item cannot be equipped.")
        except Exception as e:
            print(f"Error: {e}")

    # Drop item
    elif choice == 3:
        try:
            inventory_system.remove_item_from_inventory(current_character, item_id)
            print(f"Dropped {item_data['name']}.")
        except Exception as e:
            print(f"Error: {e}")
    pass

def quest_menu():
    """Quest management menu"""
    global current_character, all_quests
    
    # TODO: Implement quest menu
    
    # Handle exceptions from quest_handler
    
    print("\n=== QUEST MENU ===")
    print("1. View Active Quests")
    print("2. View Available Quests")
    print("3. View Completed Quests")
    print("4. Accept Quest")
    print("5. Abandon Quest")
    print("6. Complete Quest (TEST ONLY)")
    print("7. Back")

    try:
        choice = int(input("Select an option: "))
    except ValueError:
        print("Invalid input.")
        return

    if choice == 7:
        return

    if choice == 1:
        quest_handler.display_active_quests(current_character, all_quests)

    elif choice == 2:
        quest_handler.display_available_quests(current_character, all_quests)

    elif choice == 3:
        quest_handler.display_completed_quests(current_character, all_quests)

    elif choice == 4:
        quest_id = input("Enter quest ID to accept: ").strip()
        try:
            quest_handler.accept_quest(current_character, quest_id, all_quests)
            print("Quest accepted!")
        except Exception as e:
            print(f"Error: {e}")

    elif choice == 5:
        quest_id = input("Enter quest ID to abandon: ").strip()
        try:
            quest_handler.abandon_quest(current_character, quest_id)
            print("Quest abandoned.")
        except Exception as e:
            print(f"Error: {e}")

    elif choice == 6:
        quest_id = input("Enter quest ID to force-complete: ").strip()
        try:
            quest_handler.complete_quest(current_character, quest_id, all_quests)
            print("Quest completed! (test mode)")
        except Exception as e:
            print(f"Error: {e}")

    pass

def explore():
    """Find and fight random enemies"""
    global current_character
    
    # TODO: Implement exploration
    # Handle exceptions
    print("\n=== EXPLORING... ===")

    try:
        # Generate random enemy based on character level
        enemy = combat_system.generate_enemy(current_character["level"])
        print(f"You encountered a {enemy['name']}!")

        # Start combat with combat_system.SimpleBattle
        battle = combat_system.SimpleBattle(current_character, enemy)
        result = battle.start()
        # Handle combat results (XP, gold, death)
        if result == "victory":
            rewards = combat_system.get_victory_rewards(enemy)
            xp = rewards["xp"]
            gold = rewards["gold"]

            current_character["experience"] += xp
            current_character["gold"] += gold

            print(f"You defeated the {enemy['name']}!")
            print(f"Rewards: +{xp} XP, +{gold} gold")
        # Handle exceptions
        elif result == "defeat":
            print("You were defeated in battle...")
            raise CharacterDeadError("Your character has died.")

        else:
            print("Combat ended unexpectedly.")

    except CombatError as e:
        print(f"Combat error: {e}")

    except CharacterDeadError as e:
        print(f"\n*** GAME OVER ***\n{e}")
        print("Load a saved game to continue.")
        return

    except Exception as e:
        print(f"Unexpected error during exploration: {e}")
    pass

def shop():
    """Shop menu for buying/selling items"""
    global current_character, all_items
    
    # TODO: Implement shop
    # Handle exceptions from inventory_system

    # Show available items for purchase
    while True:
        print("\n=== SHOP MENU ===")
         # Show current gold
        print(f"Your Gold: {current_character['gold']}")
        print("Items for Sale:")

        item_list = list(all_items.items())
        for index, (item_id, item) in enumerate(item_list, 1):
            print(f"{index}. {item['name']} ({item['type']}), Cost: {item['cost']} gold")

        print("\nOptions:")
        print("1. Buy Item")
        print("2. Sell Item")
        print("3. Back")

        try:
            choice = int(input("Choose an option: "))
        except ValueError:
            print("Invalid input. Enter a number.")
            continue

        # Return to menu
        if choice == 3:
            return

        # Options: Buy item, Sell item, Back
        if choice == 1:
            try:
                num = int(input("Enter item number to buy: ")) - 1
                item_id, item_data = item_list[num]

                inventory_system.purchase_item(current_character, item_id, item_data)
                print(f"Purchased {item_data['name']}!")

            except IndexError:
                print("Invalid item number.")
            except Exception as e:
                print(f"Error: {e}")

        elif choice == 2:
            inv = current_character["inventory"]

            if not inv:
                print("Your inventory is empty.")
                continue

            print("\nYour Items:")
            for idx, item_id in enumerate(inv, 1):
                item = all_items[item_id]
                print(f"{idx}. {item['name']} ({item['type']})")

            try:
                num = int(input("Enter item number to sell: ")) - 1
                item_id = inv[num]
                item_data = all_items[item_id]

                gold_received = inventory_system.sell_item(current_character, item_id, item_data)
                print(f"Sold {item_data['name']} for {gold_received} gold.")

            except IndexError:
                print("Invalid item number.")
            except Exception as e:
                print(f"Error: {e}")

        else:
            print("Invalid choice. Pick 1, 2, or 3.")
    
    pass

# ============================================================================
# HELPER FUNCTIONS
# ============================================================================

def save_game():
    """Save current game state"""
    global current_character
    
    # TODO: Implement save
   
    try:
        # Use character_manager.save_character()
        character_manager.save_character(current_character)
        print("\nGame saved successfully!\n")
    # Handle any file I/O exceptions
    except Exception as e:
        print(f"[ERROR] Failed to save game: {e}")
    pass

def load_game_data():
    """Load all quest and item data from files"""
    global all_quests, all_items
    
    # TODO: Implement data loading
    try:
        # Try to load quests with game_data.load_quests()
        all_quests = game_data.load_quests()
        # Try to load items with game_data.load_items()
        all_items = game_data.load_items()
    # Handle MissingDataFileError, InvalidDataFormatError
    except MissingDataFileError:
        print("[WARNING] Data files missing. Creating default files...")
         # If files missing, create defaults with game_data.create_default_data_files()
        game_data.create_default_data_files()

        try:
            all_quests = game_data.load_quests()
            all_items = game_data.load_items()
        except Exception as e:
            print(f"[ERROR] Failed to load data even after creating defaults: {e}")
            all_quests = {}
            all_items = {}

    except InvalidDataFormatError as e:
        print(f"[ERROR] Data file format invalid: {e}")
        all_quests = {}
        all_items = {}

    except Exception as e:
        print(f"[ERROR] Unexpected error loading data: {e}")
        all_quests = {}
        all_items = {}
   
    pass

def handle_character_death():
    """Handle character death"""
    global current_character, game_running
    
    # TODO: Implement death handling
    
    # Display death message
    print("\n===== YOU HAVE DIED =====")
    print("Want to revive? Choose an option:\n")

    while True:
        # Offer: Revive (costs gold) or Quit
        print("1. Revive (cost: 50 gold)")
        print("2. Quit to Main Menu")

        choice = input("Choose an option: ")
        # If revive: use character_manager.revive_character()

        if choice == "1":
            if current_character.gold >= 50:
                current_character.gold -= 50
                character_manager.revive_character(current_character)
                print("\nYou have been revived!\n")
                return
            else:
                print("Not enough gold to revive!")
        # If quit: set game_running = False
        elif choice == "2":
            print("Returning to main menu…")
            game_running = False
            return
        else:
            print("Invalid choice.")

    pass

def display_welcome():
    """Display welcome message"""
    print("=" * 50)
    print("     QUEST CHRONICLES - A MODULAR RPG ADVENTURE")
    print("=" * 50)
    print("\nWelcome to Quest Chronicles!")
    print("Build your character, complete quests, and become a legend!")
    print()

# ============================================================================
# MAIN EXECUTION
# ============================================================================

def main():
    """Main game execution function"""
    
    # Display welcome message
    display_welcome()
    
    # Load game data
    try:
        load_game_data()
        print("Game data loaded successfully!")
    except MissingDataFileError:
        print("Creating default game data...")
        game_data.create_default_data_files()
        load_game_data()
    except InvalidDataFormatError as e:
        print(f"Error loading game data: {e}")
        print("Please check data files for errors.")
        return
    
    # Main menu loop
    while True:
        choice = main_menu()
        
        if choice == 1:
            new_game()
        elif choice == 2:
            load_game()
        elif choice == 3:
            print("\nThanks for playing Quest Chronicles!")
            break
        else:
            print("Invalid choice. Please select 1-3.")

if __name__ == "__main__":
    main()

