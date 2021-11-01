# CircleTable
# SoftDev
# P00
# 2021-10-28


import sqlite3  # Enable control of an sqlite database
import routes  # Information from routes will be recorded in database


def main():
    DB_FILE = "storyboard.db"

    db = sqlite3.connect(DB_FILE)  # Open if file exists, otherwise create
    c = db.cursor()  # Facilitate db ops

    # Create tables if exists
    c.execute("CREATE TABLE IF EXISTS users(username TEXT, email TEXT, password TEXT);")

#----------------------------------------------------
    # Test Method
    for row in c.execute("SELECT * FROM users"):
        print(row)
    for row in c.execute("SELECT * FROM stories"):
        print(row)

    db.commit()  # Save changes
    db.close()  # Close database


if __name__ == "__main__":
    main()
