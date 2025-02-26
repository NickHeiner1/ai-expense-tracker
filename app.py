from flask import Flask, request, jsonify
import uuid
from datetime import datetime

# Initialize Flask app
app = Flask(__name__)

# In-memory storage for expenses
expenses = []

# Basic route to check if the server is running
@app.route('/')
def home():
    return jsonify({"message": "Welcome to the AI Expense Tracker API!"})

# Route to add a new expense
@app.route('/add-expense', methods=['POST'])
def add_expense():
    data = request.json
    expense = {
        "id": str(uuid.uuid4()),  # Generates a unique ID for each expense
        "amount": data.get('amount'),
        "category": data.get('category', 'Uncategorized'),
        "description": data.get('description', ''),
        "date": data.get('date', datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
    }
    expenses.append(expense)
    return jsonify({"message": "Expense added successfully!", "expense": expense}), 201

# Route to get all expenses
@app.route('/expenses', methods=['GET'])
def get_expenses():
    return jsonify(expenses), 200

# Run the app
if __name__ == '__main__':
    app.run(debug=True)
