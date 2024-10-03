<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Ping Checker</title>
</head>
<body>
    <h1>Ping Checker</h1>

    <form method="GET" action="">
        <label for="ip">Enter IP Address to Ping:</label>
        <input type="text" name="ip" id="ip" required>
        <input type="submit" value="Ping">
    </form>

    <?php
    if (isset($_GET['ip'])) {
        $ip = $_GET['ip'];

        //$ip = escapeshellarg($ip);

        # Execute ping command
        $output = shell_exec("ping -c 3 $ip");

        echo "<h3>Ping result for $ip:</h3>";
        echo "<pre>$output</pre>";
    }
    ?>
</body>
</html>
