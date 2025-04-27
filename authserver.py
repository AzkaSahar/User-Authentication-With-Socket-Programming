import socket
import ssl
import sqlite3
import hashlib

# Function to check if username exists in DB
def check_username_exists(username):
    conn = sqlite3.connect('users.db')
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM users WHERE username=?', (username,))
    result = cursor.fetchone()
    conn.close()
    return result

# Function to register a user
def register_user(username, password):
    hashed_password = hashlib.sha256(password.encode()).hexdigest()
    
    conn = sqlite3.connect('users.db')
    cursor = conn.cursor()

    try:
        # Check if the username already exists before inserting
        cursor.execute('SELECT username FROM users WHERE username=?', (username,))
        existing_user = cursor.fetchone()
        
        if existing_user:
            return "Error: Username already exists."
        
        # Insert the new user
        cursor.execute('INSERT INTO users (username, password) VALUES (?, ?)', (username, hashed_password))
        conn.commit()
        return "Success: User registered!"
    
    except sqlite3.OperationalError as e:
        # Handle OperationalError, like database locking
        return f"Error: {str(e)}"
    
    finally:
        # Always close the connection
        conn.close()

# Function to authenticate a user
def authenticate_user(username, password):
    conn = sqlite3.connect('users.db')
    cursor = conn.cursor()
    cursor.execute('SELECT password FROM users WHERE username=?', (username,))
    result = cursor.fetchone()
    conn.close()
    if result and hashlib.sha256(password.encode()).hexdigest() == result[0]:
        return "Success: User authenticated!"
    return "Error: Invalid credentials."

# Server setup
HOST = 'localhost'
PORT = 12345

# Paths to your certificate and key files
CERT_FILE = "cert.pem"  # Replace with your file path
KEY_FILE = "key.pem"     # Replace with your file path

# Create SSL context
context = ssl.create_default_context(ssl.Purpose.CLIENT_AUTH)
context.load_cert_chain(certfile=CERT_FILE, keyfile=KEY_FILE)

# Create and bind the socket
with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.bind((HOST, PORT))
    s.listen(5)
    print(f"Server running securely on {HOST}:{PORT}...")

    # Wrap the socket with SSL using the context
    secure_socket = context.wrap_socket(s, server_side=True)

    while True:
        conn, addr = secure_socket.accept()
        with conn:
            print('Connected by', addr)
            data = conn.recv(1024).decode('utf-8')
            if data:
                print(f"Received request: {data}")
                
                if data.startswith("REGISTER:"):
                    # Handle registration
                    _, username, password = data.split(":")
                    response = register_user(username, password)
                elif data.startswith("LOGIN:"):
                    # Handle login
                    _, username, password = data.split(":")
                    response = authenticate_user(username, password)
                else:
                    response = "Error: Invalid request."

                # Send the response back to the client
                conn.sendall(response.encode('utf-8'))
