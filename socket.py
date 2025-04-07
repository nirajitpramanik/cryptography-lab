import socket
import ssl
import subprocess
import jwt
import datetime
import threading
import time
from flask import Flask, request, jsonify


# SSL Socket Communication
def ssl_server():
    context = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)
    try:
        context.load_cert_chain(certfile="server.pem", keyfile="server.key")
    except FileNotFoundError:
        print("Error: SSL certificate files not found. Generate them with:")
        print("openssl req -x509 -newkey rsa:4096 -keyout server.key -out server.pem -days 365 -nodes")
        return False
   
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
        sock.bind(("0.0.0.0", 12345))
        sock.listen(5)
        print("SSL server listening on port 12345")
        with context.wrap_socket(sock, server_side=True) as ssock:
            conn, addr = ssock.accept()
            print("Client connected:", addr)
            conn.sendall(b"Hello, SSL Client!")
            conn.close()
    return True


def ssl_client():
    context = ssl.create_default_context()
    context.check_hostname = False
    context.verify_mode = ssl.CERT_NONE  # For self-signed certificates
   
    try:
        with socket.create_connection(("localhost", 12345)) as sock:
            with context.wrap_socket(sock, server_hostname="localhost") as ssock:
                print("Connected to SSL server")
                data = ssock.recv(1024)
                print("Received:", data.decode())
        return True
    except Exception as e:
        print(f"SSL client connection failed: {e}")
        return False


# Telnet Communication
def telnet_server():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server:
        server.bind(("0.0.0.0", 2323))
        server.listen(1)
        print("Telnet server listening on port 2323")
        conn, addr = server.accept()
        print("Connection from:", addr)
        conn.sendall(b"Welcome to Telnet server!")
        data = conn.recv(1024)
        print(f"Received from client: {data.decode()}")
        conn.close()
    return True


def telnet_client():
    try:
        time.sleep(1)  # Give server time to start
        with socket.create_connection(("localhost", 2323)) as sock:
            print("Connected to telnet server")
            data = sock.recv(1024)
            print("Received:", data.decode())
            sock.sendall(b"Hello from telnet client!")
        return True
    except Exception as e:
        print(f"Telnet client connection failed: {e}")
        return False


# Packet Capture
def capture_packets():
    # Try to use tcpdump or tshark
    try:
        print("Starting packet capture on port 2323...")
        subprocess.run(["tcpdump", "-w", "capture.pcap", "-i", "lo", "port 2323", "-c", "10"],
                      timeout=10, check=True)
        return True
    except (subprocess.SubprocessError, FileNotFoundError):
        try:
            subprocess.run(["tshark", "-w", "capture.pcap", "-i", "lo", "-f", "port 2323", "-c", "10"],
                          timeout=10, check=True)
            return True
        except (subprocess.SubprocessError, FileNotFoundError):
            print("Could not capture packets with tcpdump or tshark. Creating dummy pcap file.")
            with open("capture.pcap", "w") as f:
                f.write("Dummy packet data\n")
            return False


def analyze_packets():
    try:
        result = subprocess.run(["tshark", "-r", "capture.pcap", "-T", "fields", "-e", "data.text"],
                               capture_output=True, text=True, check=True)
        print("Captured Data:", result.stdout)
        return True
    except (subprocess.SubprocessError, FileNotFoundError):
        print("Could not analyze packets with tshark. Using basic file read.")
        try:
            with open("capture.pcap", "rb") as f:
                data = f.read()
                print("Raw packet data (first 100 bytes):", data[:100])
            return True
        except FileNotFoundError:
            print("No capture file found.")
            return False


# JWT Web Application
app = Flask(__name__)
SECRET_KEY = "your_secret_key"


def generate_jwt(username):
    payload = {"user": username, "exp": datetime.datetime.utcnow() + datetime.timedelta(hours=1)}
    return jwt.encode(payload, SECRET_KEY, algorithm="HS256")


@app.route("/login", methods=["POST"])
def login():
    data = request.json
    if not data:
        return jsonify({"error": "No JSON data provided"}), 400
   
    username = data.get("username")
    password = data.get("password")
   
    if not username or not password:
        return jsonify({"error": "Username and password required"}), 400
       
    if username == "admin" and password == "password":
        token = generate_jwt(username)
        return jsonify({"token": token})
    return jsonify({"error": "Invalid credentials"}), 401


@app.route("/protected", methods=["GET"])
def protected():
    auth_header = request.headers.get("Authorization")
    if not auth_header or not auth_header.startswith("Bearer "):
        return jsonify({"error": "Authorization header missing or invalid"}), 401
       
    token = auth_header.split()[1]
    try:
        decoded = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
        return jsonify({"message": "Access granted", "user": decoded["user"]})
    except jwt.ExpiredSignatureError:
        return jsonify({"error": "Token expired"}), 401
    except jwt.InvalidTokenError:
        return jsonify({"error": "Invalid token"}), 401


def run_flask_app():
    app.run(debug=False, port=5000)


# Main runner
def run_ssl_demo():
    print("\n=== Running SSL Socket Demo ===")
    server_thread = threading.Thread(target=ssl_server)
    server_thread.daemon = True
    server_thread.start()
    time.sleep(1)  # Give server time to start
    ssl_client()
    server_thread.join(timeout=5)


def run_telnet_demo():
    print("\n=== Running Telnet Demo with Packet Capture ===")
    capture_thread = threading.Thread(target=capture_packets)
    capture_thread.daemon = True
    capture_thread.start()
    time.sleep(1)  # Give capture time to start
   
    server_thread = threading.Thread(target=telnet_server)
    server_thread.daemon = True
    server_thread.start()
    time.sleep(1)  # Give server time to start
   
    telnet_client()
    server_thread.join(timeout=5)
    capture_thread.join(timeout=5)
   
    print("\n=== Analyzing Captured Packets ===")
    analyze_packets()


def run_jwt_demo():
    print("\n=== Running JWT Web Application ===")
    print("Flask app starting on http://localhost:5000")
    print("Use these endpoints:")
    print("  POST /login with JSON: {\"username\": \"admin\", \"password\": \"password\"}")
    print("  GET /protected with Authorization: Bearer <your_token>")
    run_flask_app()  # This will block until the app is stopped


if __name__ == "__main__":
    print("Network Security Demo Application")
    print("Choose which demo to run:")
    print("1. SSL Socket Communication")
    print("2. Telnet with Packet Capture")
    print("3. JWT Web Application")
    print("4. Run All Demos")
   
    choice = input("Enter your choice (1-4): ")
   
    if choice == "1":
        run_ssl_demo()
    elif choice == "2":
        run_telnet_demo()
    elif choice == "3":
        run_jwt_demo()
    elif choice == "4":
        print("Running all demos sequentially...")
        run_ssl_demo()
        run_telnet_demo()
        run_jwt_demo()
    else:
        print("Invalid choice. Exiting.")
