from flask import Flask, jsonify, request
import requests
import json
import os

app = Flask(__name__)

DATA_URL = 'https://raw.githubusercontent.com/henryqhc1/API_Test/main/data.json'

def load_data():
    try:
        response = requests.get(DATA_URL)
        response.raise_for_status()  
        return response.json()
    except Exception as e:
        print(f"Error fetching data: {e}")
        return []

@app.route('/api/data', methods=['GET'])
def get_data():
    data = load_data()

    ID = request.args.get('ID')
    Name = request.args.get('Name')
    Age = request.args.get('Age')
    Zipcode = request.args.get('Zipcode')

    filtered_data = [
        item for item in data
        if (ID is None or item['ID'] == int(ID)) and
           (Name is None or item['Name'].lower() == Name.lower()) and
           (Age is None or item['Age'] == int(Age)) and
           (Zipcode is None or item['Zipcode'] == Zipcode)
    ]

    output_file = 'filtered_data.json'
    with open(output_file, 'w') as f:
        json.dump(filtered_data, f, indent=4)

    return jsonify(filtered_data)

if __name__ == '__main__':
    app.run(debug=True)