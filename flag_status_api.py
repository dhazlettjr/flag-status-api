from flask import Flask, jsonify
import requests
from bs4 import BeautifulSoup

app = Flask(__name__)

@app.route("/flag-status", methods=["GET"])
def flag_status():
    url = "https://www.orangebeachal.gov/170/Beach-Safety-Mollys-Patrol"

    try:
        response = requests.get(url, timeout=10)
    except requests.exceptions.RequestException as e:
        return jsonify({"error": f"Request failed: {str(e)}"}), 500

    if response.status_code != 200:
        return jsonify({"error": f"Failed to fetch page, status: {response.status_code}"}), 500

    soup = BeautifulSoup(response.text, "html.parser")
    page_text = soup.get_text(separator=' ', strip=True).lower()

    # Debug: log the first 500 chars to Render logs
    print("🔍 PAGE TEXT (trimmed):", page_text[:500])

    if "yellow flag" in page_text:
        color = "Yellow"
        hazard = "Medium"
        description = "Moderate surf and/or currents"
    elif "red flag" in page_text:
        color = "Red"
        hazard = "High"
        description = "High surf and/or strong currents"
    elif "green flag" in page_text:
        color = "Green"
        hazard = "Low"
        description = "Calm conditions, exercise caution"
    elif "purple flag" in page_text:
        color = "Purple"
        hazard = "Marine Pests"
        description = "Dangerous marine life"
    else:
        return jsonify({"error": "Flag not found in page text"}), 404

    return jsonify({
        "color": color,
        "hazard": hazard,
        "description": description
    })

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
