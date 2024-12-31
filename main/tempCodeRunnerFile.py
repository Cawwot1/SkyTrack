import requests

# Replace with your Skyblock API key
API_KEY = "601aad2c-a1d6-4461-b288-ced32af5f8db"

# Skyblock API endpoint
BASE_URL = "https://api.hypixel.net/v2/skyblock/profile"

# Function to test the API
def test_skyblock_api():
    params = {
        'key': API_KEY,
    }
    
    # Make the request to the Skyblock API
    response = requests.get(BASE_URL, params=params)
    
    # Check if the request was successful
    if response.status_code == 200:
        data = response.json()
        print("API Response:")
        print(data)
    else:
        print(f"Error: {response.status_code}")
        # Print the response text to help debug
        print("Response text:", response.text)

if __name__ == "__main__":
    test_skyblock_api()