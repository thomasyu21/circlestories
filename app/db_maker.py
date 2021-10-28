# CircleTable
# SoftDev
# P00
# Oct 28 2021 


import sqlite3   # enable control of an sqlite database
import routes    # information from routes will be recorded in database

DB_FILE="storyboard.db"

db = sqlite3.connect(DB_FILE) # open if file exists, otherwise create
c = db.cursor()               # facilitate db ops 
try:
    # Users table
    command = "CREATE TABLE users(username TEXT, email TEXT, password TEXT);"      
    c.execute(command)    # run SQL statement 

    # Stories table
    command = "CREATE TABLE stories(username TEXT, first_block_id INTEGER, last_block_id INTEGER);"      
    c.execute(command)   

except:
    print("Database already exists")

# Test Method
for row in c.execute("SELECT * FROM users"):
    print(row)
for row in c.execute("SELECT * FROM stories"):
    print(row)

db.commit() #save changes
db.close()  #close database


