"""
COMP 163 - Project 3: Quest Chronicles
Character Manager Module - Starter Code

Name: [Tashe Graham]

AI Usage: [Document any AI assistance used]

This module handles character creation, loading, and saving.
"""

import os
from custom_exceptions import (
    InvalidCharacterClassError,
    CharacterNotFoundError,
    SaveFileCorruptedError,
    InvalidSaveDataError,
    CharacterDeadError
)

# ============================================================================
# CHARACTER MANAGEMENT FUNCTIONS
# ============================================================================
def create_character(name, character_class):

    
    # Validate character_class first
    valid_char_classes = ["Warrior", "Mage", "Rogue", "Cleric"]
    
    # Raise InvalidCharacterClassError if class not in valid list
    if character_class not in valid_char_classes:
        raise InvalidCharacterClassError(f"{character_class} is not an available class.")
    
    base_stats = {
        "Warrior": {"health": 120, "strength": 15, "magic": 5}, 
        "Mage":    {"health": 80,  "strength": 8,  "magic": 20},
        "Rogue":   {"health": 90,  "strength": 12, "magic": 10},
        "Cleric":  {"health": 100, "strength": 10, "magic": 15}
    }

    stats = base_stats[character_class]

    return {
        "name": name,
        "class": character_class,
        "level": 1,
        "health": stats["health"],
        "max_health": stats["health"],
        "strength": stats["strength"],
        "magic": stats["magic"],
        "experience": 0, 
        "gold": 100,
        # Empty
        "inventory": [], 
        "active_quests": [],
        "completed_quests": [] 
    }



def save_character(character, save_directory="data/save_games"):
    # AI Use. Google Gemini was used to handle I/O errors properly
    # TODO: Implement save functionality
    # Handle any file I/O errors appropriately
    
    # Create save_directory if it doesn't exist
    os.makedirs(save_directory, exist_ok=True)

    filepath = os.path.join(save_directory, f"{character['name']}_save.txt")

    try:
        with open(filepath, "w") as f:
            for key, value in character.items():
                # Lists should be saved as comma-separated values
                if isinstance(value, list):
                    value = ",".join(value)
                # Write the line as key:value
                f.write(f"{key}:{value}\n")
        return True
    except Exception as e:
        # Could log e here if needed
        return False
    
def load_character(character_name, save_directory="data/save_games"):

    
    # TODO: Implement load functionality

    filepath = os.path.join(save_directory, f"{character_name}_save.txt")

    # Check if the file exists
    if not os.path.exists(filepath):
        raise CharacterNotFoundError(f"Save file not found for: {character_name}")

    character = {}
    # Try to read file → SaveFileCorruptedError
    try:
        with open(filepath, "r") as f:
            for line in f:
                # Skips invalid lines
                if ":" not in line:
                    continue

                # Split at the first colon into key and value
                key, value = line.strip().split(":", 1)

                # Strip extra whitespace from key and value
                key = key.strip()
                value = value.strip()
                # Parse comma-separated lists back into Python lists
                if "," in value:
                    value = value.split(",")
                # Convert numeric strings to integers
                elif value.isdigit():
                    value = int(value)

                # Store in character dictionary
                character[key] = value

    except Exception as e:
         # Validate data format → InvalidSaveDataError
        raise InvalidSaveDataError(f"Save data format is invalid for {character_name}: {e}")

    return character

def list_saved_characters(save_directory="data/save_games"):

    """
    Get list of all saved character names
    
    Returns: List of character names (without _save.txt extension)
    """
    # TODO: Implement this function
    # AI Use. Google Gemini was used to extract character names from file

    
    if not os.path.exists(save_directory):
        # Return empty list if directory doesn't exist
        return []
    # Extract character names from filenames
    files = os.listdir(save_directory)
    return [f.replace("_save.txt", "") for f in files if f.endswith("_save.txt")]
    

def delete_character(character_name, save_directory="data/save_games"):


    
    # TODO: Implement character deletion
    # Verify file exists before attempting deletion
    filename = f"{character_name}_save.txt"
    filepath = os.path.join(save_directory, filename)
    if not os.path.exists(filepath):
        raise CharacterNotFoundError(f"Character {character_name} was not found.")
    os.remove(filepath)

    return True


# ============================================================================
# CHARACTER OPERATIONS
# ============================================================================

def gain_experience(character, xp_amount):
    
    # TODO: Implement experience gain and leveling
    # Update stats on level up
    
    # Check if character is dead first
    if character["health"] == 0:
        raise CharacterDeadError("Character is dead.")
    # Add experience
    character["experience"] += xp_amount
    # Check for level up (can level up multiple times)
    while character["experience"] >= character["level"] * 100:
        level_up_xp = character["level"] * 100
        character["experience"] -= level_up_xp
        character["level"] += 1
        character["max_health"] += 10
        character["strength"] += 2
        character["magic"] += 2
        character["health"] = character["max_health"]

    

def add_gold(character, amount):

    # TODO: Implement gold management


    # character.get() reads the amount of gold the character has
    current_gold = character.get("gold", 0)
    # Check that result won't be negative
    total_gold = current_gold + amount
    if total_gold < 0:
        raise ValueError("Not enough gold.")

    # Update character's gold
    character["gold"] = total_gold

    return total_gold
    

def heal_character(character, amount):
    
    # TODO: Implement healing
    
    if character["health"] <= 0:
        raise CharacterDeadError("Character is dead, heal failed.")
        
    # Calculate actual healing (don't exceed max_health)
    base_character_health = character["health"]
     # Update character health

    character["health"] = min(character["health"] + amount, character["max_health"]) 

    return character["health"] - base_character_health

def is_character_dead(character):

    # TODO: Implement death check

    current_health = character.get("health", 0) 

    if current_health <= 0:
        print("Character is dead.")
        return True # Character has no health
    else:
        print("Character is alive.")
        return False # Character has health  


def revive_character(character):

    # TODO: Implement revival
    # Restore health to half of max_health

    # Check if character is dead
    if not is_character_dead(character):
        return False  # If the character is alive, they obviously cannot be revived
    
    # Restore health to half of max_health
    half_health = character["max_health"] // 2  

    character["health"] = half_health 

    return True
    

# ============================================================================
# VALIDATION
# ============================================================================
  
def validate_character_data(character):
    
    
    # Check all required keys exist
    required_fields = {
        "name": str,
        "class": str,
        "level": int,
        "health": int,
        "max_health": int,
        "strength": int,
        "magic": int,
        "experience": int,
        "gold": int,
        "inventory": list,
        "active_quests": list,
        "completed_quests": list
    }

    # Check that numeric values are numbers
    # Check that lists are actually lists
    for field, expected_type in required_fields.items():
        if field not in character:
            raise InvalidSaveDataError(f"Missing required field: {field}")
        value = character[field]
        if not isinstance(value, expected_type):
            raise InvalidSaveDataError(f"Field '{field}' must be of type {expected_type.__name__}")

    return True
# ============================================================================
# TESTING
# ============================================================================

if __name__ == "__main__":
    print("=== CHARACTER MANAGER TEST ===")
    
    # Test character creation
    # try:
    #     char = create_character("TestHero", "Warrior")
    #     print(f"Created: {char['name']} the {char['class']}")
    #     print(f"Stats: HP={char['health']}, STR={char['strength']}, MAG={char['magic']}")
    # except InvalidCharacterClassError as e:
    #     print(f"Invalid class: {e}")
    
    # Test saving
    # try:
    #     save_character(char)
    #     print("Character saved successfully")
    # except Exception as e:
    #     print(f"Save error: {e}")
    
    # Test loading
    # try:
    #     loaded = load_character("TestHero")
    #     print(f"Loaded: {loaded['name']}")
    # except CharacterNotFoundError:
    #     print("Character not found")
    # except SaveFileCorruptedError:
    #     print("Save file corrupted")
