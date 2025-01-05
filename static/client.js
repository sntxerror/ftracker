const baseUrl = window.location.origin;

async function apiRequest(endpoint, method = "GET", body = null) {
    try {
        const headers = { "Content-Type": "application/json" };
        const response = await fetch(`${baseUrl}${endpoint}`, {
            method,
            headers,
            body: body ? JSON.stringify(body) : null,
        });

        if (!response.ok) throw new Error(`Error: ${response.statusText}`);
        return await response.json();
    } catch (error) {
        console.error(`API Request failed: ${error}`);
        alert("An error occurred. Check the console for details.");
    }
}

async function login(event) {
    event.preventDefault();
    const username = document.getElementById("username").value;
    const password = document.getElementById("password").value;

    const response = await apiRequest("/login", "POST", { username, password });
    if (response && response.message) {
        alert(response.message);
        document.getElementById("login-form").style.display = "none";
        document.getElementById("logout-btn").style.display = "inline-block";
        document.getElementById("link-btn").style.display = "inline-block";
    }
}

async function logout() {
    const response = await apiRequest("/logout", "POST");
    if (response && response.message) {
        alert(response.message);
        document.getElementById("login-form").style.display = "block";
        document.getElementById("logout-btn").style.display = "none";
        document.getElementById("link-btn").style.display = "none";
        document.getElementById("transactions-list").innerHTML = "";
    }
}

async function createLinkToken() {
    const response = await apiRequest("/create_link_token", "POST");
    if (response && response.link_token) {
        initializePlaidLink(response.link_token);
    }
}

function initializePlaidLink(linkToken) {
    const handler = Plaid.create({
        token: linkToken,
        onSuccess: async (publicToken) => {
            await exchangePublicToken(publicToken);
        },
        onExit: (err) => {
            if (err) console.error("Plaid Link Error:", err);
        },
    });
    handler.open();
}

async function exchangePublicToken(publicToken) {
    const response = await apiRequest("/exchange_public_token", "POST", { publicToken });
    if (response && response.access_token) {
        alert("Public token exchanged successfully.");
        fetchTransactions();
    }
}

async function fetchTransactions() {
    console.log("Fetching transactions...");
    const transactions = await apiRequest("/transactions");
    console.log("Received transactions:", transactions);
    if (transactions) {
        displayTransactions(transactions);
    }
}

function displayTransactions(transactions) {
    const container = document.getElementById("transactions-list");
    if (!transactions || transactions.length === 0) {
        container.innerHTML = '<div class="alert alert-info">No transactions found. Please ensure you connected a sandbox bank account with test data.</div>';
        return;
    }
    
    container.innerHTML = transactions
        .map(tx => `
            <div class="card mb-2">
                <div class="card-body">
                    <h5 class="card-title">${tx.merchant_name || tx.name}</h5>
                    <p class="card-text">
                        Amount: $${Math.abs(tx.amount).toFixed(2)}<br>
                        Date: ${tx.date}<br>
                        ${tx.category ? `Category: ${tx.category.join(', ')}` : ''}
                    </p>
                </div>
            </div>
        `)
        .join("");
}

// Attach event listeners
document.getElementById("login-form").addEventListener("submit", login);
document.getElementById("logout-btn").addEventListener("click", logout);
document.getElementById("link-btn").addEventListener("click", createLinkToken);
