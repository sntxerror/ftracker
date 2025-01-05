# Plaid Web Application - Python Version

## Overview
This is the Python version of the Plaid Web App. It integrates with Plaid to securely link financial accounts and retrieve transaction data. The project includes a web-based front-end and a Python-based back-end.

## Features
- **User Authentication:** Users can log in and out.
- **Plaid Integration:** Allows users to securely link their financial accounts using Plaid.
- **Transaction Retrieval:** Fetches and displays user transactions.

## Project Structure
```
.
├── app.py             		# Python server handling API endpoints
├── templates/index.html  # Frontend HTML file
├── static/client.js      # Folder for static files like CSS and JS
└── requirements.txt     	# Python dependencies
```

## Installation

### Prerequisites
- Python 3.8+
- Pip (Python package manager)

### Steps
1. Clone this repository:
   ```bash
   git clone <repository-url>
   cd <repository-folder>
   ```
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Start the server:
   ```bash
   python app.py
   ```
4. Open the `index.html` file in a web browser or host it using a web server.

## Usage

### Frontend
1. Open the `index.html` file in your browser.
2. Log in using the authentication form.
3. Click "Create Link Token" to link your financial account.
4. View transaction data under the Transactions section.

### Backend
The Python server provides the following endpoints:
- **`/login`**: Handles user login.
- **`/logout`**: Logs out the user.
- **`/create_link_token`**: Creates a Plaid link token.
- **`/exchange_public_token`**: Exchanges a public token for access tokens.
- **`/transactions`**: Fetches transaction data.

### Key Files
- `index.html`: Contains the structure and layout of the web app.
- `client.js`: Implements the JavaScript logic for user interaction and API calls.
- `app.py`: Python server responsible for handling API requests and interacting with Plaid.

## Dependencies
Install the Python dependencies listed in `requirements.txt`.

## Environment Variables
Create a `.env` file to store sensitive information such as:
```
PLAID_CLIENT_ID=your_client_id
PLAID_SECRET=your_secret
PLAID_ENV=sandbox
```

## Plaid Setup
1. Sign up for a Plaid account.
2. Retrieve your API keys from the Plaid dashboard.
3. Set the keys in your `.env` file.

## Running the Project
1. Start the backend server:
   ```bash
   python app.py
   ```
2. Open the `index.html` in your browser or deploy it to a web server.

## Contributing
Contributions are welcome! Please follow these steps:
1. Fork the repository.
2. Create a new branch for your feature or bugfix.
3. Submit a pull request with a detailed description of your changes.

## License
This project is licensed under the MIT License.
