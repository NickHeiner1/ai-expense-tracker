import os
import uuid
import json
from flask import Flask, request, jsonify
from flask_cors import CORS
from dotenv import load_dotenv
from openai import OpenAI
from supabase import create_client, Client
from datetime import datetime

# Load environment variables
load_dotenv()
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
SUPABASE_DB_URL = os.getenv("SUPABASE_DB_URL")
SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")  # Now using correct key

# Validate environment variables
if not OPENAI_API_KEY or not SUPABASE_DB_URL:
    raise ValueError("Missing API keys. Check your .env file.")

# Initialize OpenAI client
client = OpenAI(api_key=OPENAI_API_KEY)

# Initialize Supabase client
supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)


# Flask app setup
app = Flask(__name__)
CORS(app)

# Function to categorize expenses using OpenAI
def categorize_expense(description):
    """Uses AI to predict an expense category based on description."""
    prompt = f"Categorize this expense: '{description}'. Possible categories: Food, Travel, Entertainment, Utilities, Shopping, Health, Other."
    
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "You are an AI that classifies expenses into categories."},
            {"role": "user", "content": prompt}
        ]
    )
    
    return response.choices[0].message.content.strip()

# Function to store expense in Supabase
def store_expense_in_db(expense):
    """Stores an expense in the Supabase database."""
    data, count = supabase.table("expenses").insert(expense).execute()
    return data

# Route to add an expense
@app.route('/add-expense', methods=['POST'])
def add_expense():
    """Adds a new expense to the database."""
    data = request.json
    description = data.get('description', '')

    # Use AI to predict category if not provided
    category = data.get('category') or categorize_expense(description)

    expense = {
        "id": str(uuid.uuid4()),
        "amount": data.get('amount'),
        "category": category,
        "description": description,
        "date": datetime.now().isoformat(),
    }

    store_expense_in_db(expense)  # Store in Supabase
    return jsonify(expense)

# Route to get all expenses
@app.route('/expenses', methods=['GET'])
def get_expenses():
    """Fetches all expenses from the database."""
    response = supabase.table("expenses").select("*").execute()

    if response.data:
        return jsonify(response.data), 200
    else:
        return jsonify([]), 200

# Run Flask app
if __name__ == '__main__':
    app.run(debug=True)
