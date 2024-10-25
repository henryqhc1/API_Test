from flask import Flask, jsonify, request
import requests
import json
import os

app = Flask(__name__)

EQUATION_URL = 'https://raw.githubusercontent.com/henryqhc1/API_Test/main/linear_equation.json'

def load_equation():
    try:
        response = requests.get(EQUATION_URL)
        response.raise_for_status()
        equation_data = response.json()
        return equation_data
    except Exception as e:
        print(f"Error loading equation: {e}")
        return None

def calculate_y(x1, x2, equation):
    intercept = equation["intercept"]
    coefficients = equation["coefficients"]
    return intercept + coefficients["x1"] * x1 + coefficients["x2"] * x2

def save_result(x1, x2, y):
    result = {"x1": x1, "x2": x2, "y": y}
    output_file = os.path.abspath('results.json')

    if os.path.exists(output_file):
        with open(output_file, 'r') as f:
            data = json.load(f)
    else:
        data = []

    data.append(result)
    with open(output_file, 'w') as f:
        json.dump(data, f, indent=4)
    print(f"Result saved to {output_file}")

@app.route('/api/calculate_y', methods=['GET'])
def get_y():
    equation = load_equation()
    if not equation:
        return jsonify({"error": "Could not load equation data."}), 500

    try:
        x1 = float(request.args.get('x1', 0))
        x2 = float(request.args.get('x2', 0))
    except ValueError:
        return jsonify({"error": "Invalid input. x1 and x2 must be numbers."}), 400

    y = calculate_y(x1, x2, equation)

    save_result(x1, x2, y)

    return jsonify({"x1": x1, "x2": x2, "y": y})

if __name__ == '__main__':
    app.run(debug=True)
