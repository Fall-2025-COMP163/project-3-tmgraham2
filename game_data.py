"""
COMP 163 - Project 3: Quest Chronicles
Game Data Module - Starter Code

Name: [Tashe Graham]

AI Usage: [Document any AI assistance used]

This module handles loading and validating game data from text files.
"""

import os
from custom_exceptions import (
    InvalidDataFormatError,
    MissingDataFileError,
    CorruptedDataError
)

# ============================================================================
# DATA LOADING FUNCTIONS
# ============================================================================

def load_quests(filename="data/quests.txt"):
    """
    Load quest data from file
    
    Expected format per quest (separated by blank lines):
    QUEST_ID: unique_quest_name
    TITLE: Quest Display Title
    DESCRIPTION: Quest description text
    REWARD_XP: 100
    REWARD_GOLD: 50
    REQUIRED_LEVEL: 1
    PREREQUISITE: previous_quest_id (or NONE)
    
    Returns: Dictionary of quests {quest_id: quest_data_dict}
    Raises: MissingDataFileError, InvalidDataFormatError, CorruptedDataError
    """
    # TODO: Implement this function
    # Must handle:
    # - FileNotFoundError → raise MissingDataFileError
    # - Invalid format → raise InvalidDataFormatError
    # - Corrupted/unreadable data → raise CorruptedDataError
    quests = {}
    
    try:
        with open(filename, 'r') as f:
            lines = f.readlines()
    except FileNotFoundError:
        raise MissingDataFileError(f"Could not find file: {filename}")
    except:
        raise CorruptedDataError(f"File {filename} is corrupted or has wrong encoding.")
    
    current_block = []
    for line in lines:
        line = line.strip()
        if line:
            current_block.append(line)
        elif current_block:
            # Blank Line
            quest_data = parse_quest_block(current_block)
            validate_quest_data(quest_data)
            quests[quest_data['quest_id']] = quest_data
            current_block = []
    
    # Process the final block if the file didn't end with a blank line
    if current_block:
        quest_data = parse_quest_block(current_block)
        validate_quest_data(quest_data)
        quests[quest_data['quest_id']] = quest_data

    return quests
    
    
     

    pass

def load_items(filename="data/items.txt"):
    """
    Load item data from file
    
    Expected format per item (separated by blank lines):
    ITEM_ID: unique_item_name
    NAME: Item Display Name
    TYPE: weapon|armor|consumable
    EFFECT: stat_name:value (e.g., strength:5 or health:20)
    COST: 100
    DESCRIPTION: Item description

    Raises: MissingDataFileError, InvalidDataFormatError, CorruptedDataError
    """
   # Returns: Dictionary of items {item_id: item_data_dict}
    # TODO: Implement this function
    # Must handle same exceptions as load_quests
    items = {}
    
    try:
        with open(filename, 'r', encoding='utf-8') as f:
            lines = f.readlines()
            
    except FileNotFoundError:
        raise MissingDataFileError(f"Could not find file: {filename}")
    except:
        raise CorruptedDataError(f"File {filename} is corrupted or has wrong encoding.")
    

    current_block = []
    for line in lines:
        line = line.strip()
        if line:
            current_block.append(line)
        elif current_block:
            item_data = parse_item_block(current_block)
            validate_item_data(item_data)
            items[item_data['item_id']] = item_data
            current_block = []
            
    if current_block:
        item_data = parse_item_block(current_block)
        validate_item_data(item_data)
        items[item_data['item_id']] = item_data

    return items
    

    pass

def validate_quest_data(quest_dict):
    """
    Validate that quest dictionary has all required fields
    
    Required fields: quest_id, title, description, reward_xp, 
                    reward_gold, required_level, prerequisite
    
    Returns: True if valid
    Raises: InvalidDataFormatError if missing required fields
    """
    # TODO: Implement validation
    # Check that all required keys exist
    required_fields = [
        'quest_id', 'title', 'description', 'reward_xp', 
        'reward_gold', 'required_level', 'prerequisite'
    ]
    for field in required_fields:
        if field not in quest_dict:
            raise InvalidDataFormatError(f"Missing required quest field: {field}")
    # Check that numeric values are actually numbers
    if not isinstance(quest_dict['reward_xp'], int):
        raise InvalidDataFormatError(f"reward_xp must be an integer")
    if not isinstance(quest_dict['reward_gold'], int):
        raise InvalidDataFormatError(f"reward_gold must be an integer")
    if not isinstance(quest_dict['required_level'], int):
        raise InvalidDataFormatError(f"required_level must be an integer")
    return True
    pass

def validate_item_data(item_dict):
    """
    Validate that item dictionary has all required fields
    
    Required fields: item_id, name, type, effect, cost, description
    Valid types: weapon, armor, consumable
    
    Returns: True if valid
    Raises: InvalidDataFormatError if missing required fields or invalid type
    """
    # TODO: Implement validation
    required_fields = ['item_id', 'name', 'type', 'effect', 'cost', 'description']
    valid_types = ['weapon', 'armor', 'consumable']

    # Check missing keys
    for field in required_fields:
        if field not in item_dict:
            raise InvalidDataFormatError(f"Missing required item field")
            
    # Check valid type
    if item_dict['type'] not in valid_types:
        raise InvalidDataFormatError(f"Invalid item type")
        
    # Check numeric cost
    if not isinstance(item_dict['cost'], int):
        raise InvalidDataFormatError("Item cost must be an integer")

    return True
    pass

def create_default_data_files():
    """
    Create default data files if they don't exist
    This helps with initial setup and testing
    """
    # TODO: Implement this function
    # Create data/ directory if it doesn't exist
    directory = 'data'
    if not os.path.exists(directory):
        try:
            os.makedirs(directory)
        except:
            print(f"Error: Could not create directory {directory}")
            return
    # Create default quests.txt and items.txt files
    # QUESTS
    quests_content = """

QUEST_ID: 2
TITLE: Saving FreeTown
DESCRIPTION: Save the town from the enemy!
REWARD_XP: 250
REWARD_GOLD: 50
REQUIRED_LEVEL: 2
PREREQUISITE: 1"""
    # ITEMS
    items_content = """ITEM_ID: i_001
NAME: Rusty Sword
TYPE: weapon
EFFECT: strength:2
COST: 15
DESCRIPTION: An old sword.
"""
    # Handle any file permission errors appropriately

    try:
        if not os.path.exists(f"{directory}/quests.txt"):
            with open(f"{directory}/quests.txt", "w") as f:
                f.write(quests_content)
                print(f"Created {directory}/quests.txt")
        
        if not os.path.exists(f"{directory}/items.txt"):
            with open(f"{directory}/items.txt", "w") as f:
                f.write(items_content)
                print(f"Created {directory}/items.txt")      
    except:
        print(f"Error creating default files")

    pass

# ============================================================================
# HELPER FUNCTIONS
# ============================================================================

def parse_quest_block(lines):
    """
    Parse a block of lines into a quest dictionary
    
    Args:
        lines: List of strings representing one quest
    
    Returns: Dictionary with quest data
    Raises: InvalidDataFormatError if parsing fails
    """
    # TODO: Implement parsing logic
    
    # Handle parsing errors gracefully
    data = {}
    
    try:
        for line in lines:
            if ": " not in line:
                raise InvalidDataFormatError(f"Missing colon separator in line: {line}")
            # Split each lin on ": " to get key-value pairs
            key, value = line.split(": ", 1)
            key = key.lower().strip()
            value = value.strip()
            
            # Convert numeric strings to integers
            if key in ['reward_xp', 'reward_gold', 'required_level']:
                if not value.isdigit():
                    raise InvalidDataFormatError(f"Value for {key} must be a number")
                value = int(value)
                
            data[key] = value
            
    except ValueError:
        raise InvalidDataFormatError("Error parsing quest block values.")
        
    return data
    pass

def parse_item_block(lines):
    """
    Parse a block of lines into an item dictionary
    
    Args:
        lines: List of strings representing one item
    
    Returns: Dictionary with item data
    Raises: InvalidDataFormatError if parsing fails
    """
    # TODO: Implement parsing logic
    data = {}
    
    try:
        for line in lines:
            if ": " not in line:
                raise InvalidDataFormatError(f"Missing colon separator in line")
                
            key, value = line.split(": ", 1)
            key = key.lower().strip()
            value = value.strip()
            
            # Type conversion
            if key == 'cost':
                if not value.isdigit():
                    raise InvalidDataFormatError(f"Value for cost must be a number")
                value = int(value)
                
            data[key] = value
            
    except ValueError:
        raise InvalidDataFormatError("Error parsing item block values.")
        
    return data
    pass

# ============================================================================
# TESTING
# ============================================================================

if __name__ == "__main__":
    print("=== GAME DATA MODULE TEST ===")
    
    # Test creating default files
    # create_default_data_files()
    
    # Test loading quests
    # try:
    #     quests = load_quests()
    #     print(f"Loaded {len(quests)} quests")
    # except MissingDataFileError:
    #     print("Quest file not found")
    # except InvalidDataFormatError as e:
    #     print(f"Invalid quest format: {e}")
    
    # Test loading items
    # try:
    #     items = load_items()
    #     print(f"Loaded {len(items)} items")
    # except MissingDataFileError:
    #     print("Item file not found")
    # except InvalidDataFormatError as e:
    #     print(f"Invalid item format: {e}")

