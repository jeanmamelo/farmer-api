from flask import Flask, jsonify, send_from_directory
from flask_swagger_ui import get_swaggerui_blueprint
import json

app = Flask(__name__)

# Load farmer data from JSON file
with open('datasource/farmer.json', 'r') as f:
    farmer_data = json.load(f)

@app.route('/')
def home():
    return "Farmer API is running."

@app.route('/farmers', methods=['GET'])
def get_farmers():
    return jsonify(farmer_data)

@app.route('/farmer/<farm_name>', methods=['GET'])
def get_farmer_by_name(farm_name):
    farmer = next((f for f in farmer_data['farmer'] if f['farm_name'] == farm_name), None)
    if farmer:
        return jsonify(farmer)
    return jsonify({"error": "Farmer not found"}), 404

@app.route('/farmer/<farm_name>/production', methods=['GET'])
def get_farm_production(farm_name):
    farmer = next((f for f in farmer_data['farmer'] if f['farm_name'] == farm_name), None)
    if farmer:
        return jsonify(farmer.get('production', {}))
    return jsonify({"error": "Production data not found"}), 404

@app.route('/farmer/<farm_name>/sensor/<sensor_id>', methods=['GET'])
def get_sensor_data(farm_name, sensor_id):
    farmer = next((f for f in farmer_data['farmer'] if f['farm_name'] == farm_name), None)
    if farmer:
        sensor = next((s for s in farmer['production']['sensor'] if s['sensor_id'] == sensor_id), None)
        if sensor:
            return jsonify(sensor)
    return jsonify({"error": "Sensor data not found"}), 404

# Swagger configuration
SWAGGER_URL = '/swagger'
API_URL = '/static/swagger.json'
swaggerui_blueprint = get_swaggerui_blueprint(
    SWAGGER_URL,
    API_URL,
    config={
        'app_name': "Farmer API"
    }
)
app.register_blueprint(swaggerui_blueprint, url_prefix=SWAGGER_URL)

@app.route('/static/<path:path>')
def send_static(path):
    return send_from_directory('static', path)

if __name__ == '__main__':
    app.run(debug=True)
