from flask import Flask, jsonify

# Initialize the Flask app
app = Flask(__name__)

# Basic route to test if the server is running
@app.route('/')
def home():
    return jsonify({"message": "Welcome to the AI Expense Tracker API!"})

# Run the app
if __name__ == '__main__':
    app.run(debug=True)
