from flask import Flask, render_template, request, redirect, url_for, flash, session
import socket
from flask_bootstrap import Bootstrap
import ssl
import logging

# Setup logging
logging.basicConfig(filename='app.log', level=logging.INFO,
                    format='%(asctime)s - CLIENT - %(levelname)s - %(message)s')

app = Flask(__name__)
app.secret_key = 'your_secret_key'
Bootstrap(app)

SERVER_HOST = 'localhost'
SERVER_PORT = 12345

# SSL context for client
context = ssl.create_default_context()
context.check_hostname = False
context.verify_mode = ssl.CERT_NONE

def send_request_to_server(request_data):
    try:
        with socket.create_connection((SERVER_HOST, SERVER_PORT)) as sock:
            with context.wrap_socket(sock, server_hostname=SERVER_HOST) as ssock:
                ssock.sendall(request_data.encode('utf-8'))
                response = ssock.recv(1024).decode('utf-8')
        return response
    except Exception as e:
        logging.error(f"Error communicating with server: {e}")
        return "Error: Could not connect to server"

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        login_request = f"LOGIN:{username}:{password}"
        response = send_request_to_server(login_request)

        if "Success" in response:
            session['username'] = username
            logging.info(f"User '{username}' logged in successfully.")
            flash('Login successful!', 'success')
            return redirect(url_for('success'))
        else:
            logging.warning(f"Failed login attempt for user '{username}'.")
            flash('Invalid credentials. Please try again.', 'danger')

    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        register_request = f"REGISTER:{username}:{password}"
        response = send_request_to_server(register_request)

        if "Success" in response:
            logging.info(f"User '{username}' registered successfully.")
            flash('Registration successful! You can now log in.', 'success')
            return redirect(url_for('login'))
        else:
            logging.warning(f"Failed registration for user '{username}': {response}")
            flash(response, 'danger')

    return render_template('register.html')

@app.route('/success')
def success():
    if 'username' not in session:
        flash('Please log in to access this page.', 'warning')
        return redirect(url_for('login'))
    return render_template('success.html', username=session['username'])

@app.route('/logout')
def logout():
    username = session.pop('username', None)
    logging.info(f"User '{username}' logged out.")
    flash('You have been logged out.', 'info')
    return redirect(url_for('login'))

if __name__ == '__main__':
    app.run(debug=True)
