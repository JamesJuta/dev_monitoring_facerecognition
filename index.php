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
session_start();

if(isset($_POST['loginBtn'])) {
    
    $username = $_POST['username'];
    $password = $_POST['password'];

    if($username === 'user' && $password === 'password') {
        
        $faceRecognitionAppUrl = "http://localhost:5000";
        $redirectUrl = "$faceRecognitionAppUrl?username=$username";
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
