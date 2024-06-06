import sqlite3

def sign_up(user_name, user_password, user_image):
    connection = sqlite3.connect("users.db")
    cursor = connection.cursor()
    cursor.execute("INSERT INTO users VALUES (?, ?, ?)", (user_name, user_password, user_image))
    connection.commit()
    connection.close()

def login(user_name, user_password):
    connection = sqlite3.connect("users.db")
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM users WHERE username =? AND password =?", (user_name, user_password))
    user = cursor.fetchone()
    connection.close()
    return user
