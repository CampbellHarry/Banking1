import json
import string
import random 
import datetime
import math
import os





varia = random.randint(1000,9999)
varib = random.randint(1000,9999) 
varic = random.randint(1000,9999)
varid = random.randint(1000,9999)

#bank openingnew
newornot = input("Hello there, Are you a new customer or an existing customer?")
if newornot == "new" or "New":
    name = input("Welcome new customer! What is your Name?")
    dob = str(input("What is your date of birth DD/MM/YYYY"))
    phone = input("Please input your phone number")
    password = input("Please enter a secure password. (It must be over 6 charectors)")
    length = len(password)
    while True:
    if (length > 6):
        print("Password needs to be above 6 Chars")
        break
     else:
        #this is kinda like a bank id thing
        creditid = varia,varib,varic,varid
        user = {
    "name": name,
    "dob": dob,
    "password": password,
    "phoneno" : phone,
    "creditid": creditid
    }
        with open("info.json", "w") as file:
         json.dump(user, file)
         break         
if newornot != "new" or "New":
while True:
    print("Hello Existing customer!")
    name = input("Please enter your name.")
    dob = str(input("Please enter your date of birth DD/MM/YYYY"))
    password = input("Please type your password")
    code = random.randint(100000,999999)
    print(code)
    factorauth = input("We have sent a 2 factor authentication code to your phone please type this 6 didgit code in.")
    if factorauth != code:
      print("This 2 factor authentication code is incorrect.")
    customer = name + dob + password
    if customer != "info.json":
       print("Sorry this information is incorrect please try again") 
    else:
      while True:
       print("Welcome" + name + "Welcome to H banking.")
       path = input("Where do you wish to go" + name + "Make a payment, See your recent transactions, Account balence, Account Settings.")
       if "payment" in path:
        while True:   
         print("Welcome to the payment section " + name + ".")
         recipient = input("Who would you like to send a payment to?")
         sendmoney = input("How much money do you want to send to" + recipient)
         if recipient == string.lower("Scam", "Unverified", "fake", "fraud","free","duplicate"):
           print("Our automated sources detect this user to be mallcious.")
           agreeornot = input("You may be in danger of a scam. Do you want to proceed?")
           if sendmoney < 1000:
             print("This may be a scam" + name + ".")
             continuescam = input("Due to you sending a large ammount of money to " + recipient + ". This has triggered one of our anti-scam systems. Do you want to continue?")
             if agreeornot and continuescam == "no" or "No" or "NO":
               print("No problem" + name + ". I have cancelled this transaction for you. You will now be sent back to the home page")
             else:
               paytime = datetime.now()
               money = {
                 "name" : name,
                 "recipient" : recipient,
                 "Sent" : sendmoney,
                 "Time of payment" : paytime
               }
               with open("paymentinfo.json", "w") as file:
                json.dump(user, file)
                break     