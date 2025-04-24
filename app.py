import flask
from flask import Flask, render_template, request, jsonify
import pyautogui
import webbrowser
import time
import pyperclip
import threading
import os

app = Flask(__name__)

# Function that will run the automation script
def send_whatsapp_messages(number, message, repeat_count):
    # Open WhatsApp Web with target chat
    url = f"https://web.whatsapp.com/send?phone={number}&text="
    webbrowser.open(url)
    
    # Wait for WhatsApp Web to load (adjust if needed)
    print("Loading WhatsApp Web... Please wait 15 seconds.")
    time.sleep(15)
    
    # Send messages very fast
    for i in range(repeat_count):
        pyperclip.copy(message)  # Copy the original message
        pyautogui.hotkey("ctrl", "v")  # Paste the message
        pyautogui.press("enter")  # Press Enter to send
        print(f"Sent: {message}")  # Print out the message sent
        time.sleep(0.1)  # Super fast! Can reduce to 0.1 if stable
    
    return {"status": "success", "messages_sent": repeat_count}

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/send', methods=['POST'])
def send():
    data = request.json
    number = data.get('phone', '').strip()
    message = data.get('message', '').strip()
    repeat_count = int(data.get('count', 1))
    
    # Start the sending process in a separate thread
    # This allows the server to respond immediately while the automation runs
    thread = threading.Thread(
        target=send_whatsapp_messages,
        args=(number, message, repeat_count)
    )
    thread.daemon = True
    thread.start()
    
    return jsonify({"status": "started", "message": "WhatsApp Web is opening. Please wait."})

# Create templates directory if it doesn't exist
if not os.path.exists('templates'):
    os.makedirs('templates')

# Create the HTML template
with open('templates/index.html', 'w') as f:
    f.write('''
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>WhatsApp Message Sender</title>
    <style>
        body {
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            background-color: #f0f2f5;
            margin: 0;
            padding: 20px;
            display: flex;
            justify-content: center;
            align-items: center;
            min-height: 100vh;
        }
        .container {
            background-color: white;
            border-radius: 10px;
            box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
            width: 100%;
            max-width: 500px;
            padding: 30px;
        }
        h1 {
            color: #128C7E;
            margin-top: 0;
            text-align: center;
        }
        .form-group {
            margin-bottom: 20px;
        }
        label {
            display: block;
            margin-bottom: 8px;
            font-weight: 500;
            color: #333;
        }
        input, textarea {
            width: 100%;
            padding: 12px;
            border: 1px solid #ddd;
            border-radius: 6px;
            box-sizing: border-box;
            font-size: 16px;
        }
        textarea {
            min-height: 100px;
            resize: vertical;
        }
        button {
            background-color: #128C7E;
            color: white;
            border: none;
            padding: 12px 20px;
            border-radius: 6px;
            cursor: pointer;
            font-size: 16px;
            width: 100%;
            font-weight: 500;
            transition: background-color 0.3s;
        }
        button:hover {
            background-color: #075E54;
        }
        .status {
            margin-top: 20px;
            padding: 15px;
            border-radius: 6px;
            background-color: #f8f9fa;
            display: none;
        }
        .status.success {
            display: block;
            background-color: #d4edda;
            color: #155724;
            border: 1px solid #c3e6cb;
        }
        .status.error {
            display: block;
            background-color: #f8d7da;
            color: #721c24;
            border: 1px solid #f5c6cb;
        }
        .status.warning {
            display: block;
            background-color: #fff3cd;
            color: #856404;
            border: 1px solid #ffeeba;
        }
        .status.info {
            display: block;
            background-color: #d1ecf1;
            color: #0c5460;
            border: 1px solid #bee5eb;
        }
        .instructions {
            margin-top: 25px;
            background-color: #e9f7fe;
            padding: 15px;
            border-radius: 6px;
            font-size: 14px;
        }
        .instructions h3 {
            margin-top: 0;
            color: #0277bd;
        }
        .instructions ol {
            padding-left: 20px;
            margin-bottom: 0;
        }
        .instructions li {
            margin-bottom: 8px;
        }
    </style>
</head>
<body>
    <div class="container">
        <h1>WhatsApp Message Sender</h1>
        
        <div class="form-group">
            <label for="phone">Phone Number (with country code)</label>
            <input type="text" id="phone" placeholder="e.g. 91XXXXXXXXXX" required>
        </div>
        
        <div class="form-group">
            <label for="message">Message</label>
            <textarea id="message" placeholder="Type your message here..." required></textarea>
        </div>
        
        <div class="form-group">
            <label for="count">Number of Times to Send</label>
            <input type="number" id="count" min="1" max="1000" value="1" required>
        </div>
        
        <button onclick="sendMessage()">Start Sending</button>
        
        <div id="status" class="status"></div>
        
        <div class="instructions">
            <h3>Important Instructions:</h3>
            <ol>
                <li>Enter the recipient's phone number with country code (no + symbol)</li>
                <li>Type your message</li>
                <li>Choose how many times to send the message</li>
                <li>Click "Start Sending"</li>
                <li>WhatsApp Web will open automatically</li>
                <li><strong>Do not touch your mouse or keyboard</strong> during the automation process</li>
                <li>Make sure you're already logged into WhatsApp Web or be ready to scan the QR code when prompted</li>
            </ol>
        </div>
    </div>

    <script>
        function sendMessage() {
            const phone = document.getElementById('phone').value.trim();
            const message = document.getElementById('message').value.trim();
            const count = document.getElementById('count').value;
            const statusDiv = document.getElementById('status');
            
            if (!phone || !message || !count) {
                statusDiv.className = "status error";
                statusDiv.textContent = "Please fill in all fields";
                return;
            }
            
            if (isNaN(count) || count < 1) {
                statusDiv.className = "status error";
                statusDiv.textContent = "Please enter a valid number of messages";
                return;
            }
            
            // Prepare status message
            statusDiv.className = "status info";
            statusDiv.textContent = "Starting WhatsApp Web... Please wait and don't touch your mouse or keyboard.";
            
            // Send the request to the server
            fetch('/send', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({
                    phone: phone,
                    message: message,
                    count: count
                }),
            })
            .then(response => response.json())
            .then(data => {
                statusDiv.className = "status warning";
                statusDiv.textContent = "WhatsApp Web is opening. Do not touch your mouse or keyboard. The messages will be sent automatically.";
            })
            .catch((error) => {
                statusDiv.className = "status error";
                statusDiv.textContent = "Error: " + error.message;
            });
        }
    </script>
</body>
</html>
    ''')

if __name__ == '__main__':
    print("Starting WhatsApp Automation Server...")
    print("Open your browser and navigate to http://127.0.0.1:5000")
    app.run(debug=True)
