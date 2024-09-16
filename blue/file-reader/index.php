<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>File Reader</title>
</head>
<body>
    <h1>File Reader</h1>

    <p>Click on the links below to read the content of the files:</p>
    <ul>
        <li><a href="?file=file1.txt">Read file1.txt</a></li>
        <li><a href="?file=file2.txt">Read file2.txt</a></li>
        <li><a href="?file=file3.txt">Read file3.txt</a></li>
    </ul>

    <?php
    if (isset($_GET['file'])) {
        $file = $_GET['file'];

        // 読み込むファイル名を制限
        $filepath = __DIR__ . '/files/' . $file;

        // 読み込むファイル名を制限
        // if (!preg_match('/^file[1-3]\.txt$/', $file)) {
        //     echo "<p style='color:red;'>Invalid file name.</p>";
        //     exit;
        // }

        // ファイルが存在するかチェックして読み込み
        if (file_exists($filepath)) {
            $content = file_get_contents($filepath);
            echo "<h3>Content of $file:</h3>";
            echo "<pre>" . htmlspecialchars($content) . "</pre>";
        } else {
            echo "<p style='color:red;'>File does not exist.</p>";
        }
    }
    ?>
</body>
</html>
