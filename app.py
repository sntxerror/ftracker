from flask import Flask, request, jsonify, make_response, render_template, session
import os
from plaid.api import plaid_api
from plaid.models import (
    ItemPublicTokenExchangeRequest, 
    LinkTokenCreateRequest, 
    TransactionsGetRequest, 
    CountryCode,
    Products  # We import Products directly from plaid.models
)
from plaid.configuration import Configuration
from plaid.api_client import ApiClient
from dotenv import load_dotenv
from datetime import datetime, timedelta 

# Load environment variables
load_dotenv()

PLAID_CLIENT_ID = os.getenv('PLAID_CLIENT_ID')
PLAID_SECRET = os.getenv('PLAID_SECRET')
PLAID_ENV = os.getenv('PLAID_ENV', 'sandbox')
SECRET_KEY = os.getenv('SECRET_KEY', 'default_secret')

# Initialize Flask app
app = Flask(__name__)
app.secret_key = SECRET_KEY

# Configure Plaid API
configuration = Configuration(
    host=f"https://{PLAID_ENV}.plaid.com",
    api_key={
        "clientId": PLAID_CLIENT_ID,
        "secret": PLAID_SECRET,
    }
)
api_client = ApiClient(configuration)
plaid_client = plaid_api.PlaidApi(api_client)

# Centralized error handler
@app.errorhandler(Exception)
def handle_exception(e):
    # Add detailed error information
    error_details = {
        "error": str(e),
        "type": str(type(e)),
        "module": getattr(e, "__module__", "unknown")
    }
    
    # Log the error for server-side debugging
    print("Error details:", error_details)
    
    return make_response(jsonify(error_details), 500)


# Render HTML page
@app.route('/')
def index():
    return render_template('index.html')

# Login route
@app.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')

    if username == 'user_good' and password == 'pass_good':
        session['user'] = username
        response = {
            "message": "Login successful"
        }
        return jsonify(response)
    return make_response(jsonify({"error": "Invalid credentials"}), 401)

# Logout route
@app.route('/logout', methods=['POST'])
def logout():
    session.pop('user', None)
    return jsonify({"message": "Logout successful"})

# Create Link Token
@app.route('/create_link_token', methods=['POST'])
def create_link_token():
    try:
        # Create a Products instance for transactions
        # This properly instantiates the enum the way Plaid expects
        transactions_product = Products('transactions')
        
        request = LinkTokenCreateRequest(
            user={"client_user_id": session.get('user', 'guest_user')},
            client_name="Plaid Web App",
            products=[transactions_product],  # Use the instantiated Products enum
            country_codes=[CountryCode("US")],
            language="en",
        )
        
        # Add debug logging to see the request structure
        print("Creating link token with request:", request)
        
        response = plaid_client.link_token_create(request)
        return jsonify(response.to_dict())
    except Exception as e:
        print(f"Error creating link token: {str(e)}")
        return handle_exception(e)

# Exchange Public Token
@app.route('/exchange_public_token', methods=['POST'])
def exchange_public_token():
    try:
        # Get the public token from the request body
        data = request.get_json()
        public_token = data.get('publicToken')
        
        # Create the exchange request using the correct Plaid model
        exchange_request = ItemPublicTokenExchangeRequest(
            public_token=public_token
        )
        
        # Make the exchange request to Plaid
        exchange_response = plaid_client.item_public_token_exchange(exchange_request)
        
        # Store the access token in the session
        session['access_token'] = exchange_response.access_token
        
        # Return the response to the client
        return jsonify(exchange_response.to_dict())
        
    except Exception as e:
        print(f"Error exchanging public token: {str(e)}")
        return handle_exception(e)

# Fetch Transactions

@app.route('/transactions', methods=['GET'])
def fetch_transactions():
    try:
        access_token = session.get('access_token')
        if not access_token:
            return make_response(jsonify({"error": "Access token not found"}), 401)
        
        # Use more recent dates for sandbox testing
        # Plaid sandbox typically has transactions in the last 2 years
        end_date = datetime.now().date()
        start_date = end_date - timedelta(days=365)  # Get last year's worth of transactions
        
        transactions_request = TransactionsGetRequest(
            access_token=access_token,
            start_date=start_date,
            end_date=end_date,
            options={
                "include_personal_finance_category": True  # Get enhanced categorization
            }
        )
        
        print(f"Fetching transactions with date range: {start_date} to {end_date}")
        response = plaid_client.transactions_get(transactions_request)
        
        # Extract transactions and add debug info
        transactions = response.to_dict()["transactions"]
        print(f"Total transactions found: {len(transactions)}")
        if transactions:
            print("Sample transaction:", transactions[0])
        
        return jsonify(transactions)
        
    except Exception as e:
        print(f"Detailed error in transactions: {str(e)}")
        import traceback
        print(f"Traceback: {traceback.format_exc()}")
        return handle_exception(e)
    
@app.route('/favicon.ico')
def favicon():
    return '', 204


if __name__ == '__main__':
    app.run(debug=True)
