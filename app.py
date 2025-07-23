from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
from pymongo import MongoClient
from dotenv import load_dotenv
import os
import datetime

# Load environment variables from .env
load_dotenv()

app = Flask(__name__)
CORS(app)

# Get the Mongo URI from environment variable
MONGO_URI = os.getenv("MONGO_URI", "mongodb://localhost:27017/")
client = MongoClient(MONGO_URI)

# Connect to database and collection
db = client['portfolio_db']
contacts_collection = db['contacts']

# Home route to serve the HTML
@app.route('/')
def index():
    return render_template('index.html')

# POST route for contact form
@app.route('/submit-form', methods=['POST'])
def submit_form():
    try:
        data = request.get_json()
        name = data.get('name')
        email = data.get('email')
        subject = data.get('subject')
        message = data.get('message')

        if not all([name, email, subject, message]):
            return jsonify({'success': False, 'message': 'Please fill in all fields'}), 400

        contact_data = {
            'name': name,
            'email': email,
            'subject': subject,
            'message': message,
            'timestamp': datetime.datetime.utcnow()
        }

        contacts_collection.insert_one(contact_data)
        return jsonify({'success': True, 'message': 'Message received successfully'})
    except Exception as e:
        print("Error submitting form:", e)
        return jsonify({'success': False, 'message': 'Something went wrong'}), 500

# Start Flask app
if __name__ == '__main__':
    app.run(debug=True)
