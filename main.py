import json
import random
from datetime import datetime
from flask import Flask, render_template, request, redirect, url_for, session, flash

app = Flask(__name__)
app.secret_key = "your_secret_key"
app.static_folder = 'img'

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

    with open('sus.txt', 'r') as file:
        suspicious_usernames = file.read().splitlines()

    if recipient.lower() in suspicious_usernames:
        print("Our automated sources detect this user to be malicious.")
        flash("This recipient is flagged as suspicious. Please contact customer support for assistance.")
        return redirect(url_for('fraud_help'))

    send_money = int(request.form['send_money'])

    if send_money >= 10000:
        flash("Transaction amount is above or equal to 10000. Please contact customer support for assistance.")
        return redirect(url_for('fraud_help'))

    payment_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    payment_data = {
        "name": name,
        "recipient": recipient,
        "amount": send_money,
        "payment_time": payment_time,
        "credit_id": creditid,  # Add the credit ID to the payment data
    }

    with open("paymentinfo.json", "a") as file:
        json.dump(payment_data, file)
        file.write('\n')

    print("Payment successful.")
    session['payment_successful'] = True
    return redirect(url_for('done'))

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

            # Generate bal
            bal = random.randint(0, 9999)

            user = {
                "name": name,
                "dob": dob,
                "password": password,
                "phone": phone,
                "creditid": creditid,
                "balance": bal
            }

            users = load_user()
            users.append(user)

            with open("info.json", "w") as file:
                json.dump(users, file)

            return redirect(url_for('login'))

        elif new_or_not.lower() == "returning":
            name = request.form['name']
            password = request.form['password']

            user = find_user(name, password)

            if user is not None:
                session['authenticated'] = True
                session['user'] = user
                return redirect(url_for('dashboard'))
            else:
                return render_template('login.html', message="Invalid username or password.")

    return render_template('login.html')

@app.route('/dashboard')
def dashboard():
    if "authenticated" not in session or not session["authenticated"]:
        return redirect(url_for('login'))

    user = session.get('user')
    return render_template('dashboard.html', user=user)

@app.route('/payment', methods=['GET', 'POST'])
def payment():
    user = session.get('user')

    if user is None:
        return redirect(url_for('login'))

    if request.method == 'POST':
        return perform_payment(user["name"], user["creditid"])

    return render_template('payment.html', user=user)


@app.route('/transactions')
def transactions():
    if "authenticated" not in session or not session["authenticated"]:
        return redirect(url_for('login'))

    # Load transaction data from paymentinfo.json
    with open("paymentinfo.json", "r") as file:
        transactions = [json.loads(line) for line in file]

    return render_template('transactions.html', transactions=transactions)


@app.route('/logout')
def logout():
    session.pop('authenticated', None)
    session.pop('user', None)
    return redirect(url_for('login'))

@app.route('/fraud-help')
def fraud_help():
    return render_template('Fraudhelp.html')

@app.route('/settings')
def settings():
    user = session.get('user')

    if user is None:
        return redirect(url_for('login'))

    return render_template('settings.html', user=user)


@app.route('/done')
def done():
    payment_successful = session.get('payment_successful')
    if payment_successful:
        del session['payment_successful']
        return render_template('done.html')
    else:
        return redirect(url_for('home'))  # Redirect to the home page if payment not successful

if __name__ == '__main__':
    app.run(debug=True)
