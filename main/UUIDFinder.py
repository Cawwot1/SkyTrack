import requests

PLAYER_NAME = "BankInterest"

def get_player_uuid(player_name):
    url = f"https://api.mojang.com/users/profiles/minecraft/{player_name}"
    response = requests.get(url)

    if response.status_code == 200:
        data = response.json()
        return data['id']  # This returns the player's UUID
    else:
        return None

# Example usage
player_name = PLAYER_NAME  # Replace with the actual player's name
uuid = get_player_uuid(player_name)
if uuid:
    print(f"Player UUID: {uuid}")
else:
    print("Player not found.")
