from flask import Flask, jsonify
import requests
from bs4 import BeautifulSoup

app = Flask(__name__)

@app.route("/flag-status", methods=["GET"])
def flag_status():
    url = "https://www.orangebeachal.gov/170/Beach-Safety-Mollys-Patrol"
    response = requests.get(url)

    if response.status_code != 200:
        return jsonify({"error": "Failed to fetch page"}), 500

    soup = BeautifulSoup(response.text, "html.parser")
    content = soup.find("div", class_="ModuleContent")

    if not content:
        return jsonify({"error": "Could not find flag info"}), 404

    text = content.get_text(strip=True)

    if "Yellow Flag" in text:
        color = "Yellow"
        hazard = "Medium"
        description = "Moderate surf and/or currents"
    elif "Red Flag" in text:
        color = "Red"
        hazard = "High"
        description = "High surf and/or strong currents"
    elif "Green Flag" in text:
        color = "Green"
        hazard = "Low"
        description = "Calm conditions, exercise caution"
    elif "Purple Flag" in text:
        color = "Purple"
        hazard = "Marine Pests"
        description = "Dangerous marine life"
    else:
        color = "Unknown"
        hazard = "Unknown"
        description = "Unable to determine flag status"

    return jsonify({
        "color": color,
        "hazard": hazard,
        "description": description
    })

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
