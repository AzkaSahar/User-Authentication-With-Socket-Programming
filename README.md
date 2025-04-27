# **Client-Server Authentication System with Flask and Socket Programming**

This project implements a simple **client-server authentication system** using **Flask** for the frontend and **socket programming** for secure communication between the client and server. It features secure login and registration, utilizing **SHA-256** encryption for password storage and SSL/TLS for secure communication.

## **Features**
- **User Registration & Login**: Allows users to register and authenticate securely.
- **Socket Communication**: Communication between client and server over secure SSL/TLS sockets.
- **Password Encryption**: User passwords are securely hashed using SHA-256.
- **Session Management**: Maintains user sessions during authentication.
- **Secure Socket Communication**: Uses SSL/TLS for encrypted communication between client and server.

---

## **Requirements**

To run this project, you'll need the following:

- Python 3.8+
- OpenSSL (for generating SSL certificates)
- Required Python libraries (listed in `requirements.txt`)

### **Required Libraries**
- Flask
- Flask-Bootstrap
- Werkzeug
- WTForms
- itsdangerous
- Jinja2

---

## **Setup Instructions**

### **1. Install Python**
Ensure that you have **Python 3.8+** installed on your system. You can download it from [python.org](https://www.python.org/downloads/).

### **2. Install OpenSSL**
You need **OpenSSL** to generate the certificates for SSL encryption. Download and install OpenSSL for Windows (or your respective OS):

- [OpenSSL for Windows](https://slproweb.com/products/Win32OpenSSL.html)

### **3. Clone the Repository**
Clone the repository to your local machine.

```bash
git clone https://github.com/your-username/client-server-authentication.git
cd client-server-authentication
```

### **4. Install Dependencies**
Install the required Python dependencies using `pip`:

```bash
pip install -r requirements.txt
```

### **5. Generate SSL Certificates**
Generate the **SSL certificates** (`cert.pem` and `key.pem`) using OpenSSL to enable secure socket communication.

```bash
openssl genpkey -algorithm RSA -out key.pem
openssl req -new -x509 -key key.pem -out cert.pem -days 365
```

Make sure the generated `cert.pem` and `key.pem` files are in the project directory.

---

## **Running the Project**

### **1. Start the Server**
Run the server using the following command:

```bash
python server.py
```

The server will start and listen on port `12345` for incoming client connections. It will be securely running over SSL.

### **2. Start the Flask Application (Client)**
Run the Flask client application using:

```bash
python client.py
```

This will start the Flask web server, and you can access the client interface through your browser at:

```
http://localhost:5000
```

### **3. Interact with the Application**
- **Register** a new user by navigating to `/register`.
- **Login** with the registered credentials at `/login`.
- If the login is successful, you will be redirected to `/success`.

---

## **Project Structure**

```
/client-server-authentication
│
├── client.py              # Flask application for user interaction (login, register)
├── server.py              # Server-side logic handling authentication via sockets
├── cert.pem               # SSL certificate for secure communication
├── key.pem                # SSL key for secure communication
├── requirements.txt       # List of dependencies
├── templates/             # HTML templates for Flask application
│   ├── index.html
│   ├── login.html
│   ├── register.html
│   └── success.html
└── README.md              # Project documentation
```

---

## **License**

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
