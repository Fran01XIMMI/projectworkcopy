import matplotlib
from flask import Flask, render_template_string, request, redirect, url_for, flash, session, get_flashed_messages, \
    send_file, render_template
import os
import matplotlib.pyplot as plt
import seaborn as sns
import io
from functools import wraps
import pandas as pd
import joblib
import mysql.connector
from mysql.connector import Error
import base64

# the decorative website
app = Flask(__name__)
app.secret_key = os.urandom(24)

#dataframe pandas
df = pd.DataFrame

filtered_data = pd.DataFrame()

df = pd.read_csv('Bank_Marketing.csv', delimiter=';')

# Carichiamo il modello, lo scaler e le colonne
model = joblib.load('random_forest_model.pkl')
scaler = joblib.load('scaler.pkl')
columns = joblib.load('columns.pkl')

# CSS styles as a string variable
css = """
/* Global Styles */
:root {
    --primary-color: #1a3b5d;
    --secondary-color: #2d6187;
    --accent-color: #e4a013;
    --text-color: #333;
    --light-text: #f8f9fa;
    --border-color: #dee2e6;
    --success-color: #28a745;
    --danger-color: #dc3545;
    --warning-color: #ffc107;
    --info-color: #17a2b8;
}

* {
    margin: 0;
    padding: 0;
    box-sizing: border-box;
}

body {
    font-family: Helvetica, sans-serif;
    line-height: 1.6;
    color: var(--text-color);
    background-color: #f5f7fa;
    min-height: 100vh;
    display: flex;
    flex-direction: column;
}

a {
    text-decoration: none;
    color: var(--secondary-color);
}

a:hover {
    color: var(--primary-color);
}

/* Header Styles */
.header {
    background-color: var(--primary-color);
    color: white;
    padding: 1rem 2rem;
    display: flex;
    justify-content: space-between;
    align-items: center;
    box-shadow: 0 2px 5px rgba(0, 0, 0, 0.1);
}

.logo-container {
    display: flex;
    align-items: center;
}

.logo-icon {
    font-size: 2rem;
    margin-right: 10px;
    color: var(--accent-color);
}

.header h1 {
    font-size: 1.5rem;
    font-weight: 600;
}

.header-right {
    display: flex;
    align-items: center;
    gap: 1.5rem;
}

.system-time {
    font-size: 0.9rem;
    color: #ddd;
}

.user-info {
    display: flex;
    align-items: center;
    gap: 0.5rem;
    font-size: 0.9rem;
}

.logout-btn {
    background-color: rgba(255, 255, 255, 0.1);
    color: white;
    padding: 0.5rem 1rem;
    border-radius: 4px;
    font-size: 0.9rem;
    transition: background-color 0.3s;
}

.logout-btn:hover {
    background-color: rgba(255, 255, 255, 0.2);
    color: white;
}

/* Main Content */
.main-content {
    flex: 1;
    padding: 2rem;
    max-width: 1200px;
    margin: 0 auto;
    width: 100%;
}

.login-container {
    display: flex;
    justify-content: center;
    align-items: center;
    min-height: calc(100vh - 140px);
}

.login-card {
    background-color: white;
    border-radius: 8px;
    box-shadow: 0 4px 15px rgba(0, 0, 0, 0.1);
    width: 100%;
    max-width: 450px;
    padding: 2rem;
}

.login-header {
    text-align: center;
    margin-bottom: 2rem;
}

.login-header h2 {
    color: var(--primary-color);
    margin-bottom: 0.5rem;
}

.login-header p {
    color: #6c757d;
    font-size: 0.9rem;
}

.login-form .form-group {
    margin-bottom: 1.5rem;
}

.login-form label {
    display: block;
    margin-bottom: 0.5rem;
    font-weight: 500;
    color: var(--primary-color);
}

.login-form input {
    width: 100%;
    padding: 0.75rem;
    border: 1px solid var(--border-color);
    border-radius: 4px;
    font-size: 1rem;
    transition: border-color 0.3s;
}

.login-form input:focus {
    border-color: var(--secondary-color);
    outline: none;
}

.form-actions {
    margin-top: 2rem;
}

.btn {
    display: inline-block;
    padding: 0.75rem 1.5rem;
    border-radius: 4px;
    font-weight: 500;
    cursor: pointer;
    border: none;
    transition: all 0.3s;
}

.btn-primary {
    background-color: var(--primary-color);
    color: white;
    width: 100%;
    font-size: 1rem;
}

.btn-primary:hover {
    background-color: var(--secondary-color);
}

.btn-danger {
    background-color: var(--danger-color);
    color: white;
    width: 100%;
    font-size: 1rem;
    border-radius: 4px;
    display: inline-block;
}

.btn-danger:hover {
    background-color: #c82333;
}

.form-footer {
    text-align: center;
    margin-top: 1.5rem;
    font-size: 0.9rem;
}

.forgot-password {
    color: var(--secondary-color);
}

/* Alerts */
.alert {
    padding: 1rem;
    border-radius: 4px;
    margin-bottom: 1.5rem;
    font-size: 0.9rem;
}

.alert-danger {
    background-color: #f8d7da;
    color: #721c24;
    border: 1px solid #f5c6cb;
}

.alert-success {
    background-color: #d4edda;
    color: #155724;
    border: 1px solid #c3e6cb;
}

.alert-info {
    background-color: #d1ecf1;
    color: #0c5460;
    border: 1px solid #bee5eb;
}

/* Navigation */
.main-nav {
    background-color: white;
    box-shadow: 0 2px 5px rgba(0, 0, 0, 0.05);
}

.main-nav ul {
    list-style: none;
    display: flex;
    max-width: 1200px;
    margin: 0 auto;
    padding: 0 2rem;
}

.main-nav li {
    position: relative;
}

.main-nav a {
    display: block;
    padding: 1rem 1.5rem;
    color: var(--text-color);
    font-weight: 500;
    transition: all 0.3s;
}

.main-nav a i {
    margin-right: 0.5rem;
}

.main-nav a:hover {
    background-color: #f8f9fa;
    color: var(--primary-color);
}

.main-nav .active a {
    color: var(--primary-color);
    border-bottom: 3px solid var(--primary-color);
}

/* Dashboard Styles */
.dashboard h2 {
    color: var(--primary-color);
    margin-bottom: 1.5rem;
}

.dashboard-stats {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(240px, 1fr));
    gap: 1.5rem;
    margin-bottom: 2rem;
}

.stat-card {
    background-color: white;
    border-radius: 8px;
    box-shadow: 0 2px 10px rgba(0, 0, 0, 0.05);
    padding: 1.5rem;
    display: flex;
    align-items: center;
}

.stat-icon {
    background-color: rgba(26, 59, 93, 0.1);
    color: var(--primary-color);
    width: 50px;
    height: 50px;
    border-radius: 50%;
    display: flex;
    justify-content: center;
    align-items: center;
    font-size: 1.5rem;
    margin-right: 1rem;
}

.stat-content h3 {
    font-size: 0.9rem;
    color: #6c757d;
    margin-bottom: 0.3rem;
}

.stat-number {
    font-size: 1.5rem;
    font-weight: 600;
    color: var(--primary-color);
}

.stat-period {
    font-size: 0.8rem;
    color: #6c757d;
}

.dashboard-tables {
    display: grid;
    grid-template-columns: 1fr;
    gap: 1.5rem;
}

.recent-activity {
    background-color: white;
    border-radius: 8px;
    box-shadow: 0 2px 10px rgba(0, 0, 0, 0.05);
    padding: 1.5rem;
}

.recent-activity h3 {
    color: var(--primary-color);
    margin-bottom: 1rem;
    display: flex;
    align-items: center;
    gap: 0.5rem;
}

table {
    width: 100%;
    border-collapse: collapse;
}

table th, table td {
    padding: 0.75rem;
    text-align: left;
    border-bottom: 1px solid var(--border-color);
}

table th {
    font-weight: 600;
    color: var(--primary-color);
}

.status-complete {
    background-color: rgba(40, 167, 69, 0.1);
    color: var(--success-color);
    padding: 0.25rem 0.5rem;
    border-radius: 4px;
    font-size: 0.8rem;
}

.status-pending {
    background-color: rgba(255, 193, 7, 0.1);
    color: var(--warning-color);
    padding: 0.25rem 0.5rem;
    border-radius: 4px;
    font-size: 0.8rem;
}

/* Footer Styles */
.footer {
    background-color: var(--primary-color);
    color: #ddd;
    padding: 1.5rem 2rem;
    margin-top: auto;
}

.footer-content {
    display: flex;
    justify-content: space-between;
    align-items: center;
    max-width: 1200px;
    margin: 0 auto;
    flex-wrap: wrap;
    gap: 1rem;
}

.footer-section {
    font-size: 0.9rem;
}

.footer-section.links a {
    color: #ddd;
    margin: 0 0.25rem;
}

.footer-section.links a:hover {
    color: white;
}

/* Container Styles */
.container {
    display: flex;
    flex-wrap: wrap;
    gap: 20px; /* Space between columns */
    margin-bottom: 20px; /* Space between sections */
    color: var(--primary-color); /* Text color */
    background-color: white; /* White background */
    border-radius: 15px; /* Rounded corners */
    padding: 20px; /* Inner spacing */
    width: 90%; /* Increase width to 90% of its parent */
    max-width: 1200px; /* Maximum width for larger screens */
    margin-left: auto; /* Center the container */
    margin-right: auto; /* Center the container */
    box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1); /* Optional: Add a subtle shadow */

}

.filter-group {
    margin-bottom: 15px;
}

.section {
    margin-bottom: 20px; /* Adds space between each section */
}

label {
    display: block; /* Makes the label take up the full width, forcing the select to go to the next line */
    margin-bottom: 5px; /* Adds a small space between the label and the dropdown */
}

select {
        width: 100%; /* Makes the dropdown take up the full width of its container */
        padding: 5px; /* Adds some padding inside the dropdown */
}

/* Basic reset of search clients */

form {
    margin-bottom: 20px;
}

label {
    display: block;
    margin-bottom: 5px;
    font-weight: bold;
}

input[type="number"], select, input[type="radio"] {
    margin-bottom: 10px;
}

input[type="number"], select {
    width: 100%;
    padding: 10px;
    border: 1px solid #ddd;
    border-radius: 4px;
}

.radio-group {
    margin-bottom: 15px;
}

.radio-label {
    display: inline-block;
    margin-right: 15px;
    font-weight: normal;
}

.search-section {
    margin-bottom: 20px;
    padding: 15px;
    border: 1px solid #eee;
    border-radius: 5px;
    background-color: #f9f9f9;
}

.search-section-title {
    font-weight: bold;
    margin-bottom: 10px;
    color: #2c3e50;
}
table {
    width: 100%;
    border-collapse: collapse;
    margin-top: 20px;
}


.hidden {
    display: none;
}

/* Section Title Styles */
.section-title {
    margin: 0; /* Remove default margin */
    font-size: 15px; /* Increase font size */
    color: var(--primary-color); /* Use primary color for the title */
    width: 100%; /* Increase width to 90% of its parent */
}

.col {
    flex: 1; /* Each column takes equal space */
    min-width: 50px; /* Minimum width for responsiveness */
}

/* Form Group Styles */
.form-group {
    margin-bottom: 15px;
}

.form-group label {
    display: block;
    margin-bottom: 5px;
    font-weight: bold;
}

.form-group input {
    width: 100%;
    padding: 8px;
    box-sizing: border-box;
    border: 1px solid #ccc;
    border-radius: 4px;
}

/* Responsive adjustments */
@media (max-width: 768px) {
    .header {
        flex-direction: column;
        text-align: center;
        padding: 1rem;
    }

    .header-right {
        margin-top: 1rem;
        justify-content: center;
    }

    .main-nav ul {
        flex-direction: column;
    }

    .dashboard-stats {
        grid-template-columns: 1fr;
    }

    .footer-content {
        flex-direction: column;
        text-align: center;
    }
}
"""

# HTML templates as string variables
login_template = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Excellent Bank Admin - Login</title>
    <style>
        {{ css }}
    </style>
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0-beta3/css/all.min.css">
</head>
<body>
    <!-- Header -->
    <header class="header">
        <div class="logo-container">
            <i class="fas fa-university logo-icon"></i>
            <h1>Excellent Bank</h1>
        </div>
        <div class="header-right">
            <span class="system-time" id="current-time"></span>
        </div>
    </header>

    <!-- Main Content -->
    <main class="main-content login-container">
        <div class="login-card">
            <div class="login-header">
                <h2>Admin Portal Login</h2>
                <p>Enter your credentials to access the banking administration system</p>
            </div>

            {% if error %}
            <div class="alert alert-danger">
                {{ error }}
            </div>
            {% endif %}

            {% with messages = get_flashed_messages(with_categories=true) %}
                {% if messages %}
                    {% for category, message in messages %}
                    <div class="alert alert-{{ category }}">
                        {{ message }}
                    </div>
                    {% endfor %}
                {% endif %}
            {% endwith %}

            <form action="{{ url_for('login') }}" method="post" class="login-form">
                <div class="form-group">
                    <label for="username"><i class="fas fa-user"></i> Username</label>
                    <input type="text" id="username" name="username" required>
                </div>
                <div class="form-group">
                    <label for="password"><i class="fas fa-lock"></i> Password</label>
                    <input type="password" id="password" name="password" required>
                </div>
                <div class="form-actions">
                    <button type="submit" class="btn btn-primary">Login <i class="fas fa-sign-in-alt"></i></button>
                </div>
                <div class="form-footer">
                    <a href="#" class="forgot-password">Forgot Password?</a>
                </div>
            </form>
        </div>
    </main>

    <!-- Footer -->
    <footer class="footer">
        <div class="footer-content">
            <div class="footer-section">
                <p>&copy; 2025 Excellent Bank Administration System. All rights reserved.</p>
            </div>
            <div class="footer-section">
                <p><i class="fas fa-shield-alt"></i> Protected by enterprise-grade security</p>
            </div>
            <div class="footer-section links">
                <a href="#">Privacy Policy</a> | 
                <a href="#">Terms of Service</a> | 
                <a href="#">Contact IT Support</a>
            </div>
        </div>
    </footer>

    <script>
        // Display current time
        function updateTime() {
            const now = new Date();
            document.getElementById('current-time').textContent = now.toLocaleString();
        }
        updateTime();
        setInterval(updateTime, 1000);
    </script>
</body>
</html>
"""

# Mock user database - in a real application, use a secure database
users = {
    "admin": {
        "password": "admin123",  # In production, use password hashing
        "role": "admin"
    },
    "manager": {
        "password": "manager123",
        "role": "manager"
    }
}

# Mock client database
clients = {}

# Chart function based on the client balance distribution
def generate_graphs(filtered_data, age_type="single"):
    """
    Generate graphs based on the age selection type:
    1. For single age: Two graphs (balance by age intervals and deposit distribution)
    2. For age range: Add a third graph showing detailed age distribution within the range
    """
    # For single age selection, use the original two graphs
    if age_type == "single" and 'age' in filtered_data.columns:
        # Reduce the figure size to make the graph smaller
        plt.figure(figsize=(12, 6))  # Adjusted from (15, 6) to (12, 5)

        # --- Graph 1: Numero di persone per ogni età specifica ---
        plt.subplot(1, 3, 1)

        # Supponiamo che la colonna 'housing' contenga la distribuzione del prestito per abitazione (Yes/No)
        housing_counts = filtered_data['housing'].value_counts()  # Conta le occorrenze di "housing" (Yes/No)

        # Crea il grafico a barre con seaborn
        bars = sns.barplot(x=housing_counts.index, y=housing_counts.values, palette='viridis')

        # Aggiungi etichette con il numero di clienti sopra ogni barra
        for i, bar in enumerate(bars.patches):
            height = bar.get_height()
            bars.text(bar.get_x() + bar.get_width() / 2., height + 0.1,
                      f'{int(height)}',  # Mostra il numero di clienti come intero
                      ha='center', va='bottom', fontweight='bold')

        # Titolo ed etichette
        plt.title('Housing Loan Distribution', fontsize=10)
        plt.xlabel('Housing Loan', fontsize=9)
        plt.ylabel('Number of Clients', fontsize=9)
        plt.grid(True, linestyle='--', alpha=0.6)

        # --- Graph 2: Deposit Distribution (Yes/No) ---
        plt.subplot(1, 3, 2)  # Create a subplot for the second graph
        deposit_counts = filtered_data['deposit'].value_counts()
        bars = sns.barplot(x=deposit_counts.index, y=deposit_counts.values, palette='viridis')

        # Add text labels on top of the bars
        for i, bar in enumerate(bars.patches):
            height = bar.get_height()
            bars.text(bar.get_x() + bar.get_width() / 2., height + 0.1,
                      f'{int(height)}',
                      ha='center', va='bottom', fontweight='bold')

        plt.title('Deposit Distribution', fontsize=10)
        plt.xlabel('Deposit', fontsize=9)
        plt.ylabel('Number of Clients', fontsize=9)
        plt.grid(True, linestyle='--', alpha=0.6)

        # --- Graph 3: Loan Distribution (Yes/No) ---
        plt.subplot(1, 3, 3)
        # Supponiamo che la colonna 'loan' contenga la distribuzione del prestito (Yes/No)
        loan_counts = filtered_data['loan'].value_counts()  # Conta le occorrenze di "loan" (Yes/No)

        # Crea il grafico a barre con seaborn
        bars = sns.barplot(x=loan_counts.index, y=loan_counts.values, palette='viridis')

        # Aggiungi etichette con il numero di clienti sopra ogni barra
        for i, bar in enumerate(bars.patches):
            height = bar.get_height()
            bars.text(bar.get_x() + bar.get_width() / 2., height + 0.1,
                      f'{int(height)}',  # Mostra il numero di clienti come intero
                      ha='center', va='bottom', fontweight='bold')

        # Titolo ed etichette
        plt.title('Loan Distribution', fontsize=10)
        plt.xlabel('Loan', fontsize=9)
        plt.ylabel('Number of Clients', fontsize=9)
        plt.grid(True, linestyle='--', alpha=0.6)

    # For age range selection, create three graphs in a better layout
    elif age_type == "range" and 'age' in filtered_data.columns:
        plt.figure(figsize=(10, 8))

        # --- Graph 1: Bilancio medio per ogni età specifica nell'intervallo ---
        plt.subplot(2, 2, 1)

        # Raggruppa per età specifica (non per intervalli) e calcola il bilancio medio
        average_balance = filtered_data.groupby('age')['balance'].mean().reset_index()

        # Ordina per età
        average_balance = average_balance.sort_values('age')

        # Crea il grafico a barre
        bars = plt.bar(average_balance['age'], average_balance['balance'],
                       color='blue', alpha=0.7, width=0.8)

        # Aggiungi etichette con il valore medio sopra ogni barra
        for bar in bars:
            height = bar.get_height()
            plt.text(bar.get_x() + bar.get_width() / 2., height + 5,
                     f'€{height:.2f}',
                     ha='center', va='bottom', fontsize=5, rotation=0, color="black")

        plt.title('Average Balance for every age', fontsize=10)
        plt.xlabel('Age', fontsize=9)
        plt.ylabel('Average Balance (€)', fontsize=9)
        plt.grid(True, linestyle='--', alpha=0.6)

        # Imposta le etichette sull'asse x per mostrare ogni età nell'intervallo
        plt.xticks(average_balance['age'])

        # --- Graph 2: Deposit Distribution (Yes/No) ---
        plt.subplot(2, 2, 2)  # Top-right position
        deposit_counts = filtered_data['deposit'].value_counts()
        bars = sns.barplot(x=deposit_counts.index, y=deposit_counts.values, palette='viridis')

        # Add text labels on top of the bars
        for i, bar in enumerate(bars.patches):
            height = bar.get_height()
            bars.text(bar.get_x() + bar.get_width() / 2., height + 0.1,
                      f'{int(height)}',
                      ha='center', va='bottom', fontsize=9)

        plt.title('Deposit Distribution', fontsize=10)
        plt.xlabel('Deposit', fontsize=9)
        plt.ylabel('Number of Clients', fontsize=9)
        plt.grid(True, linestyle='--', alpha=0.6)
        plt.tight_layout()  # Adjust spacing between plots

        # --- Graph 3: Age Distribution within Selected Range ---
        plt.subplot(2, 1, 2)  # Bottom full-width position
        ax = sns.histplot(filtered_data['age'], bins=min(30, len(filtered_data['age'].unique())),
                          kde=True, color='purple')

        # Add count text above each histogram bar selectively
        max_height = max([p.get_height() for p in ax.patches]) if ax.patches else 0
        threshold = max_height * 0.1  # Only label bars with at least 10% of max height

        for p in ax.patches:
            height = p.get_height()
            if height > threshold:  # Only add text if the bar has significant height
                ax.text(p.get_x() + p.get_width() / 2., height + 0.1,
                        f'{int(height)}',
                        ha='center', va='bottom', fontsize=8)

        plt.title('Age Distribution within Selected Range', fontsize=10)
        plt.xlabel('Age', fontsize=9)
        plt.ylabel('Number of Clients', fontsize=9)
        plt.grid(True, linestyle='--', alpha=0.6)
        plt.tight_layout()  # Adjust spacing between plots

    # Save the combined graph to a bytes buffer with tight layout
    buf = io.BytesIO()
    plt.tight_layout(pad=1.5)  # Add padding around the entire figure
    plt.savefig(buf, format='png', bbox_inches='tight', dpi=100)
    plt.close()
    buf.seek(0)

    # Convert the graph to a base64-encoded string
    graph_url = base64.b64encode(buf.getvalue()).decode('utf-8')
    return graph_url

# Generating the statement of the results
def generate_statement(filtered_data, age=None, age_range=None, job=None, marital=None, education=None, loan=None,
                       housing=None, month=None):
    """
    Generate statement of client balances by age and job and marital and education type.
    """
    deposit_counts = filtered_data['deposit'].value_counts()
    majority_deposit = deposit_counts.idxmax()
    majority_count = deposit_counts.max()
    minority_count = deposit_counts.min()

    # Generating the selection text
    selection_text = []
    if age:
        selection_text.append(f"<i>age</i> = <b>{age}</b>")
    if age_range:
        selection_text.append(f"<i>age range</i> = <b>{age_range}</b>")
    if job:
        selection_text.append(f"<i>job</i> = <b>{job}</b>")
    if marital:
        selection_text.append(f"<i>marital</i> = <b>{marital}</b>")
    if education:
        selection_text.append(f"<i>education</i> = <b>{education}</b>")
    if loan:
        selection_text.append(f"<i>loan</i> = <b>{loan}</b>")
    if housing:
        selection_text.append(f"<i>housing</i> = <b>{housing}</b>")
    if month:
        selection_text.append(f"<i>month</i> = <b>{month}</b>")

    selection_text = " <i>and</i> ".join(selection_text)

    # Generate the statement
    if majority_deposit == "yes":
        statement = (f"This is the result of {selection_text}.\n"
                     f"The <b>majority</b> of people (<b>{majority_count}</b>) have a deposit, while the <b>minority</b> (<b>{minority_count}</b>) does not.")
    else:
        statement = (f"This is the result of {selection_text}.\n"
                     f"The <b>majority</b> of people (<b>{majority_count}</b>) does not have a deposit, while the <b>minority</b> (<b>{minority_count}</b>) has.")

    return statement

# Login required decorator IMPORTANT TO VERIFY THE PERSON WHO LOGS IN
def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'username' not in session:
            flash('Please log in to access this page', 'danger')
            return redirect(url_for('login'))
        return f(*args, **kwargs)

    return decorated_function

# MAIN PAGE
@app.route('/')
def index():
    return redirect(url_for('login'))

# ONCE ENTERING THE WEBSITE
@app.route('/login', methods=['GET', 'POST'])
def login():
    error = None
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        if username in users and users[username]['password'] == password:
            session['username'] = username
            session['role'] = users[username]['role']
            flash('You have been successfully logged in', 'success')
            return redirect(url_for('dashboard'))
        else:
            error = 'Invalid credentials. Please try again.'

    return render_template_string(login_template, css=css, error=error)

# THE ROLE OF THE STAFF MEMBER ADMIN OR MANAGER
@app.route('/dashboard')
@login_required
def dashboard():
    #codice CSS
    css = """
        /* Global Styles */
        :root {
            --primary-color: #1a3b5d;
            --secondary-color: #2d6187;
            --accent-color: #e4a013;
            --text-color: #333;
            --light-text: #f8f9fa;
            --border-color: #dee2e6;
            --success-color: #28a745;
            --danger-color: #dc3545;
            --warning-color: #ffc107;
            --info-color: #17a2b8;
        }

        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }

        body {
            font-family: Helvetica, sans-serif;
            line-height: 1.6;
            color: var(--text-color);
            background-color: #f5f7fa;
            min-height: 100vh;
            display: flex;
            flex-direction: column;
        }

        a {
            text-decoration: none;
            color: var(--secondary-color);
        }

        a:hover {
            color: var(--primary-color);
        }

        /* Header Styles */
        .header {
            background-color: var(--primary-color);
            color: white;
            padding: 1rem 2rem;
            display: flex;
            justify-content: space-between;
            align-items: center;
            box-shadow: 0 2px 5px rgba(0, 0, 0, 0.1);
        }

        .logo-container {
            display: flex;
            align-items: center;
        }

        .logo-icon {
            font-size: 2rem;
            margin-right: 10px;
            color: var(--accent-color);
        }

        .header h1 {
            font-size: 1.5rem;
            font-weight: 600;
        }

        .header-right {
            display: flex;
            align-items: center;
            gap: 1.5rem;
        }

        .system-time {
            font-size: 0.9rem;
            color: #ddd;
        }

        .user-info {
            display: flex;
            align-items: center;
            gap: 0.5rem;
            font-size: 0.9rem;
        }

        .logout-btn {
            background-color: rgba(255, 255, 255, 0.1);
            color: white;
            padding: 0.5rem 1rem;
            border-radius: 4px;
            font-size: 0.9rem;
            transition: background-color 0.3s;
        }

        .logout-btn:hover {
            background-color: rgba(255, 255, 255, 0.2);
            color: white;
        }

        /* Main Content */
        .main-content {
            flex: 1;
            padding: 2rem;
            max-width: 1200px;
            margin: 0 auto;
            width: 100%;
        }

        .login-container {
            display: flex;
            justify-content: center;
            align-items: center;
            min-height: calc(100vh - 140px);
        }

        .login-card {
            background-color: white;
            border-radius: 8px;
            box-shadow: 0 4px 15px rgba(0, 0, 0, 0.1);
            width: 100%;
            max-width: 450px;
            padding: 2rem;
        }

        .login-header {
            text-align: center;
            margin-bottom: 2rem;
        }

        .login-header h2 {
            color: var(--primary-color);
            margin-bottom: 0.5rem;
        }

        .login-header p {
            color: #6c757d;
            font-size: 0.9rem;
        }

        .login-form .form-group {
            margin-bottom: 1.5rem;
        }

        .login-form label {
            display: block;
            margin-bottom: 0.5rem;
            font-weight: 500;
            color: var(--primary-color);
        }

        .login-form input {
            width: 100%;
            padding: 0.75rem;
            border: 1px solid var(--border-color);
            border-radius: 4px;
            font-size: 1rem;
            transition: border-color 0.3s;
        }

        .login-form input:focus {
            border-color: var(--secondary-color);
            outline: none;
        }

        .form-actions {
            margin-top: 2rem;
        }

        .btn {
            display: inline-block;
            padding: 0.75rem 1.5rem;
            border-radius: 4px;
            font-weight: 500;
            cursor: pointer;
            border: none;
            transition: all 0.3s;
        }

        .btn-primary {
            background-color: var(--primary-color);
            color: white;
            width: 100%;
            font-size: 1rem;
        }

        .btn-primary:hover {
            background-color: var(--secondary-color);
        }

        .btn-danger {
            background-color: var(--danger-color);
            color: white;
            width: 100%;
            font-size: 1rem;
            border-radius: 4px;
            display: inline-block;
        }

        .btn-danger:hover {
            background-color: #c82333;
        }

        .form-footer {
            text-align: center;
            margin-top: 1.5rem;
            font-size: 0.9rem;
        }

        .forgot-password {
            color: var(--secondary-color);
        }

        /* Alerts */
        .alert {
            padding: 1rem;
            border-radius: 4px;
            margin-bottom: 1.5rem;
            font-size: 0.9rem;
        }

        .alert-danger {
            background-color: #f8d7da;
            color: #721c24;
            border: 1px solid #f5c6cb;
        }

        .alert-success {
            background-color: #d4edda;
            color: #155724;
            border: 1px solid #c3e6cb;
        }

        .alert-info {
            background-color: #d1ecf1;
            color: #0c5460;
            border: 1px solid #bee5eb;
        }

        /* Navigation */
        .main-nav {
            background-color: white;
            box-shadow: 0 2px 5px rgba(0, 0, 0, 0.05);
        }

        .main-nav ul {
            list-style: none;
            display: flex;
            max-width: 1200px;
            margin: 0 auto;
            padding: 0 2rem;
        }

        .main-nav li {
            position: relative;
        }

        .main-nav a {
            display: block;
            padding: 1rem 1.5rem;
            color: var(--text-color);
            font-weight: 500;
            transition: all 0.3s;
        }

        .main-nav a i {
            margin-right: 0.5rem;
        }

        .main-nav a:hover {
            background-color: #f8f9fa;
            color: var(--primary-color);
        }

        .main-nav .active a {
            color: var(--primary-color);
            border-bottom: 3px solid var(--primary-color);
        }

        /* Dashboard Styles */
        .dashboard h2 {
            color: var(--primary-color);
            margin-bottom: 1.5rem;
        }

        .dashboard-stats {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(240px, 1fr));
            gap: 1.5rem;
            margin-bottom: 2rem;
        }

        .stat-card {
            background-color: white;
            border-radius: 8px;
            box-shadow: 0 2px 10px rgba(0, 0, 0, 0.05);
            padding: 1.5rem;
            display: flex;
            align-items: center;
        }

        .stat-icon {
            background-color: rgba(26, 59, 93, 0.1);
            color: var(--primary-color);
            width: 50px;
            height: 50px;
            border-radius: 50%;
            display: flex;
            justify-content: center;
            align-items: center;
            font-size: 1.5rem;
            margin-right: 1rem;
        }

        .stat-content h3 {
            font-size: 0.9rem;
            color: #6c757d;
            margin-bottom: 0.3rem;
        }

        .stat-number {
            font-size: 1.5rem;
            font-weight: 600;
            color: var(--primary-color);
        }

        .stat-period {
            font-size: 0.8rem;
            color: #6c757d;
        }

        .dashboard-tables {
            display: grid;
            grid-template-columns: 1fr;
            gap: 1.5rem;
        }

        .recent-activity {
            background-color: white;
            border-radius: 8px;
            box-shadow: 0 2px 10px rgba(0, 0, 0, 0.05);
            padding: 1.5rem;
        }

        .recent-activity h3 {
            color: var(--primary-color);
            margin-bottom: 1rem;
            display: flex;
            align-items: center;
            gap: 0.5rem;
        }

        table {
            width: 100%;
            border-collapse: collapse;
        }

        table th, table td {
            padding: 0.75rem;
            text-align: left;
            border-bottom: 1px solid var(--border-color);
        }

        table th {
            font-weight: 600;
            color: var(--primary-color);
        }

        .status-complete {
            background-color: rgba(40, 167, 69, 0.1);
            color: var(--success-color);
            padding: 0.25rem 0.5rem;
            border-radius: 4px;
            font-size: 0.8rem;
        }

        .status-pending {
            background-color: rgba(255, 193, 7, 0.1);
            color: var(--warning-color);
            padding: 0.25rem 0.5rem;
            border-radius: 4px;
            font-size: 0.8rem;
        }

        /* Footer Styles */
        .footer {
            background-color: var(--primary-color);
            color: #ddd;
            padding: 1.5rem 2rem;
            margin-top: auto;
        }

        .footer-content {
            display: flex;
            justify-content: space-between;
            align-items: center;
            max-width: 1200px;
            margin: 0 auto;
            flex-wrap: wrap;
            gap: 1rem;
        }

        .footer-section {
            font-size: 0.9rem;
        }

        .footer-section.links a {
            color: #ddd;
            margin: 0 0.25rem;
        }

        .footer-section.links a:hover {
            color: white;
        }

        /* Container Styles */
        .container {
            display: flex;
            flex-wrap: wrap;
            gap: 20px; /* Space between columns */
            margin-bottom: 20px; /* Space between sections */
            color: var(--primary-color); /* Text color */
            background-color: white; /* White background */
            border-radius: 15px; /* Rounded corners */
            padding: 20px; /* Inner spacing */
            width: 90%; /* Increase width to 90% of its parent */
            max-width: 1200px; /* Maximum width for larger screens */
            margin-left: auto; /* Center the container */
            margin-right: auto; /* Center the container */
            box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1); /* Optional: Add a subtle shadow */

        }

        .filter-group {
            margin-bottom: 15px;
        }

        .section {
            margin-bottom: 20px; /* Adds space between each section */
        }

        label {
            display: block; /* Makes the label take up the full width, forcing the select to go to the next line */
            margin-bottom: 5px; /* Adds a small space between the label and the dropdown */
        }

        select {
                width: 100%; /* Makes the dropdown take up the full width of its container */
                padding: 5px; /* Adds some padding inside the dropdown */
        }

        /* Basic reset of search clients */

        form {
            margin-bottom: 20px;
        }

        label {
            display: block;
            margin-bottom: 5px;
            font-weight: bold;
        }

        input[type="number"], select, input[type="radio"] {
            margin-bottom: 10px;
        }

        input[type="number"], select {
            width: 100%;
            padding: 10px;
            border: 1px solid #ddd;
            border-radius: 4px;
        }

        .radio-group {
            margin-bottom: 15px;
        }

        .radio-label {
            display: inline-block;
            margin-right: 15px;
            font-weight: normal;
        }

        .search-section {
            margin-bottom: 20px;
            padding: 15px;
            border: 1px solid #eee;
            border-radius: 5px;
            background-color: #f9f9f9;
        }

        .search-section-title {
            font-weight: bold;
            margin-bottom: 10px;
            color: #2c3e50;
        }
        table {
            width: 100%;
            border-collapse: collapse;
            margin-top: 20px;
        }


        .hidden {
            display: none;
        }

        /* Section Title Styles */
        .section-title {
            margin: 0; /* Remove default margin */
            font-size: 15px; /* Increase font size */
            color: var(--primary-color); /* Use primary color for the title */
            width: 100%; /* Increase width to 90% of its parent */
        }

        .col {
            flex: 1; /* Each column takes equal space */
            min-width: 50px; /* Minimum width for responsiveness */
        }

        /* Form Group Styles */
        .form-group {
            margin-bottom: 15px;
        }

        .form-group label {
            display: block;
            margin-bottom: 5px;
            font-weight: bold;
        }

        .form-group input {
            width: 100%;
            padding: 8px;
            box-sizing: border-box;
            border: 1px solid #ccc;
            border-radius: 4px;
        }

        /* Responsive adjustments */
        @media (max-width: 768px) {
            .header {
                flex-direction: column;
                text-align: center;
                padding: 1rem;
            }

            .header-right {
                margin-top: 1rem;
                justify-content: center;
            }

            .main-nav ul {
                flex-direction: column;
            }

            .dashboard-stats {
                grid-template-columns: 1fr;
            }

            .footer-content {
                flex-direction: column;
                text-align: center;
            }
        }
        """
    #codice HTML
    dashboard_template = """
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <link href="https://fonts.googleapis.com/css2?family=Roboto:wght@400;700&display=swap" rel="stylesheet">
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Excellent Bank Admin - Dashboard</title>
        <style> {{css}} </style>
        <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0-beta3/css/all.min.css">
    </head>
    <body>
        <!-- Header -->
        <header class="header">
            <div class="logo-container">
                <i class="fas fa-university logo-icon"></i>
                <h1>Excellent Bank</h1>
            </div>
            <div class="header-right">
                <span class="user-info">
                    <i class="fas fa-user-circle"></i> {{ username }} ({{ role }})
                </span>
                <span class="system-time" id="current-time"></span>
                <a href="{{ url_for('logout') }}" class="logout-btn"><i class="fas fa-sign-out-alt"></i> Logout</a>
            </div>
        </header>

        <!-- Navigation -->
        <nav class="main-nav">
            <ul>
                <li class="active"><a href="#"><i class="fas fa-tachometer-alt"></i> Dashboard</a></li>
                <li><a href="{{ url_for('add_client') }}"><i class="fas fa-user-plus"></i> Add Client</a></li>
                <li><a href="{{ url_for('delete_client') }}"><i class="fas fa-user-minus"></i> Delete Client</a></li>
                <li><a href="{{ url_for('search_client') }}"><i class="fas fa-users"></i> Search Clients</a></li>
                <li><a href="{{ url_for('prediction_form') }}"><i class="fas fa-chart-line"></i> Prediction Report</a></li>
            </ul>
        </nav>

        <!-- Main Content -->
        <main class="main-content dashboard">
            <h2>Welcome to the Excellent Bank Administration System</h2>
            {% with messages = get_flashed_messages(with_categories=true) %}
                {% if messages %}
                    {% for category, message in messages %}
                    <div class="alert alert-{{ category }}">
                        {{ message }}
                    </div>
                    {% endfor %}
                {% endif %}
            {% endwith %}

            <div class="dashboard-stats">
                <div class="stat-card">
                    <div class="stat-icon"><i class="fas fa-solid fa-user"></i></div>
                    <div class="stat-content">
                        <h3>Accounts</h3>
                        <p class="stat-number">44,307</p>
                        <p class="stat-period"> Updated since now</p>
                    </div>
                </div>
                <div class="stat-card">
                    <div class="stat-icon"><i class="fas fa-money-bill-wave"></i></div>
                    <div class="stat-content">
                        <h3>Total Wallet</h3>
                        <p class="stat-number">$102,127</p>
                        <p class="stat-period">Max wallet of the year</p>
                    </div>
                </div>
                <div class="stat-card">
                    <div class="stat-icon"><i class="fas fa-briefcase"></i></div>
                    <div class="stat-content">
                        <h3>Client Job Stats</h3>
                        <p class="stat-number">12</p>
                        <p class="stat-period">Popular jobs by clients</p>
                    </div>
                </div>
                <div class="stat-card">
                    <div class="stat-icon"><i class="fas fa-phone"></i></div>
                    <div class="stat-content">
                        <h3>Contact History</h3>
                        <p class="stat-number">4918</p>
                        <p class="stat-period">Max duration of the year</p>
                    </div>
                </div>
            </div>

            <div class="dashboard-tables">
                <div class="recent-activity">
                    <h3><i class="fas fa-history"></i> Recent Activity</h3>
                    <table>
                        <thead>
                            <tr>
                                <th>Time</th>
                                <th>Client ID</th>
                                <th>Contact</th>
                                <th>Deposit</th>
                            </tr>
                        </thead>
                        <tbody>
                            <tr>
                                <td>10:45 AM</td>
                                <td>27891</td>
                                <td>Cellular</td>
                                <td><span class="status-pending">No</span></td>
                            </tr>
                            <tr>
                                <td>09:32 AM</td>
                                <td>12345</td>
                                <td>Unknown</td>
                                <td><span class="status-pending">No</span></td>
                            </tr>
                            <tr>
                                <td>08:17 AM</td>
                                <td>19969</td>
                                <td>Cellular</td>
                                <td><span class="status-complete">Yes</span></td>
                            </tr>
                            <tr>
                                <td>Yesterday</td>
                                <td>8192</td>
                                <td>unknown</td>
                                <td><span class="status-pending">No</span></td>
                            </tr>
                        </tbody>
                    </table>
                </div>
            </div>
        </main>

        <!-- Footer -->
        <footer class="footer">
            <div class="footer-content">
                <div class="footer-section">
                    <p>&copy; 2025 Excellent Bank Administration System. All rights reserved.</p>
                </div>
                <div class="footer-section">
                    <p><i class="fas fa-shield-alt"></i> Protected by enterprise-grade security</p>
                </div>
                <div class="footer-section links">
                    <a href="#">Privacy Policy</a> | 
                    <a href="#">Terms of Service</a> | 
                    <a href="#">Contact IT Support</a>
                </div>
            </div>
        </footer>

        <script>
            // Display current time
            function updateTime() {
                const now = new Date();
                document.getElementById('current-time').textContent = now.toLocaleString();
            }
            updateTime();
            setInterval(updateTime, 1000);
        </script>
    </body>
    </html>
    """

    return render_template_string(dashboard_template, css=css,
                                  username=session['username'],
                                  role=session['role'])

# THE ABILITY TO ADD A CLIENT
@app.route('/add_client', methods=['GET', 'POST'])
@login_required
def add_client():
    if request.method == "POST":
        try:
            # Ottieni i dati dal form
            new_client = {
                'age': request.form['age'],
                'job': request.form['job'],
                'marital': request.form['marital'],
                'education': request.form['education'],
                'default': request.form['default'],
                'balance': request.form['balance'],
                'housing': request.form['housing'],
                'loan': request.form['loan'],
                'contact': request.form['contact'],
                'day': request.form['day'],
                'month': request.form['month'],
                'duration': request.form['duration'],
                'campaign': request.form['campaign'],
                'pdays': request.form['pdays'],
                'previous': request.form['previous'],
                'poutcome': request.form['poutcome'],
                'deposit': request.form['deposit']
            }

            # Aggiorna il file CSV
            global df
            df = df._append(new_client, ignore_index=True)
            df.to_csv('Bank_Marketing.csv', sep=';', index=False)

            # Configurazione della connessione al database
            db_config = {
                'host': 'localhost',
                'user': 'root',  # Sostituisci con il tuo nome utente MySQL
                'password': '',  # Sostituisci con la tua password MySQL
                'database': 'bank_marketing'  # Sostituisci con il nome del tuo database
            }

            # Ottieni la connessione al database
            conn = mysql.connector.connect(**db_config)
            cursor = conn.cursor()

            try:
                # Ottieni l'ID del job e l'ID massimo + 1
                job_name = new_client['job']
                cursor.execute("SELECT id_job FROM jobs WHERE nome = %s", (job_name,))
                job_id = cursor.fetchone()[0]  # Recupera l'id del job

                cursor.execute("SELECT MAX(id_client) FROM client")
                id = cursor.fetchone()[0] or 0  # Ottieni l'ID massimo + 1, se non esiste setta a 0
                id += 1  # Incrementa l'ID per il nuovo client

                # Inserimento dei dati nelle tabelle
                insert_campaign = """
                    INSERT INTO campaigns (id_campaign, campaign, p_days, previous, p_outcome)
                    VALUES (%s, %s, %s, %s, %s)
                """
                values = (
                id, new_client['campaign'], new_client['pdays'], new_client['previous'], new_client['poutcome'])
                cursor.execute(insert_campaign, values)

                insert_contact_history = """
                    INSERT INTO contact_history (id_history, day_of_week, month, duration)
                    VALUES (%s, %s, %s, %s)
                """
                values = (id, new_client['day'], new_client['month'], new_client['duration'])
                cursor.execute(insert_contact_history, values)

                insert_deposit = """
                    INSERT INTO deposit (id_deposit, term_deposit) VALUES (%s, %s)
                """
                if new_client['deposit'] == 'yes':
                    values = (id, '1')
                else:
                    values = (id, '0')
                cursor.execute(insert_deposit, values)

                insert_wallet = """
                    INSERT INTO wallet (id_wallet, credit_default, balance, housing_loan, personal_loan)
                    VALUES (%s, %s, %s, %s, %s)
                """
                v_default = '1' if new_client['default'] == 'yes' else '0'
                v_housing = '1' if new_client['housing'] == 'yes' else '0'
                v_loan = '1' if new_client['loan'] == 'yes' else '0'
                values = (
                id, v_default, new_client['balance'], v_housing, v_loan)
                cursor.execute(insert_wallet, values)

                insert_client = """
                    INSERT INTO client (id_client, age, job_id, marital, education, contact, wallet_id, history_id, campaign_id, deposit_id)
                    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                """
                values = (
                    id,
                    new_client['age'],
                    job_id,  # Usa l'ID numerico recuperato
                    new_client['marital'],
                    new_client['education'],
                    new_client['contact'],
                    id,  # wallet_id
                    id,  # history_id
                    id,  # campaign_id
                    id  # deposit_id
                )
                cursor.execute(insert_client, values)

                # Commit della transazione
                conn.commit()

            except mysql.connector.Error as err:
                conn.rollback()
                return f"An error occurred while inserting data into the database {err}", 500
                # return redirect(url_for('add_client'))

            finally:
                cursor.close()
                conn.close()

            return redirect(url_for('success'))

        except Exception as e:
            return e, 500

    # CSS variable
    css = """
        /* Global Styles */
        :root {
            --primary-color: #1a3b5d;
            --secondary-color: #2d6187;
            --accent-color: #e4a013;
            --text-color: #333;
            --light-text: #f8f9fa;
            --border-color: #dee2e6;
            --success-color: #28a745;
            --danger-color: #dc3545;
            --warning-color: #ffc107;
            --info-color: #17a2b8;
        }

        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }

        body {
            font-family: Helvetica, sans-serif;
            line-height: 1.6;
            color: var(--text-color);
            background-color: #f5f7fa;
            min-height: 100vh;
            display: flex;
            flex-direction: column;
        }

        a {
            text-decoration: none;
            color: var(--secondary-color);
        }

        a:hover {
            color: var(--primary-color);
        }

        /* Header Styles */
        .header {
            background-color: var(--primary-color);
            color: white;
            padding: 1rem 2rem;
            display: flex;
            justify-content: space-between;
            align-items: center;
            box-shadow: 0 2px 5px rgba(0, 0, 0, 0.1);
        }

        .logo-container {
            display: flex;
            align-items: center;
        }

        .logo-icon {
            font-size: 2rem;
            margin-right: 10px;
            color: var(--accent-color);
        }

        .header h1 {
            font-size: 1.5rem;
            font-weight: 600;
        }

        .header-right {
            display: flex;
            align-items: center;
            gap: 1.5rem;
        }

        .system-time {
            font-size: 0.9rem;
            color: #ddd;
        }

        .user-info {
            display: flex;
            align-items: center;
            gap: 0.5rem;
            font-size: 0.9rem;
        }

        .logout-btn {
            background-color: rgba(255, 255, 255, 0.1);
            color: white;
            padding: 0.5rem 1rem;
            border-radius: 4px;
            font-size: 0.9rem;
            transition: background-color 0.3s;
        }

        .logout-btn:hover {
            background-color: rgba(255, 255, 255, 0.2);
            color: white;
        }

        /* Main Content */
        .main-content {
            flex: 1;
            padding: 2rem;
            max-width: 1200px;
            margin: 0 auto;
            width: 100%;
        }

        .login-container {
            display: flex;
            justify-content: center;
            align-items: center;
            min-height: calc(100vh - 140px);
        }

        .login-card {
            background-color: white;
            border-radius: 8px;
            box-shadow: 0 4px 15px rgba(0, 0, 0, 0.1);
            width: 100%;
            max-width: 450px;
            padding: 2rem;
        }

        .login-header {
            text-align: center;
            margin-bottom: 2rem;
        }

        .login-header h2 {
            color: var(--primary-color);
            margin-bottom: 0.5rem;
        }

        .login-header p {
            color: #6c757d;
            font-size: 0.9rem;
        }

        .login-form .form-group {
            margin-bottom: 1.5rem;
        }

        .login-form label {
            display: block;
            margin-bottom: 0.5rem;
            font-weight: 500;
            color: var(--primary-color);
        }

        .login-form input {
            width: 100%;
            padding: 0.75rem;
            border: 1px solid var(--border-color);
            border-radius: 4px;
            font-size: 1rem;
            transition: border-color 0.3s;
        }

        .login-form input:focus {
            border-color: var(--secondary-color);
            outline: none;
        }

        .form-actions {
            margin-top: 2rem;
        }

        .btn {
            display: inline-block;
            padding: 0.75rem 1.5rem;
            border-radius: 4px;
            font-weight: 500;
            cursor: pointer;
            border: none;
            transition: all 0.3s;
        }

        .btn-primary {
            background-color: var(--primary-color);
            color: white;
            width: 100%;
            font-size: 1rem;
        }

        .btn-primary:hover {
            background-color: var(--secondary-color);
        }

        .btn-danger {
            background-color: var(--danger-color);
            color: white;
            width: 100%;
            font-size: 1rem;
            border-radius: 4px;
            display: inline-block;
        }

        .btn-danger:hover {
            background-color: #c82333;
        }

        .form-footer {
            text-align: center;
            margin-top: 1.5rem;
            font-size: 0.9rem;
        }

        .forgot-password {
            color: var(--secondary-color);
        }

        /* Alerts */
        .alert {
            padding: 1rem;
            border-radius: 4px;
            margin-bottom: 1.5rem;
            font-size: 0.9rem;
        }

        .alert-danger {
            background-color: #f8d7da;
            color: #721c24;
            border: 1px solid #f5c6cb;
        }

        .alert-success {
            background-color: #d4edda;
            color: #155724;
            border: 1px solid #c3e6cb;
        }

        .alert-info {
            background-color: #d1ecf1;
            color: #0c5460;
            border: 1px solid #bee5eb;
        }

        /* Navigation */
        .main-nav {
            background-color: white;
            box-shadow: 0 2px 5px rgba(0, 0, 0, 0.05);
        }

        .main-nav ul {
            list-style: none;
            display: flex;
            max-width: 1200px;
            margin: 0 auto;
            padding: 0 2rem;
        }

        .main-nav li {
            position: relative;
        }

        .main-nav a {
            display: block;
            padding: 1rem 1.5rem;
            color: var(--text-color);
            font-weight: 500;
            transition: all 0.3s;
        }

        .main-nav a i {
            margin-right: 0.5rem;
        }

        .main-nav a:hover {
            background-color: #f8f9fa;
            color: var(--primary-color);
        }

        .main-nav .active a {
            color: var(--primary-color);
            border-bottom: 3px solid var(--primary-color);
        }

        /* Dashboard Styles */
        .dashboard h2 {
            color: var(--primary-color);
            margin-bottom: 1.5rem;
        }

        .dashboard-stats {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(240px, 1fr));
            gap: 1.5rem;
            margin-bottom: 2rem;
        }

        .stat-card {
            background-color: white;
            border-radius: 8px;
            box-shadow: 0 2px 10px rgba(0, 0, 0, 0.05);
            padding: 1.5rem;
            display: flex;
            align-items: center;
        }

        .stat-icon {
            background-color: rgba(26, 59, 93, 0.1);
            color: var(--primary-color);
            width: 50px;
            height: 50px;
            border-radius: 50%;
            display: flex;
            justify-content: center;
            align-items: center;
            font-size: 1.5rem;
            margin-right: 1rem;
        }

        .stat-content h3 {
            font-size: 0.9rem;
            color: #6c757d;
            margin-bottom: 0.3rem;
        }

        .stat-number {
            font-size: 1.5rem;
            font-weight: 600;
            color: var(--primary-color);
        }

        .stat-period {
            font-size: 0.8rem;
            color: #6c757d;
        }

        .dashboard-tables {
            display: grid;
            grid-template-columns: 1fr;
            gap: 1.5rem;
        }

        .recent-activity {
            background-color: white;
            border-radius: 8px;
            box-shadow: 0 2px 10px rgba(0, 0, 0, 0.05);
            padding: 1.5rem;
        }

        .recent-activity h3 {
            color: var(--primary-color);
            margin-bottom: 1rem;
            display: flex;
            align-items: center;
            gap: 0.5rem;
        }

        table {
            width: 100%;
            border-collapse: collapse;
        }

        table th, table td {
            padding: 0.75rem;
            text-align: left;
            border-bottom: 1px solid var(--border-color);
        }

        table th {
            font-weight: 600;
            color: var(--primary-color);
        }

        .status-complete {
            background-color: rgba(40, 167, 69, 0.1);
            color: var(--success-color);
            padding: 0.25rem 0.5rem;
            border-radius: 4px;
            font-size: 0.8rem;
        }

        .status-pending {
            background-color: rgba(255, 193, 7, 0.1);
            color: var(--warning-color);
            padding: 0.25rem 0.5rem;
            border-radius: 4px;
            font-size: 0.8rem;
        }

        /* Footer Styles */
        .footer {
            background-color: var(--primary-color);
            color: #ddd;
            padding: 1.5rem 2rem;
            margin-top: auto;
        }

        .footer-content {
            display: flex;
            justify-content: space-between;
            align-items: center;
            max-width: 1200px;
            margin: 0 auto;
            flex-wrap: wrap;
            gap: 1rem;
        }

        .footer-section {
            font-size: 0.9rem;
        }

        .footer-section.links a {
            color: #ddd;
            margin: 0 0.25rem;
        }

        .footer-section.links a:hover {
            color: white;
        }

        /* Container Styles */
        .container {
            display: flex;
            flex-wrap: wrap;
            gap: 20px; /* Space between columns */
            margin-bottom: 20px; /* Space between sections */
            color: var(--primary-color); /* Text color */
            background-color: white; /* White background */
            border-radius: 15px; /* Rounded corners */
            padding: 20px; /* Inner spacing */
            width: 90%; /* Increase width to 90% of its parent */
            max-width: 1200px; /* Maximum width for larger screens */
            margin-left: auto; /* Center the container */
            margin-right: auto; /* Center the container */
            box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1); /* Optional: Add a subtle shadow */

        }

        .filter-group {
            margin-bottom: 15px;
        }

        .section {
            margin-bottom: 20px; /* Adds space between each section */
        }

        label {
            display: block; /* Makes the label take up the full width, forcing the select to go to the next line */
            margin-bottom: 5px; /* Adds a small space between the label and the dropdown */
        }

        select {
                width: 100%; /* Makes the dropdown take up the full width of its container */
                padding: 5px; /* Adds some padding inside the dropdown */
        }

        /* Basic reset of search clients */

        form {
            margin-bottom: 20px;
        }

        label {
            display: block;
            margin-bottom: 5px;
            font-weight: bold;
        }

        input[type="number"], select, input[type="radio"] {
            margin-bottom: 10px;
        }

        input[type="number"], select {
            width: 100%;
            padding: 10px;
            border: 1px solid #ddd;
            border-radius: 4px;
        }

        .radio-group {
            margin-bottom: 15px;
        }

        .radio-label {
            display: inline-block;
            margin-right: 15px;
            font-weight: normal;
        }

        .search-section {
            margin-bottom: 20px;
            padding: 15px;
            border: 1px solid #eee;
            border-radius: 5px;
            background-color: #f9f9f9;
        }

        .search-section-title {
            font-weight: bold;
            margin-bottom: 10px;
            color: #2c3e50;
        }
        table {
            width: 100%;
            border-collapse: collapse;
            margin-top: 20px;
        }


        .hidden {
            display: none;
        }

        /* Section Title Styles */
        .section-title {
            margin: 0; /* Remove default margin */
            font-size: 15px; /* Increase font size */
            color: var(--primary-color); /* Use primary color for the title */
            width: 100%; /* Increase width to 90% of its parent */
        }

        .col {
            flex: 1; /* Each column takes equal space */
            min-width: 50px; /* Minimum width for responsiveness */
        }

        /* Form Group Styles */
        .form-group {
            margin-bottom: 15px;
        }

        .form-group label {
            display: block;
            margin-bottom: 5px;
            font-weight: bold;
        }

        .form-group input {
            width: 100%;
            padding: 8px;
            box-sizing: border-box;
            border: 1px solid #ccc;
            border-radius: 4px;
        }

        /* Responsive adjustments */
        @media (max-width: 768px) {
            .header {
                flex-direction: column;
                text-align: center;
                padding: 1rem;
            }

            .header-right {
                margin-top: 1rem;
                justify-content: center;
            }

            .main-nav ul {
                flex-direction: column;
            }

            .dashboard-stats {
                grid-template-columns: 1fr;
            }

            .footer-content {
                flex-direction: column;
                text-align: center;
            }
        }
        """
    # HTML variable
    add_client_template = """
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Excellent Bank Admin - Add Client</title>
        <style> {{css}} </style>
        <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0-beta3/css/all.min.css">
    </head>
    <body>
        <!-- Header -->
        <header class="header">
            <div class="logo-container">
                <i class="fas fa-university logo-icon"></i>
                <h1>Excellent Bank</h1>
            </div>
            <div class="header-right">
                <span class="user-info">
                    <i class="fas fa-user-circle"></i> {{ username }} ({{ role }})
                </span>
                <span class="system-time" id="current-time"></span>
                <a href="{{ url_for('logout') }}" class="logout-btn"><i class="fas fa-sign-out-alt"></i> Logout</a>
            </div>
        </header>

        <!-- Navigation -->
        <nav class="main-nav">
            <ul>
                <li><a href="{{ url_for('dashboard') }}"><i class="fas fa-tachometer-alt"></i> Dashboard</a></li>
                <li class="active"><a href="{{ url_for('add_client') }}"><i class="fas fa-user-plus"></i> Add Client</a></li>
                <li><a href="{{ url_for('delete_client') }}"><i class="fas fa-user-minus"></i> Delete Client</a></li>
                <li><a href="{{ url_for('search_client')}}"><i class="fas fa-users"></i> Search Clients</a></li>
                <li><a href="{{url_for('prediction_form') }}"><i class="fas fa-chart-line"></i> Prediction Report</a></li>
            </ul>
        </nav>

        <!-- Main Content -->
    <main class="main-content dashboard">
        <h2>Add New Client</h2>
        <form action="{{ url_for('add_client') }}" method="post">
            <!-- Personal Information Section -->
            <div class="container">
                <div class="section-title">
                    <h3>Personal Information</h3><br><br>
                    <div class="col">
                        <div class="radio-group">
                            <label for="age">Age:</label>
                            <input type="number" id="age" name="age" placeholder="Enter age" required><br><br>

                            <label for="job">Job:</label>
                            <select id="job" name="job" required>
                                <option value="">Select a job</option>
                                <option value="management">Management</option>
                                <option value="technician">Technician</option>
                                <option value="entrepreneur">Entrepreneur</option>
                                <option value="blue-collar">Blue-collar</option>
                                <option value="retired">Retired</option>
                                <option value="unknown">Unknown</option>
                            </select><br><br>

                            <label for="marital">Marital:</label>
                            <select id="marital" name="marital" required>
                                <option value="">Select marital status</option>
                                <option value="married">Married</option>
                                <option value="single">Single</option>
                                <option value="divorced">Divorced</option>
                            </select><br><br>

                            <label for="education">Education:</label>
                            <select id="education" name="education" required>
                                <option value="">Select education</option>
                                <option value="primary">Primary</option>
                                <option value="secondary">Secondary</option>
                                <option value="tertiary">Tertiary</option>
                                <option value="unknown">Unknown</option>
                            </select>
                        </div>
                    </div>
                </div>
            </div>

            <!-- Client Financial Info Section -->
            <div class="container">
                <div class="section-title">
                    <h3>Financial Information</h3><br><br>
                    <div class="col">
                        <div class="form-group">
                            <label for="default">Default:</label>
                            <select id="default" name="default" required>
                                <option value="">Select default</option>
                                <option value="yes">Yes</option>
                                <option value="no">No</option>
                            </select><br><br>

                            <label for="balance">Balance:</label>
                            <input type="number" id="balance" name="balance" placeholder="Enter balance" required><br><br>

                            <label for="housing">Housing:</label>
                            <select id="housing" name="housing" required>
                                <option value="">Select housing status</option>
                                <option value="yes">Yes</option>
                                <option value="no">No</option>
                            </select><br><br>

                            <label for="loan">Loan:</label>
                            <select id="loan" name="loan" required>
                                <option value="">Select loan</option>
                                <option value="yes">Yes</option>
                                <option value="no">No</option>
                            </select>
                        </div>
                    </div>
                </div>
            </div>

            <!-- Client Contact Info Section -->
            <div class="container">
                <div class="section-title">
                    <h3>Contact Information</h3><br><br>
                    <div class="col">
                        <div class="form-group">
                            <label for="contact">Contact:</label>
                            <select id="contact" name="contact" required>
                                <option value="">Select contact type</option>
                                <option value="cellular">Cellular</option>
                                <option value="telephone">Telephone</option>
                            </select><br><br>

                            <label for="day">Day:</label>
                            <input type="number" id="day" name="day" placeholder="Enter day" min="1" max="31" required><br><br>

                            <label for="month">Month:</label>
                            <select id="month" name="month" required>
                                <option value="">Select month</option>
                                <option value="jan">January</option>
                                <option value="feb">February</option>
                                <option value="mar">March</option>
                                <option value="apr">April</option>
                                <option value="may">May</option>
                                <option value="jun">June</option>
                                <option value="jul">July</option>
                                <option value="aug">August</option>
                                <option value="sep">September</option>
                                <option value="oct">October</option>
                                <option value="nov">November</option>
                                <option value="dec">December</option>
                            </select>
                        </div>
                    </div>
                </div>
            </div>

            <!-- Client Campaign Info Section -->
            <div class="container">
                <div class="section-title">
                    <h3>Campaign Information</h3><br><br>
                    <div class="col">
                        <div class="form-group">
                            <label for="duration">Duration:</label>
                            <input type="number" id="duration" name="duration" placeholder="Enter duration" required><br><br>

                            <label for="campaign">Campaign:</label>
                            <input type="number" id="campaign" name="campaign" placeholder="Enter campaign" required><br><br>

                            <label for="pdays">Pdays:</label>
                            <input type="number" id="pdays" name="pdays" placeholder="Enter pdays" required><br><br>

                            <label for="previous">Previous:</label>
                            <input type="number" id="previous" name="previous" placeholder="Enter previous" required><br><br>

                            <label for="poutcome">Poutcome:</label>
                            <select id="poutcome" name="poutcome" required>
                                <option value="">Select outcome</option>
                                <option value="success">Success</option>
                                <option value="failure">Failure</option>
                                <option value="other">Other</option>
                                <option value="unknown">Unknown</option>
                            </select>
                        </div>
                    </div>
                </div>
            </div>

            <!-- Client Deposit Info Section -->
            <div class="container">
                <div class="section-title">
                    <h3>Deposit Information</h3><br><br>
                    <div class="col">
                        <div class="form-group">
                            <label for="deposit">Deposit:</label>
                            <select id="deposit" name="deposit" required>
                                <option value="">Select deposit</option>
                                <option value="yes">Yes</option>
                                <option value="no">No</option>
                            </select>
                        </div>
                    </div>
                </div>
            </div>

            <!-- Submit Button -->
            <div class="container">
                <div class="col">
                    <button type="submit" class="btn btn-primary">Add Client</button>
                </div>
            </div>
        </form>
    </main>

        <!-- Footer -->
        <footer class="footer">
            <div class="footer-content">
                <div class="footer-section">
                    <p>&copy; 2025 Excellent Bank Administration System. All rights reserved.</p>
                </div>
                <div class="footer-section">
                    <p><i class="fas fa-shield-alt"></i> Protected by enterprise-grade security</p>
                </div>
                <div class="footer-section links">
                    <a href="#">Privacy Policy</a> | 
                    <a href="#">Terms of Service</a> | 
                    <a href="#">Contact IT Support</a>
                </div>
            </div>
        </footer>
    </body>
    </html>
    """
    return render_template_string(add_client_template, css=css,
                                  username=session['username'],
                                  role=session['role'])

# THE ABILITY TO DELETE THE CLIENT
@app.route('/delete_client', methods=['GET', 'POST'])
@login_required
def delete_client():
    if request.method == 'POST':
        id_client = request.form['client_id']

        try:
            # Connessione al database
            conn = mysql.connector.connect(
                host="localhost",
                user="root",
                password="",
                database="bank_marketing"
            )
            cursor = conn.cursor()

            # Verifica se il cliente esiste
            check_query = "SELECT wallet_id, history_id, campaign_id, deposit_id FROM client WHERE id_client = %s"
            cursor.execute(check_query, (id_client,))
            result = cursor.fetchone()

            if result:
                wallet_id, history_id, campaign_id, deposit_id = result

                # Eliminare i dati collegati nelle altre tabelle
                cursor.execute("DELETE FROM wallet WHERE id_wallet = %s", (wallet_id,))
                cursor.execute("DELETE FROM contact_history WHERE id_history = %s", (history_id,))
                cursor.execute("DELETE FROM campaigns WHERE id_campaign = %s", (campaign_id,))
                cursor.execute("DELETE FROM deposit WHERE id_deposit = %s", (deposit_id,))

                # Ora elimina il cliente
                cursor.execute("DELETE FROM client WHERE id_client = %s", (id_client,))

                # Commit delle modifiche
                conn.commit()

                cursor.close()
                conn.close()

                return redirect(url_for('delete_success'))
            else:
                cursor.close()
                conn.close()
                return "Nessun cliente trovato con i criteri specificati"

        except mysql.connector.Error as err:
            return f"Errore database: {err}"
        except Exception as e:
            return f"Errore generale: {e}"

        # CSS variable
    css = """
                            /* Global Styles */
                            :root {
                                --primary-color: #1a3b5d;
                                --secondary-color: #2d6187;
                                --accent-color: #e4a013;
                                --text-color: #333;
                                --light-text: #f8f9fa;
                                --border-color: #dee2e6;
                                --success-color: #28a745;
                                --danger-color: #dc3545;
                                --warning-color: #ffc107;
                                --info-color: #17a2b8;
                            }

                            * {
                                margin: 0;
                                padding: 0;
                                box-sizing: border-box;
                            }

                            body {
                                font-family: Helvetica, sans-serif;
                                line-height: 1.6;
                                color: var(--text-color);
                                background-color: #f5f7fa;
                                min-height: 100vh;
                                display: flex;
                                flex-direction: column;
                            }

                            a {
                                text-decoration: none;
                                color: var(--secondary-color);
                            }

                            a:hover {
                                color: var(--primary-color);
                            }

                            /* Header Styles */
                            .header {
                                background-color: var(--primary-color);
                                color: white;
                                padding: 1rem 2rem;
                                display: flex;
                                justify-content: space-between;
                                align-items: center;
                                box-shadow: 0 2px 5px rgba(0, 0, 0, 0.1);
                            }

                            .logo-container {
                                display: flex;
                                align-items: center;
                            }

                            .logo-icon {
                                font-size: 2rem;
                                margin-right: 10px;
                                color: var(--accent-color);
                            }

                            .header h1 {
                                font-size: 1.5rem;
                                font-weight: 600;
                            }

                            .header-right {
                                display: flex;
                                align-items: center;
                                gap: 1.5rem;
                            }

                            .system-time {
                                font-size: 0.9rem;
                                color: #ddd;
                            }

                            .user-info {
                                display: flex;
                                align-items: center;
                                gap: 0.5rem;
                                font-size: 0.9rem;
                            }

                            .logout-btn {
                                background-color: rgba(255, 255, 255, 0.1);
                                color: white;
                                padding: 0.5rem 1rem;
                                border-radius: 4px;
                                font-size: 0.9rem;
                                transition: background-color 0.3s;
                            }

                            .logout-btn:hover {
                                background-color: rgba(255, 255, 255, 0.2);
                                color: white;
                            }

                            /* Main Content */
                            .main-content {
                                flex: 1;
                                padding: 2rem;
                                max-width: 1200px;
                                margin: 0 auto;
                                width: 100%;
                            }

                            .login-container {
                                display: flex;
                                justify-content: center;
                                align-items: center;
                                min-height: calc(100vh - 140px);
                            }

                            .login-card {
                                background-color: white;
                                border-radius: 8px;
                                box-shadow: 0 4px 15px rgba(0, 0, 0, 0.1);
                                width: 100%;
                                max-width: 450px;
                                padding: 2rem;
                            }

                            .login-header {
                                text-align: center;
                                margin-bottom: 2rem;
                            }

                            .login-header h2 {
                                color: var(--primary-color);
                                margin-bottom: 0.5rem;
                            }

                            .login-header p {
                                color: #6c757d;
                                font-size: 0.9rem;
                            }

                            .login-form .form-group {
                                margin-bottom: 1.5rem;
                            }

                            .login-form label {
                                display: block;
                                margin-bottom: 0.5rem;
                                font-weight: 500;
                                color: var(--primary-color);
                            }

                            .login-form input {
                                width: 100%;
                                padding: 0.75rem;
                                border: 1px solid var(--border-color);
                                border-radius: 4px;
                                font-size: 1rem;
                                transition: border-color 0.3s;
                            }

                            .login-form input:focus {
                                border-color: var(--secondary-color);
                                outline: none;
                            }

                            .form-actions {
                                margin-top: 2rem;
                            }

                            .btn {
                                display: inline-block;
                                padding: 0.75rem 1.5rem;
                                border-radius: 4px;
                                font-weight: 500;
                                cursor: pointer;
                                border: none;
                                transition: all 0.3s;
                            }

                            .btn-primary {
                                background-color: var(--primary-color);
                                color: white;
                                width: 100%;
                                font-size: 1rem;
                            }

                            .btn-primary:hover {
                                background-color: var(--secondary-color);
                            }

                            .btn-danger {
                                background-color: var(--danger-color);
                                color: white;
                                width: 100%;
                                font-size: 1rem;
                                border-radius: 4px;
                                display: inline-block;
                            }

                            .btn-danger:hover {
                                background-color: #c82333;
                            }

                            .form-footer {
                                text-align: center;
                                margin-top: 1.5rem;
                                font-size: 0.9rem;
                            }

                            .forgot-password {
                                color: var(--secondary-color);
                            }

                            /* Alerts */
                            .alert {
                                padding: 1rem;
                                border-radius: 4px;
                                margin-bottom: 1.5rem;
                                font-size: 0.9rem;
                            }

                            .alert-danger {
                                background-color: #f8d7da;
                                color: #721c24;
                                border: 1px solid #f5c6cb;
                            }

                            .alert-success {
                                background-color: #d4edda;
                                color: #155724;
                                border: 1px solid #c3e6cb;
                            }

                            .alert-info {
                                background-color: #d1ecf1;
                                color: #0c5460;
                                border: 1px solid #bee5eb;
                            }

                            /* Navigation */
                            .main-nav {
                                background-color: white;
                                box-shadow: 0 2px 5px rgba(0, 0, 0, 0.05);
                            }

                            .main-nav ul {
                                list-style: none;
                                display: flex;
                                max-width: 1200px;
                                margin: 0 auto;
                                padding: 0 2rem;
                            }

                            .main-nav li {
                                position: relative;
                            }

                            .main-nav a {
                                display: block;
                                padding: 1rem 1.5rem;
                                color: var(--text-color);
                                font-weight: 500;
                                transition: all 0.3s;
                            }

                            .main-nav a i {
                                margin-right: 0.5rem;
                            }

                            .main-nav a:hover {
                                background-color: #f8f9fa;
                                color: var(--primary-color);
                            }

                            .main-nav .active a {
                                color: var(--primary-color);
                                border-bottom: 3px solid var(--primary-color);
                            }

                            /* Dashboard Styles */
                            .dashboard h2 {
                                color: var(--primary-color);
                                margin-bottom: 1.5rem;
                            }

                            .dashboard-stats {
                                display: grid;
                                grid-template-columns: repeat(auto-fit, minmax(240px, 1fr));
                                gap: 1.5rem;
                                margin-bottom: 2rem;
                            }

                            .stat-card {
                                background-color: white;
                                border-radius: 8px;
                                box-shadow: 0 2px 10px rgba(0, 0, 0, 0.05);
                                padding: 1.5rem;
                                display: flex;
                                align-items: center;
                            }

                            .stat-icon {
                                background-color: rgba(26, 59, 93, 0.1);
                                color: var(--primary-color);
                                width: 50px;
                                height: 50px;
                                border-radius: 50%;
                                display: flex;
                                justify-content: center;
                                align-items: center;
                                font-size: 1.5rem;
                                margin-right: 1rem;
                            }

                            .stat-content h3 {
                                font-size: 0.9rem;
                                color: #6c757d;
                                margin-bottom: 0.3rem;
                            }

                            .stat-number {
                                font-size: 1.5rem;
                                font-weight: 600;
                                color: var(--primary-color);
                            }

                            .stat-period {
                                font-size: 0.8rem;
                                color: #6c757d;
                            }

                            .dashboard-tables {
                                display: grid;
                                grid-template-columns: 1fr;
                                gap: 1.5rem;
                            }

                            .recent-activity {
                                background-color: white;
                                border-radius: 8px;
                                box-shadow: 0 2px 10px rgba(0, 0, 0, 0.05);
                                padding: 1.5rem;
                            }

                            .recent-activity h3 {
                                color: var(--primary-color);
                                margin-bottom: 1rem;
                                display: flex;
                                align-items: center;
                                gap: 0.5rem;
                            }

                            table {
                                width: 100%;
                                border-collapse: collapse;
                            }

                            table th, table td {
                                padding: 0.75rem;
                                text-align: left;
                                border-bottom: 1px solid var(--border-color);
                            }

                            table th {
                                font-weight: 600;
                                color: var(--primary-color);
                            }

                            .status-complete {
                                background-color: rgba(40, 167, 69, 0.1);
                                color: var(--success-color);
                                padding: 0.25rem 0.5rem;
                                border-radius: 4px;
                                font-size: 0.8rem;
                            }

                            .status-pending {
                                background-color: rgba(255, 193, 7, 0.1);
                                color: var(--warning-color);
                                padding: 0.25rem 0.5rem;
                                border-radius: 4px;
                                font-size: 0.8rem;
                            }

                            /* Footer Styles */
                            .footer {
                                background-color: var(--primary-color);
                                color: #ddd;
                                padding: 1.5rem 2rem;
                                margin-top: auto;
                            }

                            .footer-content {
                                display: flex;
                                justify-content: space-between;
                                align-items: center;
                                max-width: 1200px;
                                margin: 0 auto;
                                flex-wrap: wrap;
                                gap: 1rem;
                            }

                            .footer-section {
                                font-size: 0.9rem;
                            }

                            .footer-section.links a {
                                color: #ddd;
                                margin: 0 0.25rem;
                            }

                            .footer-section.links a:hover {
                                color: white;
                            }

                            /* Container Styles */
                            .container {
                                display: flex;
                                flex-wrap: wrap;
                                gap: 20px; /* Space between columns */
                                margin-bottom: 20px; /* Space between sections */
                                color: var(--primary-color); /* Text color */
                                background-color: white; /* White background */
                                border-radius: 15px; /* Rounded corners */
                                padding: 20px; /* Inner spacing */
                                width: 90%; /* Increase width to 90% of its parent */
                                max-width: 1200px; /* Maximum width for larger screens */
                                margin-left: auto; /* Center the container */
                                margin-right: auto; /* Center the container */
                                box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1); /* Optional: Add a subtle shadow */

                            }

                            .filter-group {
                                margin-bottom: 15px;
                            }

                            .section {
                                margin-bottom: 20px; /* Adds space between each section */
                            }

                            label {
                                display: block; /* Makes the label take up the full width, forcing the select to go to the next line */
                                margin-bottom: 5px; /* Adds a small space between the label and the dropdown */
                            }

                            select {
                                    width: 100%; /* Makes the dropdown take up the full width of its container */
                                    padding: 5px; /* Adds some padding inside the dropdown */
                            }

                            /* Basic reset of search clients */

                            form {
                                margin-bottom: 20px;
                            }

                            label {
                                display: block;
                                margin-bottom: 5px;
                                font-weight: bold;
                            }

                            input[type="number"], select, input[type="radio"] {
                                margin-bottom: 10px;
                            }

                            input[type="number"], select {
                                width: 100%;
                                padding: 10px;
                                border: 1px solid #ddd;
                                border-radius: 4px;
                            }

                            .radio-group {
                                margin-bottom: 15px;
                            }

                            .radio-label {
                                display: inline-block;
                                margin-right: 15px;
                                font-weight: normal;
                            }

                            .search-section {
                                margin-bottom: 20px;
                                padding: 15px;
                                border: 1px solid #eee;
                                border-radius: 5px;
                                background-color: #f9f9f9;
                            }

                            .search-section-title {
                                font-weight: bold;
                                margin-bottom: 10px;
                                color: #2c3e50;
                            }
                            table {
                                width: 100%;
                                border-collapse: collapse;
                                margin-top: 20px;
                            }


                            .hidden {
                                display: none;
                            }

                            /* Section Title Styles */
                            .section-title {
                                margin: 0; /* Remove default margin */
                                font-size: 15px; /* Increase font size */
                                color: var(--primary-color); /* Use primary color for the title */
                                width: 100%; /* Increase width to 90% of its parent */
                            }

                            .col {
                                flex: 1; /* Each column takes equal space */
                                min-width: 50px; /* Minimum width for responsiveness */
                            }

                            /* Form Group Styles */
                            .form-group {
                                margin-bottom: 15px;
                            }

                            .form-group label {
                                display: block;
                                margin-bottom: 5px;
                                font-weight: bold;
                            }

                            .form-group input {
                                width: 100%;
                                padding: 8px;
                                box-sizing: border-box;
                                border: 1px solid #ccc;
                                border-radius: 4px;
                            }

                            /* Responsive adjustments */
                            @media (max-width: 768px) {
                                .header {
                                    flex-direction: column;
                                    text-align: center;
                                    padding: 1rem;
                                }

                                .header-right {
                                    margin-top: 1rem;
                                    justify-content: center;
                                }

                                .main-nav ul {
                                    flex-direction: column;
                                }

                                .dashboard-stats {
                                    grid-template-columns: 1fr;
                                }

                                .footer-content {
                                    flex-direction: column;
                                    text-align: center;
                                }
                            }
                            """
    # HTML variable
    delete_client_template = """
                    <!DOCTYPE html>
                    <html lang="en">
                    <head>
                        <meta charset="UTF-8">
                        <meta name="viewport" content="width=device-width, initial-scale=1.0">
                        <title>Excellent Bank Admin - Delete Client</title>
                        <style> {{ css }} </style>
                        <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0-beta3/css/all.min.css">
                    </head>
                    <body>
                        <!-- Header -->
                        <header class="header">
                            <div class="logo-container">
                                <i class="fas fa-university logo-icon"></i>
                                <h1>Excellent Bank</h1>
                            </div>
                            <div class="header-right">
                                <span class="user-info">
                                    <i class="fas fa-user-circle"></i> {{ username }} ({{ role }})
                                </span>
                                <span class="system-time" id="current-time"></span>
                                <a href="{{ url_for('logout') }}" class="logout-btn"><i class="fas fa-sign-out-alt"></i> Logout</a>
                            </div>
                        </header>

                        <!-- Navigation -->
                        <nav class="main-nav">
                            <ul>
                                <li><a href="{{ url_for('dashboard') }}"><i class="fas fa-tachometer-alt"></i> Dashboard</a></li>
                                <li><a href="{{ url_for('add_client') }}"><i class="fas fa-user-plus"></i> Add Client</a></li>
                                <li class="active"><a href="{{ url_for('delete_client') }}"><i class="fas fa-user-minus"></i> Delete Client</a></li>
                                <li><a href="{{ url_for('search_client') }}"><i class="fas fa-users"></i> Search Clients</a></li>
                                <li><a href="{{url_for('prediction_form') }}"><i class="fas fa-chart-line"></i> Prediction Report</a></li>
                            </ul>
                        </nav>

                        <!-- Main Content -->
                        <main class="main-content dashboard">
                            <h2>Delete Client</h2>
                            <form action="{{ url_for('delete_client') }}" method="post">
                                <div class="container">
                                    <div class="section-title">
                                        <div class="col">
                                            <div class="form-group">
                                                <label for="client_id">Client ID:</label>
                                                <input type="number" id="client_id" name="client_id" placeholder="Enter Client ID" required>
                                            </div>
                                        </div>
                                    </div>
                                </div>
                                <div class="container">
                                    <button type="submit" class="btn btn-danger">Delete Client</button>
                                </div>    
                            </form>
                        </main>

                        <!-- Footer -->
                        <footer class="footer">
                            <div class="footer-content">
                                <div class="footer-section">
                                    <p>&copy; 2025 Exellent Bank Administration System. All rights reserved.</p>
                                </div>
                                <div class="footer-section">
                                    <p><i class="fas fa-shield-alt"></i> Protected by enterprise-grade security</p>
                                </div>
                                <div class="footer-section links">
                                    <a href="#">Privacy Policy</a> | 
                                    <a href="#">Terms of Service</a> | 
                                    <a href="#">Contact IT Support</a>
                                </div>
                            </div>
                        </footer>
                    </body>
                    </html>
                    """

    return render_template_string(delete_client_template, css=css,
                                  username=session['username'],
                                  role=session['role'])

# THE ABILITY TO SEARCH CLIENT
@app.route('/search_client')
@login_required
def search_client():
    # Create a figure for the initial empty state
    matplotlib.use('Agg')
    plt.figure(figsize=(10, 6))
    plt.title('Client Data Visualization')
    plt.tight_layout(pad=1.5)

    # Save the empty plot to a buffer
    buf = io.BytesIO()
    plt.savefig(buf, format='png', bbox_inches='tight', dpi=100)
    plt.close('all')
    buf.seek(0)
    graph_url = base64.b64encode(buf.getvalue()).decode('utf-8')

    # Initial empty data frame
    df = pd.DataFrame()
    filtered_data = pd.DataFrame()
    data_html = filtered_data.to_html(classes='data', index=False)
    total_rows = len(filtered_data)

    # Initial statement
    statement = "Select search criteria to view client data analysis"

    # Connect to database
    conn = mysql.connector.connect(
        host="localhost",
        user="root",
        password="",
        database="bank_marketing"
    )
    cursor = conn.cursor(dictionary=True)

    # Get unique values for dropdowns
    cursor.execute("SELECT DISTINCT nome as job FROM jobs ORDER BY nome")
    job_options = [row['job'] for row in cursor.fetchall()]

    cursor.execute("SELECT DISTINCT marital FROM client ORDER BY marital")
    marital_options = [row['marital'] for row in cursor.fetchall()]

    cursor.execute("SELECT DISTINCT education FROM client ORDER BY education")
    education_options = [row['education'] for row in cursor.fetchall()]

    cursor.execute("SELECT DISTINCT personal_loan as loan FROM wallet")
    loan_options = [row['loan'] for row in cursor.fetchall()]

    cursor.execute("SELECT DISTINCT housing_loan as housing FROM wallet")
    housing_options = [row['housing'] for row in cursor.fetchall()]

    cursor.execute("SELECT DISTINCT month FROM contact_history ORDER BY month")
    month_options = [row['month'] for row in cursor.fetchall()]

    # Define age ranges
    age_ranges = ['20-30', '30-40', '40-50', '50-60', '60-70', '70-80', '80-90', '90+']

    cursor.close()
    conn.close()

    #codice CSS
    css = """
    /* Global Styles */
    :root {
        --primary-color: #1a3b5d;
        --secondary-color: #2d6187;
        --accent-color: #e4a013;
        --text-color: #333;
        --light-text: #f8f9fa;
        --border-color: #dee2e6;
        --success-color: #28a745;
        --danger-color: #dc3545;
        --warning-color: #ffc107;
        --info-color: #17a2b8;
    }

    * {
        margin: 0;
        padding: 0;
        box-sizing: border-box;
    }

    body {
        font-family: Helvetica, sans-serif;
        line-height: 1.6;
        color: var(--text-color);
        background-color: #f5f7fa;
        min-height: 100vh;
        display: flex;
        flex-direction: column;
    }

    a {
        text-decoration: none;
        color: var(--secondary-color);
    }

    a:hover {
        color: var(--primary-color);
    }

    /* Header Styles */
    .header {
        background-color: var(--primary-color);
        color: white;
        padding: 1rem 2rem;
        display: flex;
        justify-content: space-between;
        align-items: center;
        box-shadow: 0 2px 5px rgba(0, 0, 0, 0.1);
    }

    .logo-container {
        display: flex;
        align-items: center;
    }

    .logo-icon {
        font-size: 2rem;
        margin-right: 10px;
        color: var(--accent-color);
    }

    .header h1 {
        font-size: 1.5rem;
        font-weight: 600;
    }

    .header-right {
        display: flex;
        align-items: center;
        gap: 1.5rem;
    }

    .system-time {
        font-size: 0.9rem;
        color: #ddd;
    }

    .user-info {
        display: flex;
        align-items: center;
        gap: 0.5rem;
        font-size: 0.9rem;
    }

    .logout-btn {
        background-color: rgba(255, 255, 255, 0.1);
        color: white;
        padding: 0.5rem 1rem;
        border-radius: 4px;
        font-size: 0.9rem;
        transition: background-color 0.3s;
    }

    .logout-btn:hover {
        background-color: rgba(255, 255, 255, 0.2);
        color: white;
    }

    /* Main Content */
    .main-content {
        flex: 1;
        padding: 2rem;
        max-width: 1200px;
        margin: 0 auto;
        width: 100%;
    }

    .login-container {
        display: flex;
        justify-content: center;
        align-items: center;
        min-height: calc(100vh - 140px);
    }

    .login-card {
        background-color: white;
        border-radius: 8px;
        box-shadow: 0 4px 15px rgba(0, 0, 0, 0.1);
        width: 100%;
        max-width: 450px;
        padding: 2rem;
    }

    .login-header {
        text-align: center;
        margin-bottom: 2rem;
    }

    .login-header h2 {
        color: var(--primary-color);
        margin-bottom: 0.5rem;
    }

    .login-header p {
        color: #6c757d;
        font-size: 0.9rem;
    }

    .login-form .form-group {
        margin-bottom: 1.5rem;
    }

    .login-form label {
        display: block;
        margin-bottom: 0.5rem;
        font-weight: 500;
        color: var(--primary-color);
    }

    .login-form input {
        width: 100%;
        padding: 0.75rem;
        border: 1px solid var(--border-color);
        border-radius: 4px;
        font-size: 1rem;
        transition: border-color 0.3s;
    }

    .login-form input:focus {
        border-color: var(--secondary-color);
        outline: none;
    }

    .form-actions {
        margin-top: 2rem;
    }

    .btn {
        display: inline-block;
        padding: 0.75rem 1.5rem;
        border-radius: 4px;
        font-weight: 500;
        cursor: pointer;
        border: none;
        transition: all 0.3s;
    }

    .btn-primary {
        background-color: var(--primary-color);
        color: white;
        width: 100%;
        font-size: 1rem;
    }

    .btn-primary:hover {
        background-color: var(--secondary-color);
    }

    .btn-danger {
        background-color: var(--danger-color);
        color: white;
        width: 100%;
        font-size: 1rem;
        border-radius: 4px;
        display: inline-block;
    }

    .btn-danger:hover {
        background-color: #c82333;
    }

    .form-footer {
        text-align: center;
        margin-top: 1.5rem;
        font-size: 0.9rem;
    }

    .forgot-password {
        color: var(--secondary-color);
    }

    /* Alerts */
    .alert {
        padding: 1rem;
        border-radius: 4px;
        margin-bottom: 1.5rem;
        font-size: 0.9rem;
    }

    .alert-danger {
        background-color: #f8d7da;
        color: #721c24;
        border: 1px solid #f5c6cb;
    }

    .alert-success {
        background-color: #d4edda;
        color: #155724;
        border: 1px solid #c3e6cb;
    }

    .alert-info {
        background-color: #d1ecf1;
        color: #0c5460;
        border: 1px solid #bee5eb;
    }

    /* Navigation */
    .main-nav {
        background-color: white;
        box-shadow: 0 2px 5px rgba(0, 0, 0, 0.05);
    }

    .main-nav ul {
        list-style: none;
        display: flex;
        max-width: 1200px;
        margin: 0 auto;
        padding: 0 2rem;
    }

    .main-nav li {
        position: relative;
    }

    .main-nav a {
        display: block;
        padding: 1rem 1.5rem;
        color: var(--text-color);
        font-weight: 500;
        transition: all 0.3s;
    }

    .main-nav a i {
        margin-right: 0.5rem;
    }

    .main-nav a:hover {
        background-color: #f8f9fa;
        color: var(--primary-color);
    }

    .main-nav .active a {
        color: var(--primary-color);
        border-bottom: 3px solid var(--primary-color);
    }

    /* Dashboard Styles */
    .dashboard h2 {
        color: var(--primary-color);
        margin-bottom: 1.5rem;
    }

    .dashboard-stats {
        display: grid;
        grid-template-columns: repeat(auto-fit, minmax(240px, 1fr));
        gap: 1.5rem;
        margin-bottom: 2rem;
    }

    .stat-card {
        background-color: white;
        border-radius: 8px;
        box-shadow: 0 2px 10px rgba(0, 0, 0, 0.05);
        padding: 1.5rem;
        display: flex;
        align-items: center;
    }

    .stat-icon {
        background-color: rgba(26, 59, 93, 0.1);
        color: var(--primary-color);
        width: 50px;
        height: 50px;
        border-radius: 50%;
        display: flex;
        justify-content: center;
        align-items: center;
        font-size: 1.5rem;
        margin-right: 1rem;
    }

    .stat-content h3 {
        font-size: 0.9rem;
        color: #6c757d;
        margin-bottom: 0.3rem;
    }

    .stat-number {
        font-size: 1.5rem;
        font-weight: 600;
        color: var(--primary-color);
    }

    .stat-period {
        font-size: 0.8rem;
        color: #6c757d;
    }

    .dashboard-tables {
        display: grid;
        grid-template-columns: 1fr;
        gap: 1.5rem;
    }

    .recent-activity {
        background-color: white;
        border-radius: 8px;
        box-shadow: 0 2px 10px rgba(0, 0, 0, 0.05);
        padding: 1.5rem;
    }

    .recent-activity h3 {
        color: var(--primary-color);
        margin-bottom: 1rem;
        display: flex;
        align-items: center;
        gap: 0.5rem;
    }

    table {
        width: 100%;
        border-collapse: collapse;
    }

    table th, table td {
        padding: 0.75rem;
        text-align: left;
        border-bottom: 1px solid var(--border-color);
    }

    table th {
        font-weight: 600;
        color: var(--primary-color);
    }

    .status-complete {
        background-color: rgba(40, 167, 69, 0.1);
        color: var(--success-color);
        padding: 0.25rem 0.5rem;
        border-radius: 4px;
        font-size: 0.8rem;
    }

    .status-pending {
        background-color: rgba(255, 193, 7, 0.1);
        color: var(--warning-color);
        padding: 0.25rem 0.5rem;
        border-radius: 4px;
        font-size: 0.8rem;
    }

    /* Footer Styles */
    .footer {
        background-color: var(--primary-color);
        color: #ddd;
        padding: 1.5rem 2rem;
        margin-top: auto;
    }

    .footer-content {
        display: flex;
        justify-content: space-between;
        align-items: center;
        max-width: 1200px;
        margin: 0 auto;
        flex-wrap: wrap;
        gap: 1rem;
    }

    .footer-section {
        font-size: 0.9rem;
    }

    .footer-section.links a {
        color: #ddd;
        margin: 0 0.25rem;
    }

    .footer-section.links a:hover {
        color: white;
    }

    /* Container Styles */
    .container {
        display: flex;
        flex-wrap: wrap;
        gap: 20px; /* Space between columns */
        margin-bottom: 20px; /* Space between sections */
        color: var(--primary-color); /* Text color */
        background-color: white; /* White background */
        border-radius: 15px; /* Rounded corners */
        padding: 20px; /* Inner spacing */
        width: 90%; /* Increase width to 90% of its parent */
        max-width: 1200px; /* Maximum width for larger screens */
        margin-left: auto; /* Center the container */
        margin-right: auto; /* Center the container */
        box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1); /* Optional: Add a subtle shadow */

    }

    .filter-group {
        margin-bottom: 15px;
    }

    .section {
        margin-bottom: 20px; /* Adds space between each section */
    }

    label {
        display: block; /* Makes the label take up the full width, forcing the select to go to the next line */
        margin-bottom: 5px; /* Adds a small space between the label and the dropdown */
    }

    select {
            width: 100%; /* Makes the dropdown take up the full width of its container */
            padding: 5px; /* Adds some padding inside the dropdown */
    }

    /* Basic reset of search clients */

    form {
        margin-bottom: 20px;
    }

    label {
        display: block;
        margin-bottom: 5px;
        font-weight: bold;
    }

    input[type="number"], select, input[type="radio"] {
        margin-bottom: 10px;
    }

    input[type="number"], select {
        width: 100%;
        padding: 10px;
        border: 1px solid #ddd;
        border-radius: 4px;
    }

    .radio-group {
        margin-bottom: 15px;
    }

    .radio-label {
        display: inline-block;
        margin-right: 15px;
        font-weight: normal;
    }

    .search-section {
        margin-bottom: 15px;
        padding: 15px;
        border: 1px solid #eee;
        border-radius: 5px;
        background-color: #f9f9f9;
        width: 80%; /* Adjust as needed */
        max-width: 1200px; /* Optional */
        margin: 0 auto; /* Center the section */
        box-sizing: border-box;
    }

    .search-section-title {
        font-weight: bold;
        margin-bottom: 10px;
        color: #2c3e50;
    }
    table {
        width: 100%;
        border-collapse: collapse;
        margin-top: 20px;
    }

    .hidden {
        display: none;
    }

    /* Section Title Styles */
    .section-title {
        margin: 0; /* Remove default margin */
        font-size: 15px; /* Increase font size */
        color: var(--primary-color); /* Use primary color for the title */
        width: 100%; /* Increase width to 90% of its parent */
    }

    .col {
        flex: 1; /* Each column takes equal space */
        width: 1550px; /* Minimum width for responsiveness */
    }

    /* Form Group Styles */
    .form-group {
        margin-bottom: 15px;
    }

    .form-group label {
        display: block;
        margin-bottom: 5px;
        font-weight: bold;
    }

    .form-group input {
        width: 100%;
        padding: 8px;
        box-sizing: border-box;
        border: 1px solid #ccc;
        border-radius: 4px;
    }

    /* Responsive adjustments */
    @media (max-width: 768px) {
        .header {
            flex-direction: column;
            text-align: center;
            padding: 1rem;
        }

        .header-right {
            margin-top: 1rem;
            justify-content: center;
        }

        .main-nav ul {
            flex-direction: column;
        }

        .dashboard-stats {
            grid-template-columns: 1fr;
        }

        .footer-content {
            flex-direction: column;
            text-align: center;
        }
    } 
    """
    #codice HTML
    search_client_template = f"""
            <!DOCTYPE html>
            <html lang="en">
            <head>
                <meta charset="UTF-8">
                <meta name="viewport" content="width=device-width, initial-scale=1.0">
                <title>Excellent Bank Admin - Search Clients</title>
                <style> {css} </style>
                    <script>
                        function toggleAgeFields() {{
                            const singleAgeOption = document.getElementById('age-single');
                            const rangeAgeOption = document.getElementById('age-range');
                            const singleAgeField = document.getElementById('single-age-field');
                            const rangeAgeField = document.getElementById('range-age-field');

                            if (singleAgeOption.checked) {{
                                singleAgeField.classList.remove('hidden');
                                rangeAgeField.classList.add('hidden');
                                document.getElementById('age_range').value = "";
                            }} else if (rangeAgeOption.checked) {{
                                singleAgeField.classList.add('hidden');
                                rangeAgeField.classList.remove('hidden');
                                document.getElementById('age').value = "";
                            }}
                        }}
                    </script>
                <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0-beta3/css/all.min.css">
            </head>
            <body>
                <!-- Header -->
                <header class="header">
                    <div class="logo-container">
                        <i class="fas fa-university logo-icon"></i>
                        <h1>Excellent Bank</h1>
                    </div>
                    <div class="header-right">
                        <span class="user-info">
                            <i class="fas fa-user-circle"></i> {{ username }} ({{ role }})
                        </span>
                        <span class="system-time" id="current-time"></span>
                        <a href="{{ url_for('logout') }}" class="logout-btn"><i class="fas fa-sign-out-alt"></i> Logout</a>
                    </div>
                </header>

                <!-- Navigation -->
                <nav class="main-nav">
                    <ul>
                        <li><a href="/dashboard"><i class="fas fa-tachometer-alt"></i> Dashboard</a></li>
                        <li><a href="/add_client"><i class="fas fa-user-plus"></i> Add Client</a></li>
                        <li><a href="/delete_client"><i class="fas fa-user-minus"></i> Delete Client</a></li>
                        <li class="active"><a href="/search_client"><i class="fas fa-users"></i> Search Clients</a></li>
                        <li><a href="/prediction_form"><i class="fas fa-chart-line"></i> Prediction Report</a></li>
                    </ul>
                </nav>

                <!-- Main Content -->
            <main class="main-content dashboard">
                <h2>Bank Data Search Engine</h2>
                <form action="/result_search_client" method="get">
                    <!-- Age Selection Section -->
                    <div class="container">
                            <div class="search-section" style="width: 2000px;">
                                <div class="search-section-title">Age Selection</div>

                                <div class="radio-group">
                                    <input type="radio" id="age-single" name="age_type" value="single" checked onclick="toggleAgeFields()">
                                    <label for="age-single" class="radio-label">Single Age</label>

                                    <input type="radio" id="age-range" name="age_type" value="range" onclick="toggleAgeFields()">
                                    <label for="age-range" class="radio-label">Age Range</label>
                                </div>

                                <div id="single-age-field">
                                    <label for="age">Specific Age:</label>
                                    <input type="number" id="age" name="age" placeholder="Enter age">
                                </div>

                                <div id="range-age-field" class="hidden">
                                    <label for="age_range">Age Range:</label>
                                    <select id="age_range" name="age_range">
                                        <option value="">Select age range</option>
                                        {"".join(f'<option value="{range}">{range}</option>' for range in age_ranges)}
                                    </select>
                                </div>
                            </div>

                            <div class="search-section" style="width: 2000px;">
                                <div class="search-section-title">Other Filters</div>
                                <label for="job">Job:</label>
                                <select id="job" name="job">
                                    <option value="">Select a job</option>
                                    {"".join(f'<option value="{job}">{job}</option>' for job in job_options)}
                                </select>

                                <label for="marital">Marital Status:</label>
                                <select id="marital" name="marital">
                                    <option value="">Select marital status</option>
                                    {"".join(f'<option value="{marital}">{marital}</option>' for marital in marital_options)}
                                </select>

                                <label for="education">Education:</label>
                                <select id="education" name="education">
                                    <option value="">Select education</option>
                                    {"".join(f'<option value="{education}">{education}</option>' for education in education_options)}
                                </select>

                                <label for="loan">Loan:</label>
                                <select id="loan" name="loan">
                                    <option value="">Select loan</option>
                                    {"".join(f'<option value="{loan}">{loan}</option>' for loan in loan_options)}
                                </select>

                                <label for="housing">Housing:</label>
                                <select id="housing" name="housing">
                                    <option value="">Select housing</option>
                                    {"".join(f'<option value="{housing}">{housing}</option>' for housing in housing_options)}
                                </select>

                                <label for="month">Month:</label>
                                <select id="month" name="month">
                                    <option value="">Select month</option>
                                    {"".join(f'<option value="{month}">{month}</option>' for month in month_options)}
                                </select>
                            </div>
                    </div>

                    <!-- Submit Button -->
                    <div class="container">
                        <div class="col">
                            <button type="submit" class="btn btn-primary">View Results</button>
                        </div>
                    </div>
                </form>
            </main>
            <div class="search-results" id="searchResults" style="display: none;">
                <div class="container">
                    <h2>Search Results</h2>
                    <div class="graph-container">
                        <div class="graph">
                            <img src="data:image/png;base64,{graph_url}" alt="Client Balances and Deposit Distribution">
                        </div>
                    </div>
                    <div class="statement" style="white-space: pre-line;">
                        {statement}
                    </div>

                    <div id="tableContainer">
                        <div class="row-count">Showing <span id="visibleRows">10</span> of {total_rows} records</div>
                        {data_html}

                        <button id="showMoreBtn" class="show-more-btn">Show More</button>
                    </div>
                </div>
            </div>
                <!-- Footer -->
                <footer class="footer">
                    <div class="footer-content">
                        <div class="footer-section">
                            <p>&copy; 2025 Excellent Bank Administration System. All rights reserved.</p>
                        </div>
                        <div class="footer-section">
                            <p><i class="fas fa-shield-alt"></i> Protected by enterprise-grade security</p>
                        </div>
                        <div class="footer-section links">
                            <a href="#">Privacy Policy</a> | 
                            <a href="#">Terms of Service</a> | 
                            <a href="#">Contact IT Support</a>
                        </div>
                    </div>
                </footer>
            </body>
            </html>
            """

    return render_template_string(search_client_template,
                                  css=css,
                                  username=session['username'],
                                  role=session['role'],
                                  age_ranges=age_ranges,
                                  job_options=job_options,
                                  marital_options=marital_options,
                                  education_options=education_options,
                                  loan_options=loan_options,
                                  housing_options=housing_options,
                                  month_options=month_options,
                                  graph_url=graph_url,
                                  statement=statement,
                                  total_rows=total_rows,
                                  data_html=data_html
                                  )

@app.route('/result_search_client', methods = ["GET"])
@login_required
def result_search_client():
    # Get filter parameters from the URL query string
    age_type = request.args.get('age_type', 'single')
    age = request.args.get('age')
    age_range = request.args.get('age_range')
    job = request.args.get('job')
    marital = request.args.get('marital')
    education = request.args.get('education')
    loan = request.args.get('loan')
    housing = request.args.get('housing')
    month = request.args.get('month')

    print("Parametri estratti dalla URL:", {
        "age_type": age_type,
        "age": age,
        "age_range": age_range,
        "job": job,
        "marital": marital,
        "education": education,
        "loan": loan,
        "housing": housing,
        "month": month
    })

    try:
        # Connessione al database
        conn = mysql.connector.connect(
            host="localhost",
            user="root",
            password="",
            database="bank_marketing"
        )
        cursor = conn.cursor(dictionary=True)  # Restituisce i risultati come dizionari

        # Costruzione della query SQL
        # Costruzione della query SQL
        query = """
                SELECT c.age, j.nome as job, c.marital, c.education, 
                       w.personal_loan as loan, w.housing_loan as housing, h.month,
                       d.term_deposit, w.balance, h.duration
                FROM client c
                JOIN jobs j ON c.job_id = j.id_job
                JOIN wallet w ON c.wallet_id = w.id_wallet
                JOIN contact_history h ON c.history_id = h.id_history
                JOIN deposit d ON c.deposit_id = d.id_deposit
                WHERE 1=1
                """
        params = []

        # Applicazione dei filtri
        if age_type == 'single' and age:
            query += " AND c.age = %s"
            params.append(int(age))
        elif age_type == 'range' and age_range:
            if age_range == '90+':
                min_age = 90
                max_age = 150  # Età massima assunta 150
            else:
                min_age, max_age = map(int, age_range.split('-'))
            query += " AND c.age >= %s AND c.age < %s"
            params.extend([min_age, max_age])

        if job:
            query += " AND j.nome = %s"
            params.append(job)
        if marital:
            query += " AND c.marital = %s"
            params.append(marital)
        if education:
            query += " AND c.education = %s"
            params.append(education)
        if loan:
            query += " AND w.personal_loan = %s"
            params.append(loan)
        if housing:
            query += " AND w.housing_loan = %s"
            params.append(housing)
        if month:
            query += " AND h.month = %s"
            params.append(month)

        # Esecuzione della query
        cursor.execute(query, params)
        results = cursor.fetchall()

        # Verifica se i risultati sono vuoti
        if not results:
            return "Nessun dato trovato che corrisponda ai tuoi criteri."

        # Converti i risultati in un DataFrame di pandas per la generazione dei grafici
        filtered_data = pd.DataFrame(results)

        # Rinomina la colonna term_deposit in deposit per compatibilità con generate_graphs()
        filtered_data.rename(columns={'term_deposit': 'deposit'}, inplace=True)

        # Assicurati che il campo deposit sia numerico
        if 'deposit' in filtered_data.columns:
            filtered_data['deposit'] = filtered_data['deposit'].astype(int)

        # Genera i grafici in base al tipo di età
        try:
            graph_url = generate_graphs(filtered_data, age_type)
        except Exception as e:
            import traceback
            traceback_str = traceback.format_exc()
            return f"Si è verificato un errore durante la generazione dei grafici: {str(e)}\nTraceback: {traceback_str}"

        # Genera la dichiarazione
        statement = generate_statement(filtered_data, age, age_range, job, marital, education, loan, housing, month)

        # Converti i dati filtrati in una tabella HTML
        data_html = filtered_data.to_html(classes='data', index=False)

        # Ottieni il numero totale di righe
        total_rows = len(filtered_data)

        # Chiusura della connessione
        cursor.close()
        conn.close()

    except Error as e:
        import traceback
        traceback_str = traceback.format_exc()
        return f"Errore durante l'accesso al database: {str(e)}\nTraceback: {traceback_str}"

    css = """
        /* Global Styles */
        :root {
            --primary-color: #1a3b5d;
            --secondary-color: #2d6187;
            --accent-color: #e4a013;
            --text-color: #333;
            --light-text: #f8f9fa;
            --border-color: #dee2e6;
            --success-color: #28a745;
            --danger-color: #dc3545;
            --warning-color: #ffc107;
            --info-color: #17a2b8;
        }

        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }

        body {
            font-family: Helvetica, sans-serif;
            line-height: 1.6;
            color: var(--text-color);
            background-color: #f5f7fa;
            min-height: 100vh;
            display: flex;
            flex-direction: column;
        }

        a {
            text-decoration: none;
            color: var(--secondary-color);
        }

        a:hover {
            color: var(--primary-color);
        }

        /* Header Styles */
        .header {
            background-color: var(--primary-color);
            color: white;
            padding: 1rem 2rem;
            display: flex;
            justify-content: space-between;
            align-items: center;
            box-shadow: 0 2px 5px rgba(0, 0, 0, 0.1);
        }

        .logo-container {
            display: flex;
            align-items: center;
        }

        .logo-icon {
            font-size: 2rem;
            margin-right: 10px;
            color: var(--accent-color);
        }

        .header h1 {
            font-size: 1.5rem;
            font-weight: 600;
        }

        .header-right {
            display: flex;
            align-items: center;
            gap: 1.5rem;
        }

        .system-time {
            font-size: 0.9rem;
            color: #ddd;
        }

        .user-info {
            display: flex;
            align-items: center;
            gap: 0.5rem;
            font-size: 0.9rem;
        }

        .logout-btn {
            background-color: rgba(255, 255, 255, 0.1);
            color: white;
            padding: 0.5rem 1rem;
            border-radius: 4px;
            font-size: 0.9rem;
            transition: background-color 0.3s;
        }

        .logout-btn:hover {
            background-color: rgba(255, 255, 255, 0.2);
            color: white;
        }

        /* Main Content */
        .main-content {
            flex: 1;
            padding: 2rem;
            max-width: 1200px;
            margin: 0 auto;
            width: 100%;
        }

        .login-container {
            display: flex;
            justify-content: center;
            align-items: center;
            min-height: calc(100vh - 140px);
        }

        .login-card {
            background-color: white;
            border-radius: 8px;
            box-shadow: 0 4px 15px rgba(0, 0, 0, 0.1);
            width: 100%;
            max-width: 450px;
            padding: 2rem;
        }

        .login-header {
            text-align: center;
            margin-bottom: 2rem;
        }

        .login-header h2 {
            color: var(--primary-color);
            margin-bottom: 0.5rem;
        }

        .login-header p {
            color: #6c757d;
            font-size: 0.9rem;
        }

        .login-form .form-group {
            margin-bottom: 1.5rem;
        }

        .login-form label {
            display: block;
            margin-bottom: 0.5rem;
            font-weight: 500;
            color: var(--primary-color);
        }

        .login-form input {
            width: 100%;
            padding: 0.75rem;
            border: 1px solid var(--border-color);
            border-radius: 4px;
            font-size: 1rem;
            transition: border-color 0.3s;
        }

        .login-form input:focus {
            border-color: var(--secondary-color);
            outline: none;
        }

        .form-actions {
            margin-top: 2rem;
        }

        .btn {
            display: inline-block;
            padding: 0.75rem 1.5rem;
            border-radius: 4px;
            font-weight: 500;
            cursor: pointer;
            border: none;
            transition: all 0.3s;
        }

        .btn-primary {
            background-color: var(--primary-color);
            color: white;
            width: 100%;
            font-size: 1rem;
        }

        .btn-primary:hover {
            background-color: var(--secondary-color);
        }

        .btn-danger {
            background-color: var(--danger-color);
            color: white;
            width: 100%;
            font-size: 1rem;
            border-radius: 4px;
            display: inline-block;
        }

        .btn-danger:hover {
            background-color: #c82333;
        }

        .form-footer {
            text-align: center;
            margin-top: 1.5rem;
            font-size: 0.9rem;
        }

        .forgot-password {
            color: var(--secondary-color);
        }

        /* Alerts */
        .alert {
            padding: 1rem;
            border-radius: 4px;
            margin-bottom: 1.5rem;
            font-size: 0.9rem;
        }

        .alert-danger {
            background-color: #f8d7da;
            color: #721c24;
            border: 1px solid #f5c6cb;
        }

        .alert-success {
            background-color: #d4edda;
            color: #155724;
            border: 1px solid #c3e6cb;
        }

        .alert-info {
            background-color: #d1ecf1;
            color: #0c5460;
            border: 1px solid #bee5eb;
        }

        /* Navigation */
        .main-nav {
            background-color: white;
            box-shadow: 0 2px 5px rgba(0, 0, 0, 0.05);
        }

        .main-nav ul {
            list-style: none;
            display: flex;
            max-width: 1200px;
            margin: 0 auto;
            padding: 0 2rem;
        }

        .main-nav li {
            position: relative;
        }

        .main-nav a {
            display: block;
            padding: 1rem 1.5rem;
            color: var(--text-color);
            font-weight: 500;
            transition: all 0.3s;
        }

        .main-nav a i {
            margin-right: 0.5rem;
        }

        .main-nav a:hover {
            background-color: #f8f9fa;
            color: var(--primary-color);
        }

        .main-nav .active a {
            color: var(--primary-color);
            border-bottom: 3px solid var(--primary-color);
        }

        /* Dashboard Styles */
        .dashboard h2 {
            color: var(--primary-color);
            margin-bottom: 1.5rem;
        }

        .dashboard-stats {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(240px, 1fr));
            gap: 1.5rem;
            margin-bottom: 2rem;
        }

        .stat-card {
            background-color: white;
            border-radius: 8px;
            box-shadow: 0 2px 10px rgba(0, 0, 0, 0.05);
            padding: 1.5rem;
            display: flex;
            align-items: center;
        }

        .stat-icon {
            background-color: rgba(26, 59, 93, 0.1);
            color: var(--primary-color);
            width: 50px;
            height: 50px;
            border-radius: 50%;
            display: flex;
            justify-content: center;
            align-items: center;
            font-size: 1.5rem;
            margin-right: 1rem;
        }

        .stat-content h3 {
            font-size: 0.9rem;
            color: #6c757d;
            margin-bottom: 0.3rem;
        }

        .stat-number {
            font-size: 1.5rem;
            font-weight: 600;
            color: var(--primary-color);
        }

        .stat-period {
            font-size: 0.8rem;
            color: #6c757d;
        }

        .dashboard-tables {
            display: grid;
            grid-template-columns: 1fr;
            gap: 1.5rem;
        }

        .recent-activity {
            background-color: white;
            border-radius: 8px;
            box-shadow: 0 2px 10px rgba(0, 0, 0, 0.05);
            padding: 1.5rem;
        }

        .recent-activity h3 {
            color: var(--primary-color);
            margin-bottom: 1rem;
            display: flex;
            align-items: center;
            gap: 0.5rem;
        }

        table {
            width: 100%;
            border-collapse: collapse;
        }

        table th, table td {
            padding: 0.75rem;
            text-align: left;
            border-bottom: 1px solid var(--border-color);
        }

        table th {
            font-weight: 600;
            color: var(--primary-color);
        }

        .status-complete {
            background-color: rgba(40, 167, 69, 0.1);
            color: var(--success-color);
            padding: 0.25rem 0.5rem;
            border-radius: 4px;
            font-size: 0.8rem;
        }

        .status-pending {
            background-color: rgba(255, 193, 7, 0.1);
            color: var(--warning-color);
            padding: 0.25rem 0.5rem;
            border-radius: 4px;
            font-size: 0.8rem;
        }

        /* Footer Styles */
        .footer {
            background-color: var(--primary-color);
            color: #ddd;
            padding: 1.5rem 2rem;
            margin-top: auto;
        }

        .footer-content {
            display: flex;
            justify-content: space-between;
            align-items: center;
            max-width: 1200px;
            margin: 0 auto;
            flex-wrap: wrap;
            gap: 1rem;
        }

        .footer-section {
            font-size: 0.9rem;
        }

        .footer-section.links a {
            color: #ddd;
            margin: 0 0.25rem;
        }

        .footer-section.links a:hover {
            color: white;
        }

        /* Container Styles */
        .container {
            display: flex;
            flex-wrap: wrap;
            gap: 20px; /* Space between columns */
            margin-bottom: 20px; /* Space between sections */
            color: var(--primary-color); /* Text color */
            background-color: white; /* White background */
            border-radius: 15px; /* Rounded corners */
            padding: 20px; /* Inner spacing */
            width: 90%; /* Increase width to 90% of its parent */
            max-width: 1200px; /* Maximum width for larger screens */
            margin-left: auto; /* Center the container */
            margin-right: auto; /* Center the container */
            box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1); /* Optional: Add a subtle shadow */

        }
        
        .container2 {
            display: flex;
            flex-wrap: wrap;
            gap: 20px; /* Space between columns */
            margin-bottom: 20px; /* Space between sections */
            color: var(--primary-color); /* Text color */
            background-color: white; /* White background */
            border-radius: 15px; /* Rounded corners */
            padding: 20px; /* Inner spacing */
            width: 100%; /* Increase width to 90% of its parent */
            max-width: 2000px; /* Maximum width for larger screens */
            margin-left: auto; /* Center the container */
            margin-right: auto; /* Center the container */
            box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1); /* Optional: Add a subtle shadow */

        }
        
        /* Search client results presentation */

.graph {
            margin-bottom: 20px;
            text-align: center;
        }

.graph-container {
            display: flex;
            justify-content: center;
            align-items: center;
            flex-direction: column;
            width: 100%;
        }


.statement {
            text-align: center;
            font-size: 1.2em;
            color: #2c3e50;
            margin-bottom: 40px;
            white-space: pre-line;
        }

/* Table styles */
        table {
            width: 100%;
            border-collapse: collapse;
            margin-top: 20px;
            align-items: center;
        }

        table, th, td {
            border: 1px solid #ddd;
        }

        th, td {
            padding: 10px;
            text-align: center;
        }

        th {
            background-color: #437DFA;
            color: #ffffff;
        }

        td {
            background-color: #f5f5f5;
            color: #000000;
        }

/* Pagination and row display */
        .hidden-row {
            display: none;
        }

        .show-more-btn {
            display: block;
            margin: 20px auto;
            padding: 10px 20px;
            background-color: #437DFA;
            color: white;
            border: none;
            border-radius: 5px;
            cursor: pointer;
            font-size: 16px;
        }

        .show-more-btn:hover {
            background-color: #3269e2;
        }

        .row-count {
            text-align: center;
            margin: 10px 0;
            color: #666;
        }

        .filter-group {
            margin-bottom: 15px;
        }

        .section {
            margin-bottom: 20px; /* Adds space between each section */
        }

        label {
            display: block; /* Makes the label take up the full width, forcing the select to go to the next line */
            margin-bottom: 5px; /* Adds a small space between the label and the dropdown */
        }

        select {
                width: 100%; /* Makes the dropdown take up the full width of its container */
                padding: 5px; /* Adds some padding inside the dropdown */
        }

        /* Basic reset of search clients */

        form {
            margin-bottom: 20px;
        }

        label {
            display: block;
            margin-bottom: 5px;
            font-weight: bold;
        }

        input[type="number"], select, input[type="radio"] {
            margin-bottom: 10px;
        }

        input[type="number"], select {
            width: 100%;
            padding: 10px;
            border: 1px solid #ddd;
            border-radius: 4px;
        }

        .radio-group {
            margin-bottom: 15px;
        }

        .radio-label {
            display: inline-block;
            margin-right: 15px;
            font-weight: normal;
        }

        .search-section {
            margin-bottom: 20px;
            padding: 15px;
            border: 1px solid #eee;
            border-radius: 5px;
            background-color: #f9f9f9;
        }

        .search-section-title {
            font-weight: bold;
            margin-bottom: 10px;
            color: #2c3e50;
        }
        table {
            width: 100%;
            border-collapse: collapse;
            margin-top: 20px;
        }


        .hidden {
            display: none;
        }

        /* Section Title Styles */
        .section-title {
            margin: 0; /* Remove default margin */
            font-size: 15px; /* Increase font size */
            color: var(--primary-color); /* Use primary color for the title */
            width: 100%; /* Increase width to 90% of its parent */
        }

        .col {
            flex: 1; /* Each column takes equal space */
            min-width: 50px; /* Minimum width for responsiveness */
        }

        /* Form Group Styles */
        .form-group {
            margin-bottom: 15px;
        }

        .form-group label {
            display: block;
            margin-bottom: 5px;
            font-weight: bold;
        }

        .form-group input {
            width: 100%;
            padding: 8px;
            box-sizing: border-box;
            border: 1px solid #ccc;
            border-radius: 4px;
        }

        /* Responsive adjustments */
        @media (max-width: 768px) {
            .header {
                flex-direction: column;
                text-align: center;
                padding: 1rem;
            }

            .header-right {
                margin-top: 1rem;
                justify-content: center;
            }

            .main-nav ul {
                flex-direction: column;
            }

            .dashboard-stats {
                grid-template-columns: 1fr;
            }

            .footer-content {
                flex-direction: column;
                text-align: center;
            }
        }
        """
    # HTML and CSS for the search results page
    result_search_client_template = f"""
        <!DOCTYPE html>
        <html lang="en">
        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <title>Search Results</title>
            <style> { css } </style>
            <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0-beta3/css/all.min.css">
        </head>
        <body>
            <!-- Header -->
            <header class="header">
                <div class="logo-container">
                    <i class="fas fa-university logo-icon"></i>
                    <h1>Excellent Bank</h1>
                </div>
                <div class="header-right">
                    <span class="user-info">
                        <i class="fas fa-user-circle"></i> {{ username }} ({{ role }})
                    </span>
                    <span class="system-time" id="current-time"></span>
                    <a href="{{ url_for('logout') }}" class="logout-btn"><i class="fas fa-sign-out-alt"></i> Logout</a>
                </div>
            </header>
        
            <!-- Navigation -->
            <nav class="main-nav">
                <ul>
                    <li><a href="{{ url_for('dashboard') }}"><i class="fas fa-tachometer-alt"></i> Dashboard</a></li>
                    <li><a href="{{ url_for('add_client') }}"><i class="fas fa-user-plus"></i> Add Client</a></li>
                    <li><a href="{{ url_for('delete_client') }}"><i class="fas fa-user-minus"></i> Delete Client</a></li>
                    <li class="active"><a href="{{ url_for('search_client') }}"><i class="fas fa-users"></i> Search Clients</a></li>
                    <li><a href="{{ url_for('prediction_form') }}"><i class="fas fa-chart-line"></i> Prediction Report</a></li>
                </ul>
            </nav>
        
            <!-- Main Content -->
            <main class="main-content dashboard">
                <h2>Search Results</h2>
                <div class="container2">
                    <div class="graph-container">
                        <div class="graph">
                            <img src="data:image/png;base64,{graph_url}" alt="Client Balances and Deposit Distribution">
                        </div>
                    </div>
                    <div class="statement" style="white-space: pre-line;">
                        {statement}
                    </div>
            
                    <div id="tableContainer">
                        <div class="row-count">Showing <span id="visibleRows">10</span> of {total_rows} records</div>
                        {data_html}
                        <button id="showMoreBtn" class="show-more-btn">Show More</button>
                    </div>
                    <a href="/search_client" class="btn btn-primary">Back to Search</a>
                </div>
            </main>
        
            <!-- Footer -->
            <footer class="footer">
                <div class="footer-content">
                    <div class="footer-section">
                        <p>&copy; 2025 Excellent Bank Administration System. All rights reserved.</p>
                    </div>
                    <div class="footer-section">
                        <p><i class="fas fa-shield-alt"></i> Protected by enterprise-grade security</p>
                    </div>
                    <div class="footer-section links">
                        <a href="#">Privacy Policy</a> | 
                        <a href="#">Terms of Service</a> | 
                        <a href="#">Contact IT Support</a>
                    </div>
                </div>
            </footer>
        
            <script>
                document.addEventListener('DOMContentLoaded', function() {{
                    // Nascondi tutte le righe dopo la decima all'inizio
                    const table = document.querySelector('.data');
                    const rows = table.querySelectorAll('tbody tr');
                    const totalRows = rows.length;
                    const showMoreBtn = document.getElementById('showMoreBtn');
                    const visibleRowsCounter = document.getElementById('visibleRows');
        
                    let visibleRows = 10;
        
                    // Se ci sono meno di 10 righe, nascondi il pulsante
                    if (totalRows <= 10) {{
                        showMoreBtn.style.display = 'none';
                        visibleRowsCounter.textContent = totalRows;
                    }}
        
                    // Nascondi le righe oltre la decima
                    for (let i = 10; i < rows.length; i++) {{
                        rows[i].classList.add('hidden-row');
                    }}
        
                    // Aggiungi event listener al pulsante Show More
                    showMoreBtn.addEventListener('click', function() {{
                        // Mostra altre 10 righe
                        for (let i = visibleRows; i < Math.min(visibleRows + 10, totalRows); i++) {{
                            rows[i].classList.remove('hidden-row');
                        }}
        
                        // Aggiorna il contatore delle righe visibili
                        visibleRows = Math.min(visibleRows + 10, totalRows);
                        visibleRowsCounter.textContent = visibleRows;
        
                        // Nascondi il pulsante se tutte le righe sono visibili
                        if (visibleRows >= totalRows) {{
                            showMoreBtn.style.display = 'none';
                        }}
                    }});
                }});
            </script>
        </body>
        </html>
        """
    return render_template_string(result_search_client_template, css=css,
                                  username=session['username'],
                                  role=session['role'],
                                  graph_url=graph_url,
                                  statement=statement,
                                  total_rows=total_rows,
                                  data_html=data_html)

# THE ABILITY TO CREATE A REPORT BASED ON THE CLIENT PREDICTION
@app.route('/prediction_form', methods=['GET', 'POST'])
@login_required
def prediction_form():
    # Get unique values for job, marital status, education, etc.
    job_options = df['job'].unique().tolist()
    marital_options = df['marital'].unique().tolist()
    education_options = df['education'].unique().tolist()
    loan_options = df['loan'].unique().tolist()
    housing_options = df['housing'].unique().tolist()
    month_options = df['month'].unique().tolist()

    # CSS styles as a string variable
    css = """
    /* Global Styles */
    :root {
        --primary-color: #1a3b5d;
        --secondary-color: #2d6187;
        --accent-color: #e4a013;
        --text-color: #333;
        --light-text: #f8f9fa;
        --border-color: #dee2e6;
        --success-color: #28a745;
        --danger-color: #dc3545;
        --warning-color: #ffc107;
        --info-color: #17a2b8;
    }

    * {
        margin: 0;
        padding: 0;
        box-sizing: border-box;
    }

    body {
        font-family: Helvetica, sans-serif;
        line-height: 1.6;
        color: var(--text-color);
        background-color: #f5f7fa;
        min-height: 100vh;
        display: flex;
        flex-direction: column;
    }

    a {
        text-decoration: none;
        color: var(--secondary-color);
    }

    a:hover {
        color: var(--primary-color);
    }

    /* Header Styles */
    .header {
        background-color: var(--primary-color);
        color: white;
        padding: 1rem 2rem;
        display: flex;
        justify-content: space-between;
        align-items: center;
        box-shadow: 0 2px 5px rgba(0, 0, 0, 0.1);
    }

    .logo-container {
        display: flex;
        align-items: center;
    }

    .logo-icon {
        font-size: 2rem;
        margin-right: 10px;
        color: var(--accent-color);
    }

    .header h1 {
        font-size: 1.5rem;
        font-weight: 600;
    }

    .header-right {
        display: flex;
        align-items: center;
        gap: 1.5rem;
    }

    .system-time {
        font-size: 0.9rem;
        color: #ddd;
    }

    .user-info {
        display: flex;
        align-items: center;
        gap: 0.5rem;
        font-size: 0.9rem;
    }

    .logout-btn {
        background-color: rgba(255, 255, 255, 0.1);
        color: white;
        padding: 0.5rem 1rem;
        border-radius: 4px;
        font-size: 0.9rem;
        transition: background-color 0.3s;
    }

    .logout-btn:hover {
        background-color: rgba(255, 255, 255, 0.2);
        color: white;
    }

    /* Main Content */
    .main-content {
        flex: 1;
        padding: 2rem;
        max-width: 1200px;
        margin: 0 auto;
        width: 100%;
    }

    .login-container {
        display: flex;
        justify-content: center;
        align-items: center;
        min-height: calc(100vh - 140px);
    }

    .login-card {
        background-color: white;
        border-radius: 8px;
        box-shadow: 0 4px 15px rgba(0, 0, 0, 0.1);
        width: 100%;
        max-width: 450px;
        padding: 2rem;
    }

    .login-header {
        text-align: center;
        margin-bottom: 2rem;
    }

    .login-header h2 {
        color: var(--primary-color);
        margin-bottom: 0.5rem;
    }

    .login-header p {
        color: #6c757d;
        font-size: 0.9rem;
    }

    .login-form .form-group {
        margin-bottom: 1.5rem;
    }

    .login-form label {
        display: block;
        margin-bottom: 0.5rem;
        font-weight: 500;
        color: var(--primary-color);
    }

    .login-form input {
        width: 100%;
        padding: 0.75rem;
        border: 1px solid var(--border-color);
        border-radius: 4px;
        font-size: 1rem;
        transition: border-color 0.3s;
    }

    .login-form input:focus {
        border-color: var(--secondary-color);
        outline: none;
    }

    .form-actions {
        margin-top: 2rem;
    }

    .btn {
        display: inline-block;
        padding: 0.75rem 1.5rem;
        border-radius: 4px;
        font-weight: 500;
        cursor: pointer;
        border: none;
        transition: all 0.3s;
    }

    .btn-primary {
        background-color: var(--primary-color);
        color: white;
        width: 100%;
        font-size: 1rem;
    }

    .btn-primary:hover {
        background-color: var(--secondary-color);
    }

    .btn-danger {
        background-color: var(--danger-color);
        color: white;
        width: 100%;
        font-size: 1rem;
        border-radius: 4px;
        display: inline-block;
    }

    .btn-danger:hover {
        background-color: #c82333;
    }

    .form-footer {
        text-align: center;
        margin-top: 1.5rem;
        font-size: 0.9rem;
    }

    .forgot-password {
        color: var(--secondary-color);
    }

    /* Alerts */
    .alert {
        padding: 1rem;
        border-radius: 4px;
        margin-bottom: 1.5rem;
        font-size: 0.9rem;
    }

    .alert-danger {
        background-color: #f8d7da;
        color: #721c24;
        border: 1px solid #f5c6cb;
    }

    .alert-success {
        background-color: #d4edda;
        color: #155724;
        border: 1px solid #c3e6cb;
    }

    .alert-info {
        background-color: #d1ecf1;
        color: #0c5460;
        border: 1px solid #bee5eb;
    }

    /* Navigation */
    .main-nav {
        background-color: white;
        box-shadow: 0 2px 5px rgba(0, 0, 0, 0.05);
    }

    .main-nav ul {
        list-style: none;
        display: flex;
        max-width: 1200px;
        margin: 0 auto;
        padding: 0 2rem;
    }

    .main-nav li {
        position: relative;
    }

    .main-nav a {
        display: block;
        padding: 1rem 1.5rem;
        color: var(--text-color);
        font-weight: 500;
        transition: all 0.3s;
    }

    .main-nav a i {
        margin-right: 0.5rem;
    }

    .main-nav a:hover {
        background-color: #f8f9fa;
        color: var(--primary-color);
    }

    .main-nav .active a {
        color: var(--primary-color);
        border-bottom: 3px solid var(--primary-color);
    }

    /* Dashboard Styles */
    .dashboard h2 {
        color: var(--primary-color);
        margin-bottom: 1.5rem;
    }

    .dashboard-stats {
        display: grid;
        grid-template-columns: repeat(auto-fit, minmax(240px, 1fr));
        gap: 1.5rem;
        margin-bottom: 2rem;
    }

    .stat-card {
        background-color: white;
        border-radius: 8px;
        box-shadow: 0 2px 10px rgba(0, 0, 0, 0.05);
        padding: 1.5rem;
        display: flex;
        align-items: center;
    }

    .stat-icon {
        background-color: rgba(26, 59, 93, 0.1);
        color: var(--primary-color);
        width: 50px;
        height: 50px;
        border-radius: 50%;
        display: flex;
        justify-content: center;
        align-items: center;
        font-size: 1.5rem;
        margin-right: 1rem;
    }

    .stat-content h3 {
        font-size: 0.9rem;
        color: #6c757d;
        margin-bottom: 0.3rem;
    }

    .stat-number {
        font-size: 1.5rem;
        font-weight: 600;
        color: var(--primary-color);
    }

    .stat-period {
        font-size: 0.8rem;
        color: #6c757d;
    }

    .dashboard-tables {
        display: grid;
        grid-template-columns: 1fr;
        gap: 1.5rem;
    }

    .recent-activity {
        background-color: white;
        border-radius: 8px;
        box-shadow: 0 2px 10px rgba(0, 0, 0, 0.05);
        padding: 1.5rem;
    }

    .recent-activity h3 {
        color: var(--primary-color);
        margin-bottom: 1rem;
        display: flex;
        align-items: center;
        gap: 0.5rem;
    }

    table {
        width: 100%;
        border-collapse: collapse;
    }

    table th, table td {
        padding: 0.75rem;
        text-align: left;
        border-bottom: 1px solid var(--border-color);
    }

    table th {
        font-weight: 600;
        color: var(--primary-color);
    }

    .status-complete {
        background-color: rgba(40, 167, 69, 0.1);
        color: var(--success-color);
        padding: 0.25rem 0.5rem;
        border-radius: 4px;
        font-size: 0.8rem;
    }

    .status-pending {
        background-color: rgba(255, 193, 7, 0.1);
        color: var(--warning-color);
        padding: 0.25rem 0.5rem;
        border-radius: 4px;
        font-size: 0.8rem;
    }

    /* Footer Styles */
    .footer {
        background-color: var(--primary-color);
        color: #ddd;
        padding: 1.5rem 2rem;
        margin-top: auto;
    }

    .footer-content {
        display: flex;
        justify-content: space-between;
        align-items: center;
        max-width: 1200px;
        margin: 0 auto;
        flex-wrap: wrap;
        gap: 1rem;
    }

    .footer-section {
        font-size: 0.9rem;
    }

    .footer-section.links a {
        color: #ddd;
        margin: 0 0.25rem;
    }

    .footer-section.links a:hover {
        color: white;
    }

    /* Container Styles */
    .container {
        display: flex;
        flex-wrap: wrap;
        gap: 20px; /* Space between columns */
        margin-bottom: 20px; /* Space between sections */
        color: var(--primary-color); /* Text color */
        background-color: white; /* White background */
        border-radius: 15px; /* Rounded corners */
        padding: 20px; /* Inner spacing */
        width: 90%; /* Increase width to 90% of its parent */
        max-width: 1200px; /* Maximum width for larger screens */
        margin-left: auto; /* Center the container */
        margin-right: auto; /* Center the container */
        box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1); /* Optional: Add a subtle shadow */

    }

    .filter-group {
        margin-bottom: 15px;
    }

    .section {
        margin-bottom: 20px; /* Adds space between each section */
    }

    label {
        display: block; /* Makes the label take up the full width, forcing the select to go to the next line */
        margin-bottom: 5px; /* Adds a small space between the label and the dropdown */
    }

    select {
            width: 100%; /* Makes the dropdown take up the full width of its container */
            padding: 5px; /* Adds some padding inside the dropdown */
    }

    /* Basic reset of search clients */

    form {
        margin-bottom: 20px;
    }

    label {
        display: block;
        margin-bottom: 5px;
        font-weight: bold;
    }

    input[type="number"], select, input[type="radio"] {
        margin-bottom: 10px;
    }

    input[type="number"], select {
        width: 100%;
        padding: 10px;
        border: 1px solid #ddd;
        border-radius: 4px;
    }

    .radio-group {
        margin-bottom: 15px;
    }

    .radio-label {
        display: inline-block;
        margin-right: 15px;
        font-weight: normal;
    }

    .search-section {
        margin-bottom: 20px;
        padding: 15px;
        border: 1px solid #eee;
        border-radius: 5px;
        background-color: #f9f9f9;
    }

    .search-section-title {
        font-weight: bold;
        margin-bottom: 10px;
        color: #2c3e50;
    }
    table {
        width: 100%;
        border-collapse: collapse;
        margin-top: 20px;
    }


    .hidden {
        display: none;
    }

    /* Section Title Styles */
    .section-title {
        margin: 0; /* Remove default margin */
        font-size: 15px; /* Increase font size */
        color: var(--primary-color); /* Use primary color for the title */
        width: 100%; /* Increase width to 90% of its parent */
    }

    .col {
        flex: 1; /* Each column takes equal space */
        min-width: 50px; /* Minimum width for responsiveness */
    }

    /* Form Group Styles */
    .form-group {
        margin-bottom: 15px;
    }

    .form-group label {
        display: block;
        margin-bottom: 5px;
        font-weight: bold;
    }

    .form-group input {
        width: 100%;
        padding: 8px;
        box-sizing: border-box;
        border: 1px solid #ccc;
        border-radius: 4px;
    }

    /* Responsive adjustments */
    @media (max-width: 768px) {
        .header {
            flex-direction: column;
            text-align: center;
            padding: 1rem;
        }

        .header-right {
            margin-top: 1rem;
            justify-content: center;
        }

        .main-nav ul {
            flex-direction: column;
        }

        .dashboard-stats {
            grid-template-columns: 1fr;
        }

        .footer-content {
            flex-direction: column;
            text-align: center;
        }
    }
    """
    # HTML as a string variable
    predict_template = """
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Excellent Bank Admin - Deposit Prediction</title>
        <style>{{ css }}</style>
        <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0-beta3/css/all.min.css">
    </head>
    <body>
        <!-- Header -->
        <header class="header">
            <div class="logo-container">
                <i class="fas fa-university logo-icon"></i>
                <h1>Excellent Bank</h1>
            </div>
            <div class="header-right">
                <span class="user-info">
                    <i class="fas fa-user-circle"></i> {{ username }} ({{ role }})
                </span>
                <span class="system-time" id="current-time"></span>
                <a href="{{ url_for('logout') }}" class="logout-btn"><i class="fas fa-sign-out-alt"></i> Logout</a>
            </div>
        </header>

        <!-- Navigation -->
        <nav class="main-nav">
            <ul>
                <li><a href="{{ url_for('dashboard') }}"><i class="fas fa-tachometer-alt"></i> Dashboard</a></li>
                <li><a href="{{ url_for('add_client') }}"><i class="fas fa-user-plus"></i> Add Client</a></li>
                <li><a href="{{ url_for('delete_client') }}"><i class="fas fa-user-minus"></i> Delete Client</a></li>
                <li><a href="{{ url_for('search_client') }}"><i class="fas fa-users"></i> Search Clients</a></li>
                <li class="active"><a href="{{ url_for('prediction_form') }}"><i class="fas fa-chart-line"></i> Prediction Report</a></li>
            </ul>
        </nav>

        <!-- Main Content -->
        <main class="main-content dashboard">
            <h2>Deposit Prediction</h2>
            <div class="container">
                <form action="/predict" method="post">
                    <div class="form-group">
                        <label for="age">Age:</label>
                        <input type="number" id="age" name="age" required>
                    </div>

                    <!-- Stato Civile -->
                    <div class="form-group">
                        <label for="marital">Marital Status:</label>
                        <select id="marital" name="marital" required>
                            {% for marital in marital_options %}
                                <option value="{{ marital }}">{{ marital }}</option>
                            {% endfor %}
                        </select>
                    </div>

                    <!-- Istruzione -->
                    <div class="form-group">
                        <label for="education">Education:</label>
                        <select id="education" name="education" required>
                            {% for education in education_options %}
                                <option value="{{ education }}">{{ education }}</option>
                            {% endfor %}
                        </select>
                    </div>

                    <!-- Default -->
                    <div class="form-group">
                        <label for="default">Default:</label>
                        <select id="default" name="default" required>
                            <option value="yes">Sì</option>
                            <option value="no">No</option>
                        </select>
                    </div>

                    <!-- Saldo -->
                    <div class="form-group">
                        <label for="balance">Balance:</label>
                        <input type="number" id="balance" name="balance" required>
                    </div>

                    <!-- Mutuo -->
                    <div class="form-group">
                        <label for="housing">Housing:</label>
                        <select id="housing" name="housing" required>
                            {% for housing in housing_options %}
                                <option value="{{ housing }}">{{ housing }}</option>
                            {% endfor %}
                        </select>
                    </div>

                    <!-- Prestito -->
                    <div class="form-group">
                        <label for="loan">Loan:</label>
                        <select id="loan" name="loan" required>
                            {% for loan in loan_options %}
                                <option value="{{ loan }}">{{ loan }}</option>
                            {% endfor %}
                        </select>
                    </div>

                    <!-- Mese -->
                    <div class="form-group">
                        <label for="month">Month:</label>
                        <select id="month" name="month" required>
                            {% for month in month_options %}
                                <option value="{{ month }}">{{ month }}</option>
                            {% endfor %}
                        </select>
                    </div>

                    <!-- Numero di contatti -->
                    <div class="form-group">
                        <label for="campaign">Number of contacts during this campaign:</label>
                        <input type="number" id="campaign" name="campaign" required>
                    </div>

                    <!-- Risultato della campagna precedente -->
                    <div class="form-group">
                        <label for="poutcome">Result of the previous campaign:</label>
                        <select id="poutcome" name="poutcome" required>
                            <option value="unknown">Sconosciuto</option>
                            <option value="failure">Fallimento</option>
                            <option value="success">Successo</option>
                        </select>
                    </div>
            </div>        
                <!-- button -->
                <div class="container">
                    <div class="col">
                        <button type="submit" style="width:980px; text-align: center;">
                            <a class="btn btn-primary" style="width:980px">Predict</a>
                        </button>
                    </div>
                </div>
            </form>
        </main>


        <!-- Footer -->
        <footer class="footer">
            <div class="footer-content">
                <div class="footer-section">
                    <p>&copy; 2025 Excellent Bank Administration System. All rights reserved.</p>
                </div>
                <div class="footer-section">
                    <p><i class="fas fa-shield-alt"></i> Protected by enterprise-grade security</p>
                </div>
                <div class="footer-section links">
                    <a href="#">Privacy Policy</a> | 
                    <a href="#">Terms of Service</a> | 
                    <a href="#">Contact IT Support</a>
                </div>
            </div>
        </footer>

        <!-- JavaScript for displaying current time -->
        <script>
            function updateTime() {
                const timeElement = document.getElementById('current-time');
                const now = new Date();
                const options = { 
                    weekday: 'short', 
                    year: 'numeric', 
                    month: 'short', 
                    day: 'numeric',
                    hour: '2-digit',
                    minute: '2-digit',
                    second: '2-digit'
                };
                timeElement.textContent = now.toLocaleDateString('en-US', options);
            }

            // Update time immediately and then every second
            updateTime();
            setInterval(updateTime, 1000);
        </script>
    </body>
    </html>
    """
    return render_template_string(predict_template,
                                  css=css,
                                  username=session['username'],
                                  role=session['role'],
                                  job_options=job_options,
                                  marital_options=marital_options,
                                  education_options=education_options,
                                  housing_options=housing_options,
                                  loan_options=loan_options,
                                  month_options=month_options)

# Funzione per fare previsioni
@app.route('/predict', methods=['POST'])
def predict():
    data = request.form.to_dict()
    df_new = pd.DataFrame([data])
    df_new = pd.get_dummies(df_new).reindex(columns=columns, fill_value=0)
    df_scaled = scaler.transform(df_new)
    prediction = model.predict(df_scaled)[0]
    global latest_prediction_data
    # Get form data
    data = request.form.to_dict()

    # Create a dataframe with a single row
    df_new = pd.DataFrame([data])

    # Salviamo i dati originali per il download
    latest_prediction_data = df_new.copy()

    # Convert to right format for model
    df_new_encoded = pd.get_dummies(df_new).reindex(columns=columns, fill_value=0)
    df_scaled = scaler.transform(df_new_encoded)

    # Make prediction
    prediction = model.predict(df_scaled)[0]

    # Get probability of positive class
    probability = model.predict_proba(df_scaled)[0][1] * 100

    # Aggiungiamo la previsione ai dati originali
    latest_prediction_data['prediction'] = "Sì" if prediction == 1 else "No"
    latest_prediction_data['probability'] = f"{probability:.2f}%"

    result = "Sì" if prediction == 1 else "No"
    # Prepare the result HTML
    html = f"""
        <!DOCTYPE html>
        <html>
        <head>
            <title>Risultato Previsione</title>
            <style>
                * {{
                    margin: 0;
                    padding: 0;
                    box-sizing: border-box;
                    font-family: Arial, sans-serif;
                }}

                body {{
                    background-color: #f5f5f5;
                    color: #333;
                    line-height: 1.6;
                    padding: 20px;
                }}

                .container {{
                    max-width: 800px;
                    margin: 0 auto;
                    background-color: white;
                    padding: 30px;
                    border-radius: 8px;
                    box-shadow: 0 2px 10px rgba(0,0,0,0.1);
                }}

                h1 {{
                    text-align: center;
                    margin-bottom: 20px;
                    color: #2c3e50;
                }}

                .result {{
                    margin: 30px 0;
                    padding: 20px;
                    background-color: #f8f9fa;
                    border: 1px solid #ddd;
                    border-radius: 4px;
                    text-align: center;
                    font-size: 1.2em;
                }}

                .result-yes {{
                    color: #2ecc71;
                    font-weight: bold;
                }}

                .result-no {{
                    color: #e74c3c;
                    font-weight: bold;
                }}

                .probability {{
                    margin-top: 10px;
                    font-size: 0.9em;
                    color: #7f8c8d;
                }}

                .buttons {{
                    display: flex;
                    justify-content: space-between;
                    margin-top: 30px;
                }}

                .button {{
                    display: inline-block;
                    padding: 10px 20px;
                    background-color: #3498db;
                    color: white;
                    text-decoration: none;
                    border-radius: 4px;
                    text-align: center;
                }}

                .button:hover {{
                    background-color: #2980b9;
                }}
            </style>
        </head>
        <body>
            <div class="container">
                <h1>Risultato Previsione</h1>

                <div class="result">
                    Il cliente farà un deposito? 
                    <span class="result-{result.lower()}">{result}</span>
                    <div class="probability">Probabilità:{probability:.2f} %</div>
                </div>

                <div class="buttons">
                    <a href="/prediction_form" class="button">Nuova Previsione</a>
                    <a href="/dashboard" class="button">Torna alla Ricerca</a>
                    <a href="/download" class="button">Scarica Previsione</a>
                </div>
            </div>
        </body>
        </html>
        """
    return render_template_string(html)

# Success message when adding a new client
@app.route('/success')
def success():
    html = """<!DOCTYPE html>
    <html lang="it">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Successo</title>
        <style>
            body {
                font-family: system-ui, -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Oxygen, Ubuntu, Cantarell, sans-serif;
                background-color: #f5f5f5;
                display: flex;
                justify-content: center;
                align-items: center;
                min-height: 100vh;
                margin: 0;
                padding: 20px;
            }
            .container {
                text-align: center;
                padding: 40px;
                background-color: #fff;
                border-radius: 8px;
                box-shadow: 0 4px 8px rgba(0,0,0,0.1);
                width: 400px;
            }
            h1 {
                color: #2ecc71;
                font-size: 36px;
            }
            p {
                font-size: 18px;
                color: #333;
            }
            button {
                background-color: #3498db;
                color: white;
                border: none;
                padding: 12px 25px;
                font-size: 18px;
                border-radius: 5px;
                cursor: pointer;
                margin-top: 20px;
                transition: background-color 0.3s;
            }
            button:hover {
                background-color: #2980b9;
            }
        </style>
    </head>
    <body>

        <div class="container">
            <h1>Inserimento riuscito!</h1>
            <p>Il cliente è stato aggiunto con successo.</p>
            <a href="{{ url_for('dashboard') }}">
                <button>Torna al Dashboard</button>
            </a>
        </div>

    </body>
    </html>
    """

    return render_template_string(html)

# Success message when delete a new client
@app.route('/delete_success')
def delete_success():
    html = """<!DOCTYPE html>
        <html lang="it">
        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <title>Successo</title>
            <style>
                body {
                    font-family: system-ui, -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Oxygen, Ubuntu, Cantarell, sans-serif;
                    background-color: #f5f5f5;
                    display: flex;
                    justify-content: center;
                    align-items: center;
                    min-height: 100vh;
                    margin: 0;
                    padding: 20px;
                }
                .container {
                    text-align: center;
                    padding: 40px;
                    background-color: #fff;
                    border-radius: 8px;
                    box-shadow: 0 4px 8px rgba(0,0,0,0.1);
                    width: 400px;
                }
                h1 {
                    color: #00FF00;
                    font-size: 36px;
                }
                p {
                    font-size: 18px;
                    color: #333;
                }
                button {
                    background-color: #3498db;
                    color: white;
                    border: none;
                    padding: 12px 25px;
                    font-size: 18px;
                    border-radius: 5px;
                    cursor: pointer;
                    margin-top: 20px;
                    transition: background-color 0.3s;
                }
                button:hover {
                    background-color: #2980b9;
                }
            </style>
        </head>
        <body>

            <div class="container">
                <h1>Rimozione riuscita!</h1>
                <p>Il cliente è stato rimosso con successo.</p>
                <a href="{{ url_for('dashboard') }}">
                    <button>Torna al Dashboard</button>
                </a>
            </div>

        </body>
        </html>
        """

    return render_template_string(html)

@app.route('/logout')
def logout():
    session.pop('username', None)
    session.pop('role', None)
    flash('You have been logged out', 'info')
    return redirect(url_for('login'))

# Rotta per scaricare CSV con risultati
@app.route('/download', methods=['GET'])
def download():
    global latest_prediction_data

    # Se non abbiamo dati di previsione, restituiamo un messaggio di errore
    if latest_prediction_data is None:
        return "Nessuna previsione effettuata. Effettua prima una previsione."

    # Creiamo un file temporaneo
    filename = 'previsione_cliente.csv'
    latest_prediction_data.to_csv(filename, index=False)

    # Inviamo il file al client
    return send_file(filename, as_attachment=True)

if __name__ == '__main__':
    app.run(debug=True)