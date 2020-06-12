<?php
session_start();
include("connection.php");
?>
<title>LOGIN</title>
<link rel="stylesheet" href="stylein.css">
<nav>
     <a href="http://www.niet.co.in" ><img src="niet_logo.png" align="right" height=18%></a>
     <a href="index.html" class="menu-link">Home</a></br>
     <a href="index.html#about" class="menu-link">About</a></br>
     <a href="index.html#contact" class="menu-link">Contact</a></br>
     <a href="member.html" class="menu-link">Signup</a></br>
  </nav>     
  <h1 align="center">LOGIN</h1> 
  <center>
     <div class="form">                  
<form action="" method="post" >
<input type="text" name="user" value="" required placeholder="Please enter username"/><br><br>
<input type="password" name="pass" value="" required placeholder="Please enter password"/><br><br>
<input type="submit" name="submit" value="Login" />   
<input type="reset" name="">   
</form>     
</div>

<?php
if(isset($_POST['submit']))
{
    $user = $_POST['user'];
    $pwd = $_POST['pass'];
    $query = "SELECT * FROM USER WHERE EMAIL='$user' && PASSWORD ='$pwd' ";
   
    $data = mysqli_query($conn, $query);
    $total = mysqli_num_rows($data);
    if ($total==1)
    {
        #echo("success");
        $_SESSION['user']=$user;
        header('location:enter_url.php');
    }
    else
    {
        echo("<p>Wrong Credentials<p>");
    }
}
?>
</center>