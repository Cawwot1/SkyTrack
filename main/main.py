import requests

# TEMP KEY
API_KEY = "601aad2c-a1d6-4461-b288-ced32af5f8db"
BASE_URL = "https://api.hypixel.net/v2/skyblock"
player_uuid = 'd874fac3f59d44fab9389f240674bc59' #UUID for Cawwot1

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

    """
    Profile Specifics
    """