import json
import random
from datetime import datetime
from flask import Flask, render_template, request, redirect, url_for, session

app = Flask(__name__)
app.secret_key = "your_secret_key"

# Function to load user data
def load_user():
    with open("info.json", "r") as file:
        users = json.load(file)
        return users if isinstance(users, list) else [users]

# Function to find a user by name and password
def find_user(name, password):
    users = load_user()
    for user in users:
        if user["name"] == name and user["password"] == password:
            return user
    return None

# Function to perform payment
def perform_payment(name, creditid):
    print("Welcome to the payment section, " + name + ".")
    recipient = request.form['recipient']

    suspicious_usernames = ["Scam", "Unverified", "Fake", "Fraud"]  # Add more suspicious usernames if needed

    if recipient.lower() in suspicious_usernames:
        print("Our automated sources detect this user to be malicious.")
        agree_or_not = request.form['agree_or_not']

        if agree_or_not.lower() == "no":
            print("No problem, " + name + ". I have cancelled this transaction for you.")
            return redirect(url_for('home'))  # Redirect back to the homepage

    send_money = int(request.form['send_money'])

    if send_money < 10000:
        agree_or_not1 = request.form['agree_or_not1']
        if agree_or_not1.lower() == "no":
            print("No problem, " + name + ". I have cancelled this transaction for you.")
            return redirect(url_for('home'))  # Redirect back to the homepage

    payment_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    payment_data = {
        "name": name,
        "recipient": recipient,
        "amount": send_money,
        "payment_time": payment_time,
        "credit_id": creditid  # Add the credit ID to the payment data
    }

    with open("paymentinfo.json", "a") as file:
        json.dump(payment_data, file)
        file.write('\n') 

    print("Payment successful.") 
    return redirect(url_for('home'))  # Redirect back to the homepage

# Main function
@app.route('/')
def home():
    return render_template('index.html')

@app.route('/login.html', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        new_or_not = request.form['new_or_not']

        if new_or_not.lower() == "new":
            name = request.form['name']
            dob = request.form['dob']
            phone = request.form['phone']
            password = request.form['password']

            while len(password) < 6:
                return render_template('login.html', message="Password needs to be above 6 characters.")

            # Generate credit ID
            varia = random.randint(1000, 9999)
            varib = random.randint(1000, 9999)
            varic = random.randint(1000, 9999)
            varid = random.randint(1000, 9999)
            creditid = f"{varia}-{varib}-{varic}-{varid}"

            user = {
                "name": name,
                "dob": dob,
                "password": password,
                "phone": phone,
                "creditid": creditid
            }

            users = load_user()
            users.append(user)

            with open("info.json", "w") as file:
                json.dump(users, file)

            session["name"] = user["name"]
            session["password"] = user["password"]

        else:
            name = request.form['name']
            password = request.form['password']

            user = find_user(name, password)

            if user is None:
                return render_template('login.html', message="Sorry, this information is incorrect. Please try again.")

            session["name"] = user["name"]
            session["password"] = user["password"]

        session["authenticated"] = True
        return redirect(url_for('dashboard'))  # Redirect to the dashboard page

    return render_template('login.html')

@app.route('/dashboard')
def dashboard():
    if "authenticated" not in session or not session["authenticated"]:
        return redirect(url_for('login'))

    user = find_user(session["name"], session["password"])

    return render_template('dashboard.html', user=user)

@app.route('/payment', methods=['POST'])
def payment():
    if "authenticated" not in session or not session["authenticated"]:
        return redirect(url_for('login'))

    user = find_user(session["name"], session["password"])

    return perform_payment(user["name"], user["creditid"])

@app.route('/transactions')
def transactions():
    if "authenticated" not in session or not session["authenticated"]:
        return redirect(url_for('login'))

    # Implement recent transactions functionality
    return render_template('transactions.html')

@app.route('/balance')
def balance():
    if "authenticated" not in session or not session["authenticated"]:
        return redirect(url_for('login'))

    # Implement account balance functionality
    return render_template('balance.html')

@app.route('/settings')
def settings():
    if "authenticated" not in session or not session["authenticated"]:
        return redirect(url_for('login'))

    # Implement account settings functionality
    return render_template('settings.html')

@app.route('/logout')
def logout():
    session.pop("authenticated", None)
    session.pop("name", None)
    session.pop("password", None)
    return redirect(url_for('home'))  # Redirect back to the homepage

# Run the Flask application
if __name__ == "__main__":
    app.run()
