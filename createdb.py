import sqlite3

# Connect to SQLite database (it will create if it doesn't exist)
conn = sqlite3.connect('users.db')
cursor = conn.cursor()

# Create users table if it doesn't exist
cursor.execute('''
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT NOT NULL UNIQUE,
        password BLOB NOT NULL
    )
''')

conn.commit()
conn.close()

print("Database and table created successfully!")
