import socket
import ssl
import sqlite3
import logging
import bcrypt

# Setup logging
logging.basicConfig(filename='app.log', level=logging.INFO,
                    format='%(asctime)s - SERVER - %(levelname)s - %(message)s')

def register_user(username, password):
    hashed_password = bcrypt.hashpw(password.encode(), bcrypt.gensalt())

    conn = sqlite3.connect('users.db')
    cursor = conn.cursor()

    try:
        cursor.execute('SELECT username FROM users WHERE username=?', (username,))
        if cursor.fetchone():
            logging.warning(f"Registration failed: Username '{username}' already exists.")
            return "Error: Username already exists."

        cursor.execute('INSERT INTO users (username, password) VALUES (?, ?)', (username, hashed_password))
        conn.commit()
        logging.info(f"User '{username}' registered successfully.")
        return "Success: User registered!"
    except sqlite3.OperationalError as e:
        logging.error(f"Database error during registration: {e}")
        return f"Error: {str(e)}"
    finally:
        conn.close()


def authenticate_user(username, password):
    conn = sqlite3.connect('users.db')
    cursor = conn.cursor()
    cursor.execute('SELECT password FROM users WHERE username=?', (username,))
    result = cursor.fetchone()
    conn.close()

    if result and bcrypt.checkpw(password.encode(), result[0]):
        logging.info(f"User '{username}' authenticated successfully.")
        return "Success: User authenticated!"

    logging.warning(f"Authentication failed for user '{username}'.")
    return "Error: Invalid credentials."

# Server setup
HOST = 'localhost'
PORT = 12345
CERT_FILE = "cert.pem"
KEY_FILE = "key.pem"

context = ssl.create_default_context(ssl.Purpose.CLIENT_AUTH)
context.load_cert_chain(certfile=CERT_FILE, keyfile=KEY_FILE)

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.bind((HOST, PORT))
    s.listen(5)
    logging.info(f"Server started securely on {HOST}:{PORT}")
    secure_socket = context.wrap_socket(s, server_side=True)

    while True:
        conn, addr = secure_socket.accept()
        with conn:
            logging.info(f"Connection accepted from {addr}")
            data = conn.recv(1024).decode('utf-8')
            if data:
                logging.info(f"Request received: {data}")
                if data.startswith("REGISTER:"):
                    _, username, password = data.split(":")
                    response = register_user(username, password)
                elif data.startswith("LOGIN:"):
                    _, username, password = data.split(":")
                    response = authenticate_user(username, password)
                else:
                    response = "Error: Invalid request."
                    logging.warning(f"Invalid request received: {data}")
                conn.sendall(response.encode('utf-8'))
