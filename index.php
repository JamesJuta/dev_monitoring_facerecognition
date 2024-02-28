<?php
// session_start();
// if(isset($_POST['loginBtn'])) {
//     $username = $_POST['username'];
//     $password = $_POST['password'];

//     if($username === 'user' && $password === 'password') {

//         $_SESSION['username'] = $username;
//         $_SESSION['password'] = $password;


//         echo "Session variables set successfully. Username: $username, Password: $password";


//         $faceRecognitionAppUrl = "http://localhost:5000";
//         header("Location: $faceRecognitionAppUrl");
//         exit();
//     } else {

//         echo "Invalid username or password. Please try again.";
//     }
// }
?>


<?php
// session_start();

// if(isset($_POST['loginBtn'])) {
    
//     $username = $_POST['username'];
//     $password = $_POST['password'];

//     if($username === 'user' && $password === 'password') {
        
//         $faceRecognitionAppUrl = "http://localhost:5000";
//         $redirectUrl = "$faceRecognitionAppUrl?username=$username";
//         header("Location: $redirectUrl");
//         exit();
//     } else {
        
//         echo "Invalid username or password. Please try again.";
//     }
// }
?>


<?php
// session_start();

// if(isset($_POST['loginBtn'])) {
//     $username = $_POST['username'];
//     $password = $_POST['password'];

//     if($username === 'user' && $password === 'password') {
 
//         $data = $username;

//         $encryptionKey = "g5K8Ht+6oCOOG8IJnZIoR59Doa8shfBjqRvvhb9yIGU=";
//         $encryptedData = openssl_encrypt($data, 'aes-256-cbc', $encryptionKey, 0, $encryptionKey);

    
//         $faceRecognitionAppUrl = "http://localhost:5000";
//         $redirectUrl = "$faceRecognitionAppUrl?data=$encryptedData";
//         header("Location: $redirectUrl");
//         exit();
//     } else {
//         echo "Invalid username or password. Please try again.";
//     }
// }
?>

<?php
session_start();

if(isset($_POST['loginBtn'])) {
    $username = $_POST['username'];
    $password = $_POST['password'];

    if($username === 'user' && $password === 'password') {
        // Construct the data to be encrypted (the username)
        $data = $username;

        // Generate a random initialization vector (IV)
        $iv = openssl_random_pseudo_bytes(openssl_cipher_iv_length('aes-256-cbc'));

        // Encrypt the data with PKCS7 padding
        $encryptionKey = "g5K8Ht+6oCOOG8IJnZIoR59Doa8shfBjqRvvhb9yIGU="; // Should be a secure key
        $encryptedData = openssl_encrypt($data, 'aes-256-cbc', $encryptionKey, OPENSSL_RAW_DATA, $iv);

        // Convert IV to hexadecimal string for safe inclusion in URL
        $hexIV = bin2hex($iv);

        // Construct the redirect URL with the encrypted data and IV
        $encodedEncryptedData = base64_encode($encryptedData); // Encode the encrypted data for URL safety
        $redirectUrl = "http://localhost:5000?data=$encodedEncryptedData&iv=$hexIV";
        header("Location: $redirectUrl");
        exit();
    } else {
        echo "Invalid username or password. Please try again.";
    }
}
?>





<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Login</title>
</head>
<body>
    <h2>Login</h2>
    <form method="post">
        <label for="username">Username:</label><br>
        <input type="text" id="username" name="username" required><br><br>
        <label for="password">Password:</label><br>
        <input type="password" id="password" name="password" required><br><br>
        <button type="submit" name="loginBtn">Login</button>
    </form>
</body>
</html>
