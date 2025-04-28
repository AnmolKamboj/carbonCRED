import requests

def calculate_home_work_distance(home_address, work_address):
    print(f"Home Address: {home_address}, Work Address: {work_address}")

    api_key = "AIzaSyActKYFWpV-gIVSbeMGzo6IaS6jgP_F_Yw" 

    endpoint = "https://maps.googleapis.com/maps/api/distancematrix/json"
    params = {
        "origins": home_address,
        "destinations": work_address,
        "key": api_key,
        "units": "imperial"
    }

    try:
        response = requests.get(endpoint, params=params)
        data = response.json()

        print(f"✅ Raw Distance API Response: {data}")
        if data['status'] != 'OK':
            raise Exception('Error fetching distance from Google API')

        element = data['rows'][0]['elements'][0]

        if element['status'] != 'OK':
            raise Exception('No valid route found between Home and Work addresses')

        distance_text = element['distance']['text']  # e.g., "5.6 mi"
        miles = float(distance_text.split()[0])

        return miles

    except Exception as e:
        print(f"❌ Distance API Error: {e}")
        return None

def gemini_predict_travel_mode(image_file):
    # This is a placeholder
    # Later we will integrate actual Gemini API here
    # For now, fake mode for testing
    return 'carpool'  # Just always returns 'carpool' for now