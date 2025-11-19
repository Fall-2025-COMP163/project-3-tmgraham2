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
    """
    Create a new character with stats based on class
    
    Valid classes: Warrior, Mage, Rogue, Cleric
    
    Returns: Dictionary with character data including:
            - name, class, level, health, max_health, strength, magic
            - experience, gold, inventory, active_quests, completed_quests
    
    Raises: InvalidCharacterClassError if class is not valid
    """
    # TODO: Implement character creation
    # Validate character_class first
    # Example base stats:
    # Warrior: health=120, strength=15, magic=5
    # Mage: health=80, strength=8, magic=20
    # Rogue: health=90, strength=12, magic=10
    # Cleric: health=100, strength=10, magic=15
    
    # All characters start with:
    # - level=1, experience=0, gold=100
    # - inventory=[], active_quests=[], completed_quests=[]
    
    # Raise InvalidCharacterClassError if class not in valid list

    class_base_stats = {
        'Warrior': {'health': 120, 'max_health': 120, 'strength': 15, 'magic': 5},
        'Mage': {'health': 80, 'max_health': 80, 'strength': 8, 'magic': 20},
        'Rogue': {'health': 90, 'max_health': 90, 'strength': 12, 'magic': 10},
        'Cleric': {'health': 100, 'max_health': 100, 'strength': 10, 'magic': 15}

    }

    if character_class not in class_base_stats:
        raise InvalidCharacterClassError(
            f"Invalid class: {character_class}"
        )
    base_stats = class_base_stats[character_class]

    character = {
        'name': name,
        'class': character_class,
        'level': 1,
        'experience': 0,
        'gold': 100,
        'inventory': [],
        'active_quests': [], 
        'completed_quests': []

    }
    character.update(base_stats)
    return character

    pass

def save_character(character, save_directory="data/save_games"):
    """
    Save character to file
    
    Filename format: {character_name}_save.txt
    
    File format:
    NAME: character_name
    CLASS: class_name
    LEVEL: 1
    HEALTH: 120
    MAX_HEALTH: 120
    STRENGTH: 15
    MAGIC: 5
    EXPERIENCE: 0
    GOLD: 100
    INVENTORY: item1,item2,item3
    ACTIVE_QUESTS: quest1,quest2
    COMPLETED_QUESTS: quest1,quest2
    
    Returns: True if successful
    Raises: PermissionError, IOError (let them propagate or handle)
    """
    # TODO: Implement save functionality
    # Create save_directory if it doesn't exist
    # Handle any file I/O errors appropriately
    # Lists should be saved as comma-separated values
    os.makedirs(save_directory, exist_ok=True)


    character_name = character['name']
    filename = f"{character_name}_save.txt"
    file_path = os.path.join(save_directory, filename)
    inventory_str = ','.join(character['inventory'])
    active_quests_str = ','.join(character['active_quests'])
    completed_quests_str = ','.join(character['completed_quests'])

    lines = [
        f"NAME: {character['name']}\n",
        f"CLASS: {character['class']}\n",
        f"LEVEL: {character['level']}\n",
        f"HEALTH: {character['health']}\n",
        f"MAX_HEALTH: {character['max_health']}\n",
        f"STRENGTH: {character['strength']}\n",
        f"MAGIC: {character['magic']}\n",
        f"EXPERIENCE: {character['experience']}\n",
        f"GOLD: {character['gold']}\n",
        f"INVENTORY: {inventory_str}\n",
        f"ACTIVE_QUESTS: {active_quests_str}\n",
        f"COMPLETED_QUESTS: {completed_quests_str}\n"

    ]

    with open(file_path, 'w') as f:
        f.writelines(lines)
    return True
    

    pass

def load_character(character_name, save_directory="data/save_games"):
    """
    Load character from save file
    
    Args:
        character_name: Name of character to load
        save_directory: Directory containing save files
    
    Returns: Character dictionary
    Raises: 
        CharacterNotFoundError if save file doesn't exist
        SaveFileCorruptedError if file exists but can't be read
        InvalidSaveDataError if data format is wrong
    """
    # TODO: Implement load functionality
    # Check if file exists → CharacterNotFoundError
    # Try to read file → SaveFileCorruptedError
    # Validate data format → InvalidSaveDataError
    # Parse comma-separated lists back into Python lists

    filename = f"{character_name}_save.txt"
    file_path = os.path.join(save_directory, filename)

    if not os.path.exists(file_path):
        raise CharacterNotFoundError(
            f"Save file not found for '{character_name}' at {file_path}")
    
    try:
        with open(file_path, 'r') as f:
            lines = f.readlines
    except (IOError, PermissionError) as e:
        raise SaveFileCorruptedError(f"Could not read file: {file_path}")

    character = {}
    
    expected_keys = [
        'name', 'class', 'level', 'health', 'max_health', 'strength', 'magic', 
        'experience', 'gold', 'inventory', 'active_quests', 'completed_quests'
    ]

    int_keys = [
        'LEVEL', 'HEALTH', 'MAX_HEALTH', 'STRENGTH', 'MAGIC', 'EXPERIENCE', 'GOLD'
    ]

    list_keys = ['INVENTORY', 'ACTIVE_QUESTS', 'COMPLETED_QUESTS']

    try:
        for line in lines:
            line = line.strip()
            if not line:
                continue # Skips empty lines
            parts = line.split(": ", 1)
            if len(parts) != 2:
                raise InvalidSaveDataError('Wrong format: {line}')
        for key in expected_keys:
            if key not in character:
                raise InvalidSaveDataError(f"Save file is missing data for {key}")
    except Exception as e:
        print(f"Failed to parse file: {e}")
    return character

    pass

def list_saved_characters(save_directory="data/save_games"):
    """
    Get list of all saved character names
    
    Returns: List of character names (without _save.txt extension)
    """
    # TODO: Implement this function
    # Return empty list if directory doesn't exist
    # Extract character names from filenames
    if not os.path.exists(save_directory):
        return []

    saved_characters = []
    suffix = '_save.txt'

    try:
        files = os.listdir(save_directory)

        for filename in files:
            if filename.endswith(suffix):
                name = filename[:-len(suffix)]
                saved_characters.append(suffix)
    except Exception as e:
        print(f"Could not list files in {save_directory}")
    return []


    pass

def delete_character(character_name, save_directory="data/save_games"):
    """
    Delete a character's save file
    
    Returns: True if deleted successfully
    Raises: CharacterNotFoundError if character doesn't exist
    """
    # TODO: Implement character deletion
    # Verify file exists before attempting deletion
    filename = f"{character_name}_save.txt"
    file_path = os.path.join(save_directory, filename)

    if not os.path.exists(file_path):
        raise CharacterNotFoundError(f"Save file not found at: {file_path}")
    os.remove(file_path)
    return True
    pass

# ============================================================================
# CHARACTER OPERATIONS
# ============================================================================

def gain_experience(character, xp_amount):
    """
    Add experience to character and handle level ups
    
    Level up formula: level_up_xp = current_level * 100
    Example when leveling up:
    - Increase level by 1
    - Increase max_health by 10
    - Increase strength by 2
    - Increase magic by 2
    - Restore health to max_health
    
    Raises: CharacterDeadError if character health is 0
    """
    # TODO: Implement experience gain and leveling
    # Check if character is dead first
    # Add experience
    # Check for level up (can level up multiple times)
    # Update stats on level up
    if character['health'] <= 0:
        raise CharacterDeadError(f"{character['name']} is dead.")
    
    character['experience'] += xp_amount
    print(f"Gained {xp_amount} XP")

    while True: 
        current_level = character['level']
        level_up_xp = current_level * 100

        if character['experience'] < level_up_xp:
            break

        character['experience'] -= level_up_xp
        # Increase Level
        character['level'] += 1

        # Increase stats
        character['max_health'] += 10
        character['strength'] += 2
        character['magic'] += 2

        # Restore health
        character['health'] = character['max_health']
        print(f"{character['name']} has leveled up to Level {character['level']}!")
        print(f"Health has been restored! HEALTH: {character['health']}")

    pass

def add_gold(character, amount):
    """
    Add gold to character's inventory
    
    Args:
        character: Character dictionary
        amount: Amount of gold to add (can be negative for spending)
    
    Returns: New gold total
    Raises: ValueError if result would be negative
    """
    # TODO: Implement gold management
    # Check that result won't be negative
    # Update character's gold
    # Calculate new balance
    new_balance = character['gold'] + amount
    # Checks if character has enough gold
    if new_balance < 0:
        raise ValueError("Not enough gold.")
    # Updates gold balance
    character['gold'] = new_balance
    return character['gold']


    pass

def heal_character(character, amount):
    """
    Heal character by specified amount
    
    Health cannot exceed max_health
    
    Returns: Actual amount healed
    """
    # TODO: Implement healing
    # Calculate actual healing (don't exceed max_health)
    # Update character health
    current_health = character['health']
    max_health = character['max_health']
    # If character is dead, it cannot heal
    if current_health == 0:
        print(f"Cannot heal. {character['name']} is dead.")
    # Potential health
    potential_health = current_health + amount
    # Calculate actual healing 
    if potential_health > max_health:
        new_health = max_health
    else:
        new_health = potential_health
    # Updates character health
    actual_healed = new_health - current_health
    character['health'] = new_health

    return actual_healed
    pass

def is_character_dead(character):
    """
    Check if character's health is 0 or below
    
    Returns: True if dead, False if alive

    """
    if character['health'] <= 0:
        return True
    else:
        return False
    # TODO: Implement death check
    pass

def revive_character(character):
    """
    Revive a dead character with 50% health
    
    Returns: True if revived
    """
    # TODO: Implement revival
    # Restore health to half of max_health
    # Calculate 50% health
    revive_health = character['max_health'] // 2
    # Restore health 
    character['max_health'] = revive_health

    print(f"{character['name']} has been revived!")
    return True
    pass

# ============================================================================
# VALIDATION
# ============================================================================

def validate_character_data(character):
    """
    Validate that character dictionary has all required fields
    
    Required fields: name, class, level, health, max_health, 
                    strength, magic, experience, gold, inventory,
                    active_quests, completed_quests
    
    Returns: True if valid
    Raises: InvalidSaveDataError if missing fields or invalid types
    """
    # TODO: Implement validation
    # Check all required keys exist
    # Check that numeric values are numbers
    # Check that lists are actually lists

    required_fields = {
        'name': str,
        'class': str,
        'level': int,
        'health': int,
        'max_health': int,
        'strength': int,
        'magic': int,
        'experience': int,
        'gold': int,
        'inventory': list,
        'active_quests': list,
        'completed_quests': list
    }
    for key in required_fields.items():
        if key not in character:
            raise InvalidSaveDataError
    return True    
    pass

# ============================================================================
# TESTING
# ============================================================================

if __name__ == "__main__":
    print("=== CHARACTER MANAGER TEST ===")
    
    # Test character creation
    try:
        char = create_character("TestHero", "Warrior")
        print(f"Created: {char['name']} the {char['class']}")
        print(f"Stats: HP={char['health']}, STR={char['strength']}, MAG={char['magic']}")
    except InvalidCharacterClassError as e:
        print(f"Invalid class: {e}")
    
    # Test saving
    try:
        save_character(char)
        print("Character saved successfully")
    except Exception as e:
        print(f"Save error: {e}")
    
    # Test loading
    try:
        loaded = load_character("TestHero")
        print(f"Loaded: {loaded['name']}")
    except CharacterNotFoundError:
        print("Character not found")
    except SaveFileCorruptedError:
        print("Save file corrupted")


