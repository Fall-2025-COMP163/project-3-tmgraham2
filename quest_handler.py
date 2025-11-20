"""
COMP 163 - Project 3: Quest Chronicles
Quest Handler Module - Starter Code

Name: [Tashe Graham]

AI Usage: [Document any AI assistance used]

This module handles quest management, dependencies, and completion.
"""

from custom_exceptions import (
    QuestNotFoundError,
    QuestRequirementsNotMetError,
    QuestAlreadyCompletedError,
    QuestNotActiveError,
    InsufficientLevelError
)

# ============================================================================
# QUEST MANAGEMENT
# ============================================================================
def accept_quest(character, quest_id, quest_data_dict):
    """
    Accept a new quest
    
    Args:
        character: Character dictionary
        quest_id: Quest to accept
        quest_data_dict: Dictionary of all quest data
    
    Requirements to accept quest:
    - Character level >= quest required_level
    - Prerequisite quest completed (if any)
    - Quest not already completed
    - Quest not already active
    
    Returns: True if quest accepted
    Raises:
        QuestNotFoundError if quest_id not in quest_data_dict
        InsufficientLevelError if character level too low
        QuestRequirementsNotMetError if prerequisite not completed
        QuestAlreadyCompletedError if quest already done
    """
    # TODO: Implement quest acceptance
    # Check quest exists
    if quest_id not in quest_data_dict:
        raise QuestNotFoundError("Quest does not exist.")
    quest = quest_data_dict[quest_id]
    # Check level requirement
    if character.get('level', 1) < quest.get('required_level', 1):
        raise InsufficientLevelError(f"Level {quest['required_level']} required.")
    # Check prerequisite (if not "NONE")
    prereq_id = quest.get('prerequisite', 'NONE')
    if prereq_id != "NONE":
        if prereq_id not in character['completed_quests']:
            raise QuestRequirementsNotMetError(f"Prerequisite quest '{prereq_id}' not completed.")
    # Check not already completed
    if quest_id in character['completed_quests']:
        raise QuestAlreadyCompletedError("Quest already completed.")
    # Check not already active
    if quest_id in character['active_quests']:
        return False
    # Add to character['active_quests']
    character['active_quests'].append(quest_id)
    return True
    pass

def complete_quest(character, quest_id, quest_data_dict):
    """
    Complete an active quest and grant rewards
    
    Args:
        character: Character dictionary
        quest_id: Quest to complete
        quest_data_dict: Dictionary of all quest data
    
    Rewards:
    - Experience points (reward_xp)
    - Gold (reward_gold)
    
    Returns: Dictionary with reward information
    Raises:
        QuestNotFoundError if quest_id not in quest_data_dict
        QuestNotActiveError if quest not in active_quests
    """
    # TODO: Implement quest completion
    # Check quest exists
    if quest_id not in quest_data_dict:
        raise QuestNotFoundError(f"Quest '{quest_id}' does not exist.")
    # Check quest is active
    if quest_id not in character['active_quests']:
        raise QuestNotActiveError(f"Quest '{quest_id}' is not currently active.")
    # Remove from active_quests
    character['active_quests'].remove(quest_id)
    # Add to completed_quests
    character['completed_quests'].append(quest_id)
    # Grant rewards (use character_manager.gain_experience and add_gold)
    quest = quest_data_dict[quest_id]
    xp_reward = quest.get('reward_xp', 0)
    gold_reward = quest.get('reward_gold', 0)
    character['experience'] = character.get('experience', 0) + xp_reward
    character['gold'] = character.get('gold', 0) + gold_reward
    # Return reward summary
    return {
        "quest_id": quest_id,
        "xp_gained": xp_reward,
        "gold_gained": gold_reward,
        "status": "COMPLETED"
    }

    pass

def abandon_quest(character, quest_id):
    """
    Remove a quest from active quests without completing it
    
    Returns: True if abandoned
    Raises: QuestNotActiveError if quest not active
    """
    # TODO: Implement quest abandonment
    if quest_id not in character['active_quests']:
        raise QuestNotActiveError(f"Cannot abandon quest '{quest_id}' because it is not active.")
    
    character['active_quests'].remove(quest_id)
    return True
    pass

def get_active_quests(character, quest_data_dict):
    """
    Get full data for all active quests
    
    Returns: List of quest dictionaries for active quests
    """
    # TODO: Implement active quest retrieval
    # Look up each quest_id in character['active_quests']
    # Return list of full quest data dictionaries
    active_data = []
    for q_id in character['active_quests']:
        if q_id in quest_data_dict:
            quest_info = quest_data_dict[q_id].copy()
            quest_info['id'] = q_id
            active_data.append(quest_info)
    return active_data
    pass

def get_completed_quests(character, quest_data_dict):
    """
    Get full data for all completed quests
    
    Returns: List of quest dictionaries for completed quests
    """
    # TODO: Implement completed quest retrieval
    completed_data = []
    for q_id in character['completed_quests']:
        if q_id in quest_data_dict:
            quest_info = quest_data_dict[q_id].copy()
            quest_info['id'] = q_id
            completed_data.append(quest_info)
    return completed_data
    pass

def get_available_quests(character, quest_data_dict):
    """
    Get quests that character can currently accept
    
    Available = meets level req + prerequisite done + not completed + not active
    
    Returns: List of quest dictionaries
    """
    # TODO: Implement available quest search
    # Filter all quests by requirements
    available = []
    
    for q_id, q_data in quest_data_dict.items():
        # We can reuse our helper function 'can_accept_quest' here!
        if can_accept_quest(character, q_id, quest_data_dict):
            quest_info = q_data.copy()
            quest_info['id'] = q_id
            available.append(quest_info)
            
    return available
    pass

# ============================================================================
# QUEST TRACKING
# ============================================================================

def is_quest_completed(character, quest_id):
    """
    Check if a specific quest has been completed
    
    Returns: True if completed, False otherwise
    """
    # TODO: Implement completion check
    return quest_id in character.get('completed_quests', [])
    pass

def is_quest_active(character, quest_id):
    """
    Check if a specific quest is currently active
    
    Returns: True if active, False otherwise
    """
    # TODO: Implement active check
    return quest_id in character.get('active_quests', [])
    pass

def can_accept_quest(character, quest_id, quest_data_dict):
    """
    Check if character meets all requirements to accept quest
    
    Returns: True if can accept, False otherwise
    Does NOT raise exceptions - just returns boolean
    """
    # TODO: Implement requirement checking
    # Check all requirements without raising exceptions
    # Check existence
    if quest_id not in quest_data_dict:
        return False
    
    quest = quest_data_dict[quest_id]
    
    # Check active/completed status
    if is_quest_active(character, quest_id) or is_quest_completed(character, quest_id):
        return False
        
    # Check Level
    if character.get('level', 1) < quest.get('required_level', 1):
        return False
        
    # Check Prerequisite
    prereq = quest.get('prerequisite', 'NONE')
    if prereq != "NONE":
        if not is_quest_completed(character, prereq):
            return False
            
    return True
    pass

def get_quest_prerequisite_chain(quest_id, quest_data_dict):
    """
    Get the full chain of prerequisites for a quest
    
    Returns: List of quest IDs in order [earliest_prereq, ..., quest_id]
    Example: If Quest C requires Quest B, which requires Quest A:
             Returns ["quest_a", "quest_b", "quest_c"]
    
    Raises: QuestNotFoundError if quest doesn't exist
    """
    # TODO: Implement prerequisite chain tracing
    # Follow prerequisite links backwards
    # Build list in reverse order
    if quest_id not in quest_data_dict:
        raise QuestNotFoundError(f"Quest '{quest_id}' not found.")
        
    # Start with the target quest
    chain = [quest_id]
    current_id = quest_id
    
    while True:
        
        if current_id not in quest_data_dict:
            break 
            
        prereq = quest_data_dict[current_id].get('prerequisite', 'NONE')
        
        if prereq == "NONE":
            break
            
        
        chain.append(prereq)
        current_id = prereq
    
    chain.reverse[-1]
    
    return chain
    pass

# ============================================================================
# QUEST STATISTICS
# ============================================================================

def get_quest_completion_percentage(character, quest_data_dict):
    """
    Calculate what percentage of all quests have been completed
    
    Returns: Float between 0 and 100
    """
    # TODO: Implement percentage calculation
    # total_quests = len(quest_data_dict)
    total_quests = len(quest_data_dict)
    # completed_quests = len(character['completed_quests'])
    completed_quests = len(character.get('completed_quests', []))
    # percentage = (completed / total) * 100
    percentage = (completed_quests / total_quests) * 100
    return percentage

    pass

def get_total_quest_rewards_earned(character, quest_data_dict):
    """
    Calculate total XP and gold earned from completed quests
    
    Returns: Dictionary with 'total_xp' and 'total_gold'
    """
    # TODO: Implement reward calculation
    # Sum up reward_xp and reward_gold for all completed quests
    totals = {
        "total_xp": 0,
        "total_gold": 0
    }
    
    for quest_id in character.get('completed_quests', []):
        
        if quest_id in quest_data_dict:
            quest = quest_data_dict[quest_id]
            totals['total_xp'] += quest.get('reward_xp', 0)
            totals['total_gold'] += quest.get('reward_gold', 0)
            
    return totals
    pass

def get_quests_by_level(quest_data_dict, min_level, max_level):
    """
    Get all quests within a level range
    
    Returns: List of quest dictionaries
    """
    # TODO: Implement level filtering
    matching_quests = []
    
    for quest_id, quest_data in quest_data_dict.items():
        req_level = quest_data.get('required_level', 1)
        
        if min_level <= req_level <= max_level:
            # Copy to create the ID inside the dict for easier display
            q_copy = quest_data.copy()
            q_copy['id'] = quest_id
            matching_quests.append(q_copy)
            
    return matching_quests
    pass

# ============================================================================
# DISPLAY FUNCTIONS
# ============================================================================

def display_quest_info(quest_data):
    """
    Display formatted quest information
    
    Shows: Title, Description, Rewards, Requirements
    """
    # TODO: Implement quest display
    print(f"\n=== {quest_data['title']} ===")
    print(f"Description: {quest_data['description']}")
    # ... etc
    print(f"Level Required: {quest_data.get('required_level', 1)}")
    # Get prerequisites
    prereq = quest_data.get('prerequisite', 'NONE')
    print(f"Prerequisite: {prereq}")
    
    print("-" * 20)
    print(f"Rewards: {quest_data.get('reward_xp', 0)} XP | {quest_data.get('reward_gold', 0)} Gold")
    print("=" * 20)
    pass

def display_quest_list(quest_list):
    """
    Display a list of quests in summary format
    
    Shows: Title, Required Level, Rewards
    """
    # TODO: Implement quest list display
    if not quest_list:
        print("\nNo quests found.")
        return

    print(f"\n{'ID':<15} | {'Lvl':<3} | {'Title':<30} | {'Rewards'}")
    print("-" * 70)
    
    for q in quest_list:
        q_id = q.get('id', 'unknown')
        lvl = q.get('required_level', 1)
        title = q.get('title', 'Untitled')
        xp = q.get('reward_xp', 0)
        gold = q.get('reward_gold', 0)
        print(f"{q_id:<15} | {lvl:<3} | {title:<30} | {xp} XP, {gold}g")
    pass

def display_character_quest_progress(character, quest_data_dict):
    """
    Display character's quest statistics and progress
    
    Shows:
    - Active quests count
    - Completed quests count
    - Completion percentage
    - Total rewards earned
    """
    # TODO: Implement progress display
    # Calculate stats
    active_count = len(character.get('active_quests', []))
    completed_count = len(character.get('completed_quests', []))
    percent = get_quest_completion_percentage(character, quest_data_dict)
    rewards = get_total_quest_rewards_earned(character, quest_data_dict)

    # Output
    print("\n=== QUEST PROGRESS ===")
    print(f"Active Quests:    {active_count}")
    print(f"Completed Quests: {completed_count}")
    print(f"Completion:       {percent}%")
    print("-" * 30)
    print(f"Total History Earned: {rewards['total_xp']} XP | {rewards['total_gold']} Gold")
    print("==============================")
    pass

# ============================================================================
# VALIDATION
# ============================================================================

def validate_quest_prerequisites(quest_data_dict):
    """
    Validate that all quest prerequisites exist
    
    Checks that every prerequisite (that's not "NONE") refers to a real quest
    
    Returns: True if all valid
    Raises: QuestNotFoundError if invalid prerequisite found
    """
    # TODO: Implement prerequisite validation
    # Check each quest's prerequisite
    for quest_id, quest_data in quest_data_dict.items():
        prereq_id = quest_data.get('prerequisite', 'NONE')
        
        # Ignore if there is no prerequisite
        if prereq_id == "NONE":
            continue
    # Ensure prerequisite exists in quest_data_dict
    if prereq_id not in quest_data_dict:
            raise QuestNotFoundError(
                "Invalid prerequisite was found")
            
    return True
    pass


# ============================================================================
# TESTING
# ============================================================================

if __name__ == "__main__":
    print("=== QUEST HANDLER TEST ===")
    
    # Test data
    # test_char = {
    #     'level': 1,
    #     'active_quests': [],
    #     'completed_quests': [],
    #     'experience': 0,
    #     'gold': 100
    # }
    #
    # test_quests = {
    #     'first_quest': {
    #         'quest_id': 'first_quest',
    #         'title': 'First Steps',
    #         'description': 'Complete your first quest',
    #         'reward_xp': 50,
    #         'reward_gold': 25,
    #         'required_level': 1,
    #         'prerequisite': 'NONE'
    #     }
    # }
    #
    # try:
    #     accept_quest(test_char, 'first_quest', test_quests)
    #     print("Quest accepted!")
    # except QuestRequirementsNotMetError as e:
    #     print(f"Cannot accept: {e}")

