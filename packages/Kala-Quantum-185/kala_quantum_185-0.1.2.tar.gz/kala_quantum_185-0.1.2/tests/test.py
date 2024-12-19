import json
import math

# Lahiri Ayanamsa value in degrees, minutes, and seconds
LAHIRI_AYANAMSA = 24 + (12 / 60) + (21 / 3600)  # Convert to decimal degrees

def convert_to_sidereal(tropical_longitude):
    """
    Convert tropical longitude to sidereal longitude using Lahiri Ayanamsa.
    """
    sidereal_longitude = tropical_longitude - LAHIRI_AYANAMSA
    if sidereal_longitude < 0:
        sidereal_longitude += 360
    return sidereal_longitude

def calculate_tithi(sun_long, moon_long):
    """
    Calculate Tithi based on the angular distance between the Sun and Moon.
    """
    # Convert both Sun and Moon longitudes to sidereal
    sidereal_sun = convert_to_sidereal(sun_long)
    sidereal_moon = convert_to_sidereal(moon_long)
    
    # Calculate angular distance
    angular_distance = (sidereal_moon - sidereal_sun) % 360
    tithi = int(angular_distance / 12) + 1
    return tithi


def calculate_nakshatra(moon_long):
    nakshatra_number = int(moon_long / 13.3333) % 27
    nakshatras = [
        "Ashwini", "Bharani", "Krittika", "Rohini", "Mrigashirsha", "Ardra", "Punarvasu",
        "Pushya", "Ashlesha", "Magha", "Purva Phalguni", "Uttara Phalguni", "Hasta", "Chitra",
        "Swati", "Vishakha", "Anuradha", "Jyeshtha", "Mula", "Purva Ashadha", "Uttara Ashadha",
        "Shravana", "Dhanishta", "Shatabhisha", "Purva Bhadrapada", "Uttara Bhadrapada", "Revati"
    ]
    return nakshatras[nakshatra_number]

def calculate_yoga(sun_long, moon_long):
    total_longitude = (sun_long + moon_long) % 360
    yoga_number = int(total_longitude / 13.3333) % 27
    return yoga_number

# Load the trained dataset
with open("sun_moon_positions.json", "r") as file:
    data = json.load(file)

# Calculate and save enriched dataset
for item in data:
    sun_long = item["sun"]["longitude"]
    moon_long = item["moon"]["longitude"]
    item["tithi"] = calculate_tithi(sun_long, moon_long)
    item["nakshatra"] = calculate_nakshatra(moon_long)
    item["yoga"] = calculate_yoga(sun_long, moon_long)

# Save enriched data
with open("sun_moon_positions_enriched.json", "w") as file:
    json.dump(data, file, indent=4)
print("Tithi, Nakshatra, and Yoga added and saved to 'sun_moon_positions_enriched.json'.")
