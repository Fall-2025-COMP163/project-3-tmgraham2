"""
COMP 163 - Project 3: Quest Chronicles
Combat System Module - Starter Code

Name: [Tashe Graham]

AI Usage: [Document any AI assistance used]

Handles combat mechanics
"""

from custom_exceptions import (
    InvalidTargetError,
    CombatNotActiveError,
    CharacterDeadError,
    AbilityOnCooldownError
)

# ============================================================================
# ENEMY DEFINITIONS
# ============================================================================

def create_enemy(enemy_type):
    """
    Create an enemy based on type
    
    Example enemy types and stats:
    - goblin: health=50, strength=8, magic=2, xp_reward=25, gold_reward=10
    - orc: health=80, strength=12, magic=5, xp_reward=50, gold_reward=25
    - dragon: health=200, strength=25, magic=15, xp_reward=200, gold_reward=100
    
    Returns: Enemy dictionary
    Raises: InvalidTargetError if enemy_type not recognized
    """
    # TODO: Implement enemy creation
    # Return dictionary with: name, health, max_health, strength, magic, xp_reward, gold_reward
    enemies = {
        'goblin': {
            'health': 50,
            'strength': 8,
            'magic': 2,
            'xp_reward': 25,
            'gold_reward': 10
        },
        'orc': {
            'health': 80,
            'strength': 12,
            'magic': 5,
            'xp_reward': 25,
            'gold_reward': 25
        },
        'dragon': {
            'health': 200,
            'strength': 25,
            'magic': 15,
            'xp_reward': 200,
            'gold_reward': 100
        }
    }
    enemy_key = enemy_type.lower()
    if enemy_key not in enemies:
        raise InvalidTargetError(f"Invalid enemy type.")
    
    template = enemies[enemy_key]

    enemy = {
        'name': enemy_type.capitalize(),
        'health': template['health'],
        'max_health': template['health'],
        'strength': template['strength'],
        'magic': template['magic'],
        'xp_reward': template['xp_reward'],
        'gold_reward': template['gold_reward']
    }

    return enemy
    pass

def get_random_enemy_for_level(character_level):
    if character_level <= 2:
         enemy_type = 'goblin'
    elif character_level <= 5:
        enemy_type = 'orc'
    else:
        enemy_type = 'dragon'
    
    return create_enemy(enemy_type)
         
     #Get an appropriate enemy for character's level
    
    #Level 1-2: Goblins
    #Level 3-5: Orcs
    #Level 6+: Dragons
    
    #Returns: Enemy dictionary
    
    # TODO: Implement level-appropriate enemy selection
    # Use if/elif/else to select enemy type
    # Call create_enemy with appropriate type
    pass
    

    


# ============================================================================
# COMBAT SYSTEM
# ============================================================================

class SimpleBattle:
    """
    Simple turn-based combat system
    
    Manages combat between character and enemy
    """
    
    def __init__(self, character, enemy):
        """Initialize battle with character and enemy"""
        self.character = character
        self.enemy = enemy
        self.combat_active = False
        self.turn_counter = 0
        # TODO: Implement initialization
        # Store character and enemy
        # Set combat_active flag
        # Initialize turn counter
        pass
    
    def start_battle(self):
        """
        Start the combat loop
        
        Returns: Dictionary with battle results:
                {'winner': 'player'|'enemy', 'xp_gained': int, 'gold_gained': int}
        
        Raises: CharacterDeadError if character is already dead
        """
        # TODO: Implement battle loop
        # Check character isn't dead
        if self.character['health'] <= 0:
            raise CharacterDeadError("Player is dead.")
        self.combat_active = True
        self.turn_counter = 1
        # Loop until someone dies
        while self.combat_active:
            if self.character['health'] <= 0 or self.enemy['health'] <= 0:
                break
            
        
        # Award XP and gold if player wins
        self.combat_active = False

        xp_gain = self.enemy['xp_reward']
        gold_gain = self.enemy['gold_reward']

        self.character['experience'] += xp_gain
        self.character['gold'] += gold_gain

        return {
            'winner': 'player',
            'xp_gained': xp_gain,
            'gold_gained': gold_gain
        }
        

        pass
    
    def player_turn(self):
        """
        Handle player's turn
        
        Displays options:
        1. Basic Attack
        2. Special Ability (if available)
        3. Try to Run
        
        Raises: CombatNotActiveError if called outside of battle
        """
        # TODO: Implement player turn
        # Check combat is active
        # Display options
        # Get player choice
        # Execute chosen action
        if not self.combat_active:
            raise CombatNotActiveError("Combat is not active.")
        
        print("1. Basic Attack")
        print("2. Special Ability (if available)")
        print("3. Try to Run")

        while True:
            choice = input("Choose action (1-3)")

            if choice == '1':
                #Basic attack
                damage = self.calculate_damage(self.character, self.enemy)
                self.enemy['health'] -= damage
                print(f"You attacked {self.enemy['name']} for {damage} damage!")
                 
            elif choice == '2':
                #Special ability
                cost = 5
                if self.character['magic'] >= cost:
                    self.character['magic'] -= cost
                    damage = damage * 1.5
                    self.enemy['health'] -= damage
                    print(f"Special ability was used on {self.enemy['name']} for {damage} damage!")
                else:
                    print("Not enough magic.")
            elif choice == '3':
                # Try to run (applicable if character has enough strength)
                if self.character['strength'] > 5:
                    print("You've successfully ran away")
                else:
                    print("You've failed to run away. Not enough strength.")




        pass
    
    def enemy_turn(self):
        """
        Handle enemy's turn - simple AI
        
        Enemy always attacks
        
        Raises: CombatNotActiveError if called outside of battle
        """
        # TODO: Implement enemy turn
        # Check combat is active
        # Calculate damage
        # Apply to character
        if not self.combat_active:
            raise CombatNotActiveError("Combat is not active.")
        # Damage calculation
        damage = self.calculate_damage(self.enemy, self.character)
        # Apply damage to character
        self.character['health'] -= damage
        print(f"{self.enemy['name']} has attacked you for {damage} damage!")
        
        pass
    
    def calculate_damage(self, attacker, defender):
        """
        Calculate damage from attack
        
        Damage formula: attacker['strength'] - (defender['strength'] // 4)
        Minimum damage: 1
        
        Returns: Integer damage amount
        """
        # TODO: Implement damage calculation
        damage = attacker['strength'] - (defender['strength'] // 4)
        return damage
        pass
    
    def apply_damage(self, target, damage):
        
        """
        Apply damage to a character or enemy
        
        Reduces health, prevents negative health
        """
        # TODO: Implement damage application
        # reduces health
        target['health'] -= damage
        # Prevents negative health
        if target['health'] < 0:
            target['health'] == 0
        pass
    
    def check_battle_end(self):
        
        
        """
        Check if battle is over
        
        Returns: 'player' if enemy dead, 'enemy' if character dead, None if ongoing
        """
        # TODO: Implement battle end check
        while self.combat_active is False:
            if self.enemy['health'] == 0:
                return 'player'
            elif self.character['health'] == 0:
                return 'enemy'
            else:
                return None

        pass
    
    def attempt_escape(self):
        import random
        """
        Try to escape from battle
        
        50% success chance
        
        Returns: True if escaped, False if failed
        """
        # TODO: Implement escape attempt
        # Use random number or simple calculation
        if random.random() < 0.5:
        # If successful, set combat_active to False
            self.combat_active = False
            return True
        return False

        pass

# ============================================================================
# SPECIAL ABILITIES
# ============================================================================

def use_special_ability(self, character, enemy):
    """
    Use character's class-specific special ability
    
    Example abilities by class:
    - Warrior: Power Strike (2x strength damage)
    - Mage: Fireball (2x magic damage)
    - Rogue: Critical Strike (3x strength damage, 50% chance)
    - Cleric: Heal (restore 30 health)
    
    Returns: String describing what happened
    Raises: AbilityOnCooldownError if ability was used recently
    """
    # TODO: Implement special abilities
    # Check character class
    # Execute appropriate ability
    # Track cooldowns (optional advanced feature)
    if self.cooldown > 0:
        raise AbilityOnCooldownError("Ability is on cooldown.")
    char_class = self.character.get('class')

    if char_class == 'Warrior':
        return "Power Strike has been used for 2x strength damage!"
    elif char_class == 'Mage':
        return "Fireball has been thrown for 2x magic damage!"
    elif char_class == 'Rogue':
        return "Crtical Strike has been used for 3x strength damage!"
    elif char_class == 'Cleric':
        return "Healing process is in effect."
    else:
        return "Invalid class"
    

    
    pass

def warrior_power_strike(character, enemy):
    """Warrior special ability"""
    # TODO: Implement power strike
    # Double strength damage
    damage = character['strength'] * 2
    enemy['health'] -= damage
    pass

def mage_fireball(character, enemy):
    """Mage special ability"""
    # TODO: Implement fireball
    # Double magic damage
    damage = character['magic'] * 2
    enemy['health'] -= damage
    pass

def rogue_critical_strike(character, enemy):
    import random
    """Rogue special ability"""
    # TODO: Implement critical strike
    # 50% chance for triple damage
    if random.random() < 0.5:
        damage = character['strength'] * 3
        enemy['health'] -= damage
    else:
        print("Your ROGUE STRIKE has missed the target!")
    pass

def cleric_heal(character):
    """Cleric special ability"""
    # TODO: Implement healing
    # Restore 30 HP (not exceeding max_health)
    pass

# ============================================================================
# COMBAT UTILITIES
# ============================================================================

def can_character_fight(character):
    """
    Check if character is in condition to fight
    
    Returns: True if health > 0 and not in battle
    """
    # TODO: Implement fight check
    if character['health'] > 0:
        return True
    pass

def get_victory_rewards(enemy):
    """
    Calculate rewards for defeating enemy
    
    Returns: Dictionary with 'xp' and 'gold'
    """
    # TODO: Implement reward calculation
    # Ensures enemy is defeated
    if enemy['health'] <= 0:
        character_xp += enemy['xp_reward']
        character_gold += enemy['gold_reward']
        return {
            'xp': character_xp,
            'gold': character_gold
        }
        
        
    pass

def display_combat_stats(character, enemy):
    """
    Display current combat status
    
    Shows both character and enemy health/stats
    """
    # TODO: Implement status display
    print(f"\n{character['name']}: HP={character['health']}/{character['max_health']}")
    print(f"{enemy['name']}: HP={enemy['health']}/{enemy['max_health']}")
    pass

def display_battle_log(message):
    """
    Display a formatted battle message
    """
    # TODO: Implement battle log display
    print(f">>> {message}")
    pass

# ============================================================================
# TESTING
# ============================================================================

if __name__ == "__main__":
    print("=== COMBAT SYSTEM TEST ===")
    
    # Test enemy creation
    try:
        goblin = create_enemy("goblin")
        print(f"Created {goblin['name']}")
    except InvalidTargetError as e:
        print(f"Invalid enemy: {e}")
    
    # Test battle
    test_char = {
        'name': 'Hero',
        'class': 'Warrior',
        'health': 120,
        'max_health': 120,
        'strength': 15,
        'magic': 5
     }
    #
    battle = SimpleBattle(test_char, goblin)
    try:
        result = battle.start_battle()
        print(f"Battle result: {result}")
    except CharacterDeadError:
        print("Character is dead!")

