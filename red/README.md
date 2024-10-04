# Attack Scenario

## Regular Checks
Every 2 minutes, the server will be checked, and if all of the following conditions are met, 10 points will be awarded:
- A web server is running on port 80 (returns status code 200).
- The web application is functioning normally.

## Targeted Attacks
Points will be awarded for preventing the following attacks:

| Time  | Event                         | Details                                           | Points           |
|:-----|:-------------------------------|:--------------------------------------------------|:-----------------|
| 0min | Start                          |                                                   |                  |
| 10min| SSH Login to User              | Attempts to log in as `root`, `user3`, `user8`, `user10`.<br>If logged in as `root`, stop the web server. | +10 x4  |
| 15min| OS Command Injection Hint      | Following commands executed via OS command injection:<br>`pwd`, `id`, `whoami`, `cat /etc/passwd` | +10 x4           |
| 20min| Credential Leak                | `memo.txt` is leaked via OS command injection        | +50              |
| 25min| Web Page Tampering             | Web page is tampered via OS command injection                               | +50              |
| 30min| End                            |                                                   |                  |

## Vulnerability Patching

```bash
# Delete users
for i in {1..10}; do userdel -r user$i; done
# Change the root user's password
echo "root:superrootpass" | chpasswd
# Delete memo.txt
rm /var/www/html/memo.txt
# Patch OS command injection
sed -i 's|//$ip = escapeshellarg($ip);|$ip = escapeshellarg($ip);|' /var/www/html/index.php && apachectl restart
```

## OS Command Injection Vulnerability
`/var/www/html/index.php` is a web application that returns the results of the Ping command, but it contains an OS command injection vulnerability.

<img width="444" alt="Screenshot 2024-10-04 at 13 50 01" src="https://github.com/user-attachments/assets/bf2dc282-a0b3-4b0e-bae0-3cd681f7b7e5">

By sending `; {cmd}`(e.g., `; ls`) as the ip, arbitrary commands can be executed.

<img width="423" alt="Screenshot 2024-10-04 at 13 50 18" src="https://github.com/user-attachments/assets/9fc51aa8-42ab-4a88-8a9b-15afe882b02c">

To fix the vulnerability, you need to uncomment `//$ip = escapeshellarg($ip);` and ensure that the string passed to the shell command is properly escaped.

```php
<?php
  if (isset($_GET['ip'])) {
      $ip = $_GET['ip'];

      # Uncomment
      $ip = escapeshellarg($ip);
  
      # Execute ping command
      $output = shell_exec("ping -c 3 $ip");
  
      echo "<h3>Ping result for $ip:</h3>";
      echo "<pre>$output</pre>";
  }
?>
```

