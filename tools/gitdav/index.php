<?php

$BASE_URI="/index.php/";
if(!file_exists("SabreDAV"))
{
    if(@$_POST["install"])
    {
        echo "<pre>";
        system("wget https://github.com/fruux/sabre-dav/releases/download/1.8.10/sabredav-1.8.10.zip");
        system("unzip sabredav-1.8.10.zip");
        system("rm sabredav-1.8.10.zip");
        system("mkdir -p public && cd public && git init && git update-server-info");
        system("mkdir -p data ");
        echo "</pre>";
    }
    else
    {
        ?>
        <h1>gitDAV</h1>
        it looks like it's not installed.
        <form method="post">
            <input type=submit name="install" value="Install"></input>
        </form>
        <?php
        die();
    }
}
if(strpos($_SERVER['REQUEST_URI'], $BASE_URI) === FALSE)
{
    $path = "${_SERVER['HTTP_HOST']}${_SERVER['REQUEST_URI']}index.php"

    ?>
    <h1>gitDAV</h1>
    <h3>DAV access</h3>
    Your files are stored here:
    <pre>
        <?php echo $path; ?>
    </pre>
    <li> You can add it as Windows 7 drive, using <a href="http://www.onemetric.com.au/Documentation/Mounting-A-WebDAV-Share-Windows-7">this manual.</a>
    <li> Or use any of <a href="https://ru.wikipedia.org/wiki/WebDAV#WebDAV-.D0.BA.D0.BB.D0.B8.D0.B5.D0.BD.D1.82.D1.8B">these clients</a>
    <li> Or mount via davfs if You use linux.
    <h3>web access</h3>
    <li> You can use <a href="index.php/">web ui</a>.
    <h3>git access</h3>
    Your repository -- here:
    <pre>
        <?php echo "$path/.git"; ?>
    </pre>
    feel free to clone. Remember, that:
    <li> Any webdav copy is a commit made by robot. So, do <pre>git pull</pre> as often as You can
    <li> I think that this will work, but I'm not sure.
    <li> Never, NEVER DO <pre>git push --force</pre>. This may AND WILL brek everything. Better contact me and I will deal with problem manually.

    <h3>Copyright notice</h3>
    <li> It's using SabreDAV as engine. http://sabre.io
    <?php
    return ;
}

use
    Sabre\DAV;
require 'SabreDAV/vendor/autoload.php';

$rootDirectory = new DAV\FS\Directory('public');
// The server object is responsible for making sense out of the WebDAV protocol
$server = new DAV\Server($rootDirectory);

// If your server is not on your webroot, make sure the following line has the
// correct information
$server->setBaseUri("$BASE_URI");

// The lock manager is reponsible for making sure users don't overwrite
// each others changes.
$lockBackend = new DAV\Locks\Backend\File('data/locks');
$lockPlugin = new DAV\Locks\Plugin($lockBackend);
$server->addPlugin($lockPlugin);

// This ensures that we get a pretty index in the browser, but it is
// optional.
$server->addPlugin(new DAV\Browser\Plugin());


// $server->on('afterWriteContent','afterWriteContent');

// All we need to do now, is to fire up the server
$server->exec();


if($_SERVER["REQUEST_METHOD"] != "GET" )
{
    if(strpos( $_SERVER['REQUEST_URI'], ".git") === FALSE)
    {
      system("cd public && git add -A 1> /dev/null 2> /dev/null");
      $changed = $_SERVER["REQUEST_URI"];
      $changed = str_replace($BASE_URI,"",$changed);
      system("cd public && git commit -m 'Changed: $changed' 1> /dev/null 2> /dev/null");
      system("cd public && git update-server-info 1> /dev/null 2> /dev/null");
    }
    else
    {
      system("cd public && git reset --hard 1> /dev/null 2>/dev/null");
      system("cd public && git clean -fx 1>/dev/null 2> /dev/null");
    }
}

?>
