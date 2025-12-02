"""
COMP 163 - Project 3: Quest Chronicles
Inventory System Module - Starter Code

Name: [Your Name Here]

AI Usage: [Document any AI assistance used]

This module handles inventory management, item usage, and equipment.
"""

from custom_exceptions import (
    InventoryFullError,
    ItemNotFoundError,
    InsufficientResourcesError,
    InvalidItemTypeError
)

# Maximum inventory size
MAX_INVENTORY_SIZE = 20

# ============================================================================
# INVENTORY MANAGEMENT
# ============================================================================

def add_item_to_inventory(character, item_id):
    """
    Add an item to character's inventory
    
    Args:
        character: Character dictionary
        item_id: Unique item identifier
    
    Returns: True if added successfully
    Raises: InventoryFullError if inventory is at max capacity
    """
    if 'inventory' not in character:
        character['inventory'] = []
    # TODO: Implement adding items
    # Check if inventory is full (>= MAX_INVENTORY_SIZE)
    if len(character['inventory']) >= MAX_INVENTORY_SIZE:
        raise InventoryFullError("Inventory is full!")
    # Add item_id to character['inventory'] list
    character['inventory'].append(item_id)
    return True

    pass

def remove_item_from_inventory(character, item_id):
    """
    Remove an item from character's inventory
    
    Args:
        character: Character dictionary
        item_id: Item to remove
    
    Returns: True if removed successfully
    Raises: ItemNotFoundError if item not in inventory
    """
    # TODO: Implement item removal
    inventory = character.get('inventory', [])
    # Check if item exists in inventory
    if item_id not in inventory:
        raise ItemNotFoundError(f"Item {item_id} not found.")
    # Remove item from list
    character['inventory'].remove(item_id)
    return True
    pass

def has_item(character, item_id):
    """
    Check if character has a specific item
    
    Returns: True if item in inventory, False otherwise
    """
    # TODO: Implement item check
    return item_id in character.get('inventory', [])
    pass

def count_item(character, item_id):
    """
    Count how many of a specific item the character has
    
    Returns: Integer count of item
    """
    # TODO: Implement item counting
    
    inventory = character.get('inventory', [])
    # Use list.count() method
    return inventory.count(item_id)
    pass

def get_inventory_space_remaining(character):
    """
    Calculate how many more items can fit in inventory
    
    Returns: Integer representing available slots
    """
    # TODO: Implement space calculation
    current_count = len(character.get('inventory', []))
    return MAX_INVENTORY_SIZE - current_count
    pass

def clear_inventory(character):
    """
    Remove all items from inventory
    
    Returns: List of removed items
    """
    # TODO: Implement inventory clearing
    inventory = character.get('inventory', [])
    # Save current inventory before clearing
    removed_items = inventory.copy()
    # Clear character's inventory list
    inventory.clear()
    return removed_items
    pass

# ============================================================================
# ITEM USAGE
# ============================================================================

def use_item(character, item_id, item_data):
    """
    Use a consumable item from inventory
    
    Args:
        character: Character dictionary
        item_id: Item to use
        item_data: Item information dictionary from game_data
    
    Item types and effects:
    - consumable: Apply effect and remove from inventory
    - weapon/armor: Cannot be "used", only equipped
    
    Returns: String describing what happened
    Raises: 
        ItemNotFoundError if item not in inventory
        InvalidItemTypeError if item type is not 'consumable'
    """
    # TODO: Implement item usage
    # Check if character has the item
    if not has_item(character, item_id):
        raise ItemNotFoundError("You do not have {item_id}.")
    # Check if item type is 'consumable'
    if item_data.get('type') != 'consumable':
        raise InvalidItemTypeError(f"{item_data} cannot be used.")
    # Parse effect (format: "stat_name:value" e.g., "health:20")
    effect_str = item_data.get('effect', '')

    try:
        stat_name, value = effect_str.split(':')
        value = int(value)
    except ValueError:
        return f"Item {item_id} has invalid effect data."

    # Apply effect to character
    current_stat = character.get(stat_name, 0)
    character[stat_name] = current_stat + value
    # Remove item from inventory
    remove_item_from_inventory(character, item_id)
    return f"Used {item_id}. {stat_name} increased by {value}."
    pass

def equip_weapon(character, item_id, item_data):

    # TODO: Implement weapon equipping
    # Check item exists and is type 'weapon'
    if item_id not in character["inventory"]:
        raise ItemNotFoundError(f"Weapon '{item_id}' not found in inventory")

    # Ensure the item type is 'weapon'
    if item_data.get("type") != "weapon":
        raise InvalidItemTypeError(f"Item '{item_id}' is not a weapon")

    # If the character already has a weapon equipped, unequip weapon
    old_weapon_id = character.get("equipped_weapon")
    if old_weapon_id:
        unequip_weapon(character)
        character["inventory"].append(old_weapon_id)

    # Equip the new weapon
    character["equipped_weapon"] = item_id

    # Apply weapon effects 
    effect = item_data.get("effect")
    if effect:
        stat, value = effect.split(":")
        value = int(value)
        if stat in character:
            character[stat] += value

    # Remove the weapon from inventory 
    character["inventory"].remove(item_id)

    return f"{character['name']} has equipped {item_id}"
    
    

def equip_armor(character, item_id, item_data):
    # TODO: Implement armor equipping
    # Similar to equip_weapon but for armor
    if item_id not in character["inventory"]:
        raise ItemNotFoundError(f"Armor '{item_id}' not found in inventory")

    item = item_data

    # Must be armor
    if item["type"] != "armor":
        raise InvalidItemTypeError(f"Item '{item_id}' is not armor")

    # If armor already equipped, remove its effect 
    if character.get("equipped_armor"):
        old_armor = character["equipped_armor"]
        old_data = item_data[old_armor]
        stat, value = old_data["effect"].split(":")
        character[stat] -= int(value)

        # Return old armor to inventory
        character["inventory"].append(old_armor)

    # Apply new armor effect
    stat, value = item["effect"].split(":")
    character[stat] += int(value)

    # Set equipped armor
    character["equipped_armor"] = item_id

    # Remove from inventory
    character["inventory"].remove(item_id)

    return f"Equipped {item_id}, {stat} increased by {value}"

def unequip_weapon(character):
   
    # TODO: Implement weapon unequipping
    equipped = character.get("equipped_weapon")
    # Check if weapon is equipped
    if not equipped:
        return None  # nothing to unequip
    if get_inventory_space_remaining(character) <= 0:
        raise InventoryFullError("Inventory is full")

    weapon_data = item_data[equipped]
    stat, value = weapon_data["effect"].split(":")
    # Remove stat bonuses
    character[stat] -= int(value)  

    # Add weapon back to inventory
    character["inventory"].append(equipped)
    # Clear equipped_weapon from character
    character["equipped_weapon"] = None

    return equipped

def unequip_armor(character):
    """
    Remove equipped armor and return it to inventory
    
    Returns: Item ID that was unequipped, or None if no armor equipped
    Raises: InventoryFullError if inventory is full
    """
    # TODO: Implement armor unequipping
    equipped = character.get("equipped_armor")

    if not equipped:
        return None

    if get_inventory_space_remaining(character) <= 0:
        raise InventoryFullError("Inventory is full")

    armor_data = item_data[equipped]
    stat, value = armor_data["effect"].split(":")
    # Remove stat bonuses
    character[stat] -= int(value)

    character["inventory"].append(equipped)
    # Clear equipped status
    character["equipped_armor"] = None

    return equipped
  

# ============================================================================
# SHOP SYSTEM
# ============================================================================

def purchase_item(character, item_id, item_data):
    """
    Purchase an item from a shop
    
    Args:
        character: Character dictionary
        item_id: Item to purchase
        item_data: Item information with 'cost' field
    
    Returns: True if purchased successfully
    Raises:
        InsufficientResourcesError if not enough gold
        InventoryFullError if inventory is full
    """
    # TODO: Implement purchasing
    cost = item_data.get('cost', 0)
    current_gold = character.get('gold', 0)
    # Check if character has enough gold
    if current_gold < cost:
        raise InsufficientResourcesError(f"Not enough gold.")
    # Check if inventory has space
    if get_inventory_space_remaining(character) <= 0:
        raise InventoryFullError("Cannot purchase: Inventory is full.")
    # Subtract gold from character
    character['gold'] = current_gold - cost
    # Add item to inventory
    add_item_to_inventory(character, item_id)
    
    return True
    pass

def sell_item(character, item_id, item_data):
    """
    Sell an item for half its purchase cost
    
    Args:
        character: Character dictionary
        item_id: Item to sell
        item_data: Item information with 'cost' field
    
    Returns: Amount of gold received
    Raises: ItemNotFoundError if item not in inventory
    """
    # TODO: Implement selling
    # Check if character has item
    if not has_item(character, item_id):
         raise ItemNotFoundError(f"Cannot sell {item_id}: Item not found.")
    # Calculate sell price (cost // 2)
    cost = item_data.get('cost', 0)
    sell_price = cost // 2
    # Remove item from inventory
    remove_item_from_inventory(character, item_id)
    # Add gold to character
    current_gold = character.get('gold', 0)
    character['gold'] = current_gold + sell_price

    return sell_price
    pass

# ============================================================================
# HELPER FUNCTIONS
# ============================================================================

def parse_item_effect(effect_string):
    """
    Parse item effect string into stat name and value
    
    Args:
        effect_string: String in format "stat_name:value"
    
    Returns: Tuple of (stat_name, value)
    Example: "health:20" → ("health", 20)
    """
    # TODO: Implement effect parsing
    if not effect_string or ":" not in effect_string:
        return None
    # Split on ":"
    try:
        stat_name, value_str = effect_string.split(':')
        return stat_name, int(value_str)
    except ValueError:
        # Handle cases where value isn't an integer
        return None
    # Convert value to integer
    pass

def apply_stat_effect(character, stat_name, value):
    """
    Apply a stat modification to character
    
    Valid stats: health, max_health, strength, magic
    
    Note: health cannot exceed max_health
    """
    # TODO: Implement stat application
    # Add value to character[stat_name]
    # If stat is health, ensure it doesn't exceed max_health
    if not stat_name:
        return

    current_val = character.get(stat_name, 0)
    new_val = current_val + value
    
    # Special handling for health
    if stat_name == 'health':
        max_health = character.get('max_health', 100) # Default to 100 if missing
        if new_val > max_health:
            new_val = max_health
        elif new_val < 0:
            new_val = 0

    character[stat_name] = new_val
    pass

def display_inventory(character, item_data_dict):
    """
    Display character's inventory in formatted way
    
    Args:
        character: Character dictionary
        item_data_dict: Dictionary of all item data
    
    Shows item names, types, and quantities
    """
    # TODO: Implement inventory display
    inventory = character.get('inventory', [])
    gold = character.get('gold', 0)

    print(f"\n=== {character.get('name', 'Hero')}'s Inventory ===")
    print(f"Gold: {gold}")

    if not inventory:
        print(" (Empty)")
        print("=" * 30)
        return
    # Count items (some may appear multiple times)
    item_counts = {}
    for item_id in inventory:
        if item_id in item_counts:
            item_counts[item_id] += 1
        else:
            item_counts[item_id] = 1

    # Display with item names from item_data_dict
    for item_id, count in item_counts.items():
        # Get readable name from game data, fallback to ID if missing
        item_info = item_data_dict.get(item_id, {})
        display_name = item_info.get('name', item_id)
        item_type = item_info.get('type', 'unknown')
        
        print(f"- {display_name} (x{count}) [{item_type}]")
    pass

# ============================================================================
# TESTING
# ============================================================================

if __name__ == "__main__":
    print("=== INVENTORY SYSTEM TEST ===")
    
    # Test adding items
    test_char = {'inventory': [], 'gold': 100, 'health': 80, 'max_health': 80}
    # 
    try:
        add_item_to_inventory(test_char, "health_potion")
        print(f"Inventory: {test_char['inventory']}")
    except InventoryFullError:
        print("Inventory is full!")
    
    # Test using items
    test_item = {
        'item_id': 'health_potion',
        'type': 'consumable',
        'effect': 'health:20'
     }
    # 
    try:
        result = use_item(test_char, "health_potion", test_item)
        print(result)
    except ItemNotFoundError:
        print("Item not found")

