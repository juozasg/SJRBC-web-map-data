import requests

# Region ID for sensors
regionId = 49

def read_token():
    with open('tolthawk-token', 'r') as f:
        token = f.read().strip()
        return token

def get_sensor_status(token, region_id):
    url = f"https://sensors.tolthawk.com/api/mobile/LocationsStatus/{region_id}"

    headers = {
        "Content-Type": "application/json",
        "Token": token
    }

    response = requests.get(url, headers=headers)
    response.raise_for_status()

    # Parse response JSON
    data = response.json()
    print(f"Successfully fetched data for {len(data)} sensors")
    return data



# Main execution
if __name__ == "__main__":
    api_token = read_token()

    sensor_status = get_sensor_status(api_token, regionId)

    print(sensor_status)

