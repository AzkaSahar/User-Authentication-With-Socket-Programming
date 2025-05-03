import sqlite3
conn = sqlite3.connect("users.db")
cursor = conn.cursor()
cursor.execute("SELECT password FROM users WHERE username=?", ("azka",))
result = cursor.fetchone()
print(type(result[0]))  # Should be <class 'bytes'>
