<?php
if (isset($_POST['direction']))
{
    $str_in=$_POST['direction'];
    $file = fopen("date.txt","w")or die("Unable to write file !");
    $str_in = mb_convert_encoding($str_in, 'HTML-ENTITIES', "UTF-8");
    fwrite($file,$str_in);
    fclose($file);
}
    $myfile = fopen("date.txt", "r") or die("Unable to open file!");
    $read=fread($myfile,filesize("date.txt"));
    fclose($myfile);
    echo $read;
?>

