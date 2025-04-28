import requests
import google.generativeai as genai
from PIL import Image
import io
import base64

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
    try:
        # Load image binary
        image_bytes = image_file.read()
        genai.configure(api_key="AIzaSyBi4YmvKw3SIhEOu_CfsnZhp9v6tMDFvSc")

        model = genai.GenerativeModel(model_name="gemini-2.0-flash")

        response = model.generate_content(
            [ 
              {"mime_type": image_file.mimetype, "data": image_bytes},
              "Identify the transport mode in this proof image. give me only one word response. choose one from the following: carpool, public transport, bicycle, work from home."
            ]
        )

        print("✅ Gemini Raw Response:", response.text)

        # Simple keyword search
        text = response.text.lower()

        if "carpool" in text or "Carpool" in text:
            return "carpool"
        elif "public transport" in text or "Public transport" in text:
            return "public_transport"
        elif "bicycle" in text or "Bicycle" in text:
            return "bicycle"
        elif "work from home" in text or "wfh" in text:
            return "wfh"
        else:
            return None

    except Exception as e:
        print(f"❌ Error during Gemini prediction: {e}")
        return None