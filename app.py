from flask import Flask, render_template, request, redirect, url_for, flash, session
import socket
import hashlib
from flask_bootstrap import Bootstrap

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Needed for sessions and flash messages
Bootstrap(app)

# Server address (the server should be running)
SERVER_HOST = 'localhost'
SERVER_PORT = 12345

import ssl
# SSL context for client
context = ssl.create_default_context()
context.check_hostname = False
context.verify_mode = ssl.CERT_NONE

# Function to communicate securely with the server via socket
def send_request_to_server(request_data):
    with socket.create_connection((SERVER_HOST, SERVER_PORT)) as sock:
        with context.wrap_socket(sock, server_hostname=SERVER_HOST) as ssock:
            ssock.sendall(request_data.encode('utf-8'))
            response = ssock.recv(1024).decode('utf-8')
    return response

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
            session['username'] = username  # Save username in session
            flash('Login successful!', 'success')
            return redirect(url_for('success'))
        else:
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
            flash('Registration successful! You can now log in.', 'success')
            return redirect(url_for('login'))
        else:
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
    session.pop('username', None)
    flash('You have been logged out.', 'info')
    return redirect(url_for('login'))

if __name__ == '__main__':
    app.run(debug=True)
