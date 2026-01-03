from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

@app.route('/api/contact', methods=['POST'])
def submit_inquiry():
    data = request.get_json()
    # Here you would process/store the inquiry
    return jsonify({'status': 'success', 'message': 'Inquiry received!', 'data': data}), 200

def main():
    print("Hello, world! This is the app entry point.")

if __name__ == "__main__":
    app.run(debug=True)
