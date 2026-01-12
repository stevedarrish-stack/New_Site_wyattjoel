from flask import Flask, request


from flask import Flask, request
from flask_cors import CORS

app = Flask(__name__)
# Allow only your GitHub Pages site to access the backend
CORS(app, origins=["https://stevedarrish-stack.github.io"])


@app.route('/inquiry', methods=['POST'])
def inquiry():
    name = request.form.get('name')
    email = request.form.get('email')
    topic = request.form.get('topic')
    message = request.form.get('message')
    print(f"Received inquiry: {name}, {email}, {topic}, {message}")
    return "Thank you for your inquiry!", 200

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=10000)

  