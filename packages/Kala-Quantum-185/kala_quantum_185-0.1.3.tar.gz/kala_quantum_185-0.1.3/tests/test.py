from Kala_Quantum.quantum_core import QuantumState, hadamard  # Assuming Kala-Quantum-185 is installed
import json
from math import atan2, degrees, sqrt, pi, sin, cos
from datetime import datetime, timedelta

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
    tithi_names = {
        1: "Pratipada",
        2: "Dwitiya",
        3: "Tritiya",
        4: "Chaturthi",
        5: "Panchami",
        6: "Shashti",
        7: "Saptami",
        8: "Ashtami",
        9: "Navami",
        10: "Dashami",
        11: "Ekadashi",
        12: "Dwadashi",
        13: "Trayodashi",
        14: "Chaturdashi",
        15: "Purnima (Full Moon)",
        16: "Pratipada (Krishna Paksha)",
        17: "Dwitiya (Krishna Paksha)",
        18: "Tritiya (Krishna Paksha)",
        19: "Chaturthi (Krishna Paksha)",
        20: "Panchami (Krishna Paksha)",
        21: "Shashti (Krishna Paksha)",
        22: "Saptami (Krishna Paksha)",
        23: "Ashtami (Krishna Paksha)",
        24: "Navami (Krishna Paksha)",
        25: "Dashami (Krishna Paksha)",
        26: "Ekadashi (Krishna Paksha)",
        27: "Dwadashi (Krishna Paksha)",
        28: "Trayodashi (Krishna Paksha)",
        29: "Chaturdashi (Krishna Paksha)",
        30: "Amavasya (New Moon)"
    }

    return tithi_names[tithi]

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
    yogas = [
        "Vishkumbha", "Priti", "Ayushman", "Saubhagya", "Shobhana", "Atiganda", "Sukarman",
        "Dhriti", "Shoola", "Ganda", "Vriddhi", "Dhruva", "Vyaghata", "Harshana", "Vajra",
        "Siddhi", "Vyatipata", "Variyana", "Parigha", "Shiva", "Siddha", "Sadhya",
        "Shubha", "Shukla", "Brahma", "Indra", "Vaidhriti"
    ]
    return yogas[yoga_number]

def calculate_planetary_positions_and_attributes(data):
    """Add Tithi, Nakshatra, and Yoga to planetary positions."""
    for item in data:
        sun_long = item["sun"]["longitude"]
        moon_long = item["moon"]["longitude"]
        item["tithi"] = calculate_tithi(sun_long, moon_long)
        item["nakshatra"] = calculate_nakshatra(moon_long)
        item["yoga"] = calculate_yoga(sun_long, moon_long)
    return data

def json_to_html(data, output_file):
    """Convert JSON data to an HTML file with basic CSS styling."""
    with open(output_file, "w") as html_file:
        html_file.write("""
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Report</title>
    <style>
        body {
            font-family: Arial, sans-serif;
            margin: 20px;
            line-height: 1.6;
        }
        .key {
            font-weight: bold;
            color: #333;
        }
        .value {
            margin-left: 20px;
            color: #555;
        }
        .item {
            margin-top: 20px;
        }
    </style>
</head>
<body>
    <h1>Report</h1>
""")

        def write_content(data, indent=0):
            """Recursive function to write content to HTML file."""
            if isinstance(data, list):
                for idx, item in enumerate(data):
                    html_file.write(f'<div class="item" style="margin-left: {indent}px;"><span class="key">Item {idx + 1}:</span></div>\n')
                    write_content(item, indent + 20)
            elif isinstance(data, dict):
                for key, value in data.items():
                    if isinstance(value, (dict, list)):
                        html_file.write(f'<div class="item" style="margin-left: {indent}px;"><span class="key">{key}:</span></div>\n')
                        write_content(value, indent + 20)
                    else:
                        html_file.write(f'<div class="item" style="margin-left: {indent}px;"><span class="key">{key}:</span> <span class="value">{value}</span></div>\n')
            else:
                html_file.write(f'<div class="item" style="margin-left: {indent}px;">{data}</div>\n')

        write_content(data)
        html_file.write("""
</body>
</html>
""")
    print(f"HTML file saved as {output_file}")

def main():
    """Main function to process JSON and generate HTML report."""
    # Example JSON input
    with open("sun_moon_positions.json", "r") as file:
        data = json.load(file)

    enriched_data = calculate_planetary_positions_and_attributes(data)

    # Save enriched data
    with open("sun_moon_positions_enriched.json", "w") as file:
        json.dump(enriched_data, file, indent=4)

    # Generate HTML Report
    json_to_html(enriched_data, "Report.html")

    print("Tithi, Nakshatra, and Yoga added and saved to 'sun_moon_positions_enriched.json'.")
    print("HTML Report saved as 'Report.html'.")

if __name__ == "__main__":
    main()
