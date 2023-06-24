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
     if (length < 6):
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
    print("Hello Existing customer!")
    name = input("Please enter your name.")
    dob = str(input("Please enter your date of birth DD/MM/YYYY"))
    password = input("Please type your password")
