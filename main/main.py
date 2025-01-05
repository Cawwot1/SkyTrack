import requests
import json

# TEMP KEY
API_KEY = "8123cc0b-42aa-4ab6-a022-9802ff7eb1b4"
BASE_URL = "https://api.hypixel.net/v2/skyblock"
player_uuid = '421ef1ee18854aeb933910160ac19f79' #UUID for BankInterest

#Finds profiles of the player
def get_skyblock_profiles(player_uuid):
    url = f"{BASE_URL}/profiles?key={API_KEY}&uuid={player_uuid}"
    response = requests.get(url)
    
    # Check for success
    if response.status_code == 200:
        data = response.json()
        profiles = data.get('profiles', [])
        
        return profiles
    else:
        print(f"Error: {response.status_code}")
        return None

#USE LATER
def profile_selector(cute_name):
    if profiles:
        for profile in profiles:
            if profile['cute_name'] == cute_name:
                return profile
    else:
        return None

if __name__ == "__main__":
    
    """
    Obtaining Player Profiles
    """

    #Gets all profile based on Player UUID
    profiles = get_skyblock_profiles(player_uuid)   

    ### TEMP DISPLAY (REMOVE ONCE FRONTEND COMPLETE) - prints out all the diffent profiles the player has
    for profile in profiles:
        print(f"Profile ID: {profile['profile_id']}, Name: {profile['cute_name']}")

    """
    Choosing Profile
    """

    #Gets profile that the user wants to select (based on cute_name)
    chosen_profile_name = input("Which profile do you want to access? ")

    chosen_profile = profile_selector(chosen_profile_name)

    if chosen_profile == None: #Choosing profile fuction
        print("No profiles found")
    else:
        print(f"Chosen {chosen_profile_name} profile")

    #TEST
    with open('output.json', 'w') as file:
        json.dump(chosen_profile, file, indent=4)

    """
    Profile Specifics - SKILLS
    """

    ###pre-output operations

    #structure for skill xp retrival chosen_profile (retrived from Hypixel API)
    exp_base = chosen_profile["members"][player_uuid]["player_data"]["experience"]

    #Creates new local foldered ditionary (dictionaries in dictionaries) for player skill xp
    skill_dict = {
    "combat": {
        "level": 0,
        "total_xp": exp_base["SKILL_COMBAT"],
        "current_xp": "",
        "next_threshold": ""
    },
    "enchanting": {
        "level": 0,
        "total_xp": exp_base["SKILL_ENCHANTING"],
        "current_xp": "",
        "next_threshold": ""
    },
    "farming": {
        "level": 0,
        "total_xp": exp_base["SKILL_FARMING"],
        "current_xp": "",
        "next_threshold": ""
    },
    "fishing": {
        "level": 0,
        "total_xp": exp_base["SKILL_FISHING"],
        "current_xp": "",
        "next_threshold": ""
    },
    "alchemy": {
        "level": 0,
        "total_xp": exp_base["SKILL_ALCHEMY"],
        "current_xp": "",
        "next_threshold": ""
    },
    "mining": {
        "level": 0,
        "total_xp": exp_base["SKILL_MINING"],
        "current_xp": "",
        "next_threshold": ""
    },
    "taming": {
        "level": 0,
        "total_xp": exp_base["SKILL_TAMING"],
        "current_xp": "",
        "next_threshold": ""
    },
    "foraging": {
        "level": 0,
        "total_xp": exp_base["SKILL_FORAGING"],
        "current_xp": "",
        "next_threshold": ""
    },
    "social": {
        "level": 0,
        "total_xp": exp_base["SKILL_SOCIAL"],
        "current_xp": "",
        "next_threshold": ""
    },
    # Skipping Runecrafting and Carpentry as requested
     "runecraft": {
        "level": 0,
        "total_xp": exp_base["SKILL_RUNECRAFTING"],
        "current_xp": "",
        "next_threshold": ""
    },
    "carpentry": {
        "level": 0,
        "total_xp": exp_base["SKILL_CARPENTRY"],
        "current_xp": "",
        "next_threshold": ""
    }
    }
    
    #Skill-Level Calculator (except dungoens & cosmetic)
    def get_skill_level(xp):
        level = 0
        next_threshold = None  # Default value in case xp is greater than the last threshold
        for lvl, threshold in xp_thresholds:
            print(xp)          # Debugging to see current xp
            print(threshold)   # Debugging to see threshold value
            print(level)       # Debugging to see current level
            if xp >= threshold:
                level = lvl
                xp -= threshold
            else:
                next_threshold = threshold
                break

        # Return level, the remaining xp, and the next threshold (if available)
        return level, xp, next_threshold

    
    #XP thresholds for each level
    xp_thresholds = [(0, 0), (1, 50), (2, 125), (3, 200), (4, 300), (5, 500), (6, 750), (7, 1000), (8, 1500), 
    (9, 2000), (10, 3500), (11, 5000), (12, 7500), (13, 10000), (14, 15000), (15, 20000), 
    (16, 30000), (17, 50000), (18, 75000), (19, 100000), (20, 200000), (21, 300000), 
    (22, 400000), (23, 500000), (24, 600000), (25, 700000), (26, 800000), (27, 900000), 
    (28, 1000000), (29, 1100000), (30, 1200000), (31, 1300000), (32, 1400000), (33, 1500000), 
    (34, 1600000), (35, 1700000), (36, 1800000), (37, 1900000), (38, 2000000), (39, 2100000), 
    (40, 2200000), (41, 2300000), (42, 2400000), (43, 2500000), (44, 2600000), (45, 2750000), 
    (46, 2900000), (47, 3100000), (48, 3400000), (49, 3700000), (50, 4000000), (51, 4300000), 
    (52, 4600000), (53, 4900000), (54, 5200000), (55, 5500000), (56, 5800000), (57, 6100000), 
    (58, 6400000), (59, 6700000), (60, 7000000)]


    # Calculate and store levels for each skill (excluding social, runecraft & dungeons)
    for skill, data in skill_dict.items():
        print(skill)
        print(data)
        if skill not in ["social", "runecraft", "dungeon", "carpentry", 'fishing', 'farming']:
            skill_dict[skill]['level'], skill_dict[skill]["current_xp"], skill_dict[skill]["next_threshold"] = get_skill_level(data['total_xp'])
        else:
            pass

    print(
        f"\n--Profile Skills--",
        f"\nCombat Level: {skill_dict['combat']['level']} ({skill_dict['combat']['total_xp']} total xp) -> {skill_dict['combat']['current_xp']} / {skill_dict['combat']['next_threshold']}"
    )

