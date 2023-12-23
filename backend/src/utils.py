import requests

def get_coordinates(address):
    base_url = f"https://geocode.xyz/"
    params = {
        "auth": "60218117238076427679x24940",
        "locate": address,
        "region":"MY",
        "json": 1
    }

    response = requests.get(base_url, params=params)
    
    if response.status_code == 200:
        data = response.json()
        if data:
           if "latt" in data and "longt" in data:
            latitude = float(data["latt"])
            longitude = float(data["longt"])
            return longitude, latitude
        else:
            print("No results found for the given address.")
    else:
        print(f"Error: {response.status_code}")

