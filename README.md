# Getting Started
Hardware I used:

- Raspberry Pi 3 Model B
- NFC Module (I used 'SunFounder PN532 NFC RFID Module Kit')
- 7 Inch Touch Screen (Any screen can be used)
- USB Speaker
- NFC Cards (13.56MHz to match the Module)
- Project box to hold the hardware in place
- Jumpers for I/O pins

# Prepare the Pi
The first thing we need to do is install Raspbian.

Once that is installed we need to update the Pi by using the following commands.
```
sudo apt-get update
sudo apt-get upgrade
sudo rpi-update
```
# Install a Web Server
We need to install a webserver that will support PHP and MySql. I used nginx.
Install nginx by using the following command.
```
sudo apt-get install nginx
```
We will now need to create a folder for the webserver with the following command.
```
sudo mkdir /var/www
```
Now we will need to edit the configuration file. Open this file with the following command.
```
sudo nano /etc/nginx/sites-available/default
```
Once this file is open we need to change it to look like the following
```
server {
        #listen   80; ## listen for ipv4; this line is default and implied
        #listen   [::]:80 default_server ipv6only=on; ## listen for ipv6
        listen 80;
        server_name $domain_name;
        root /var/www;
        index index.html index.htm;
        access_log /var/log/nginx/access.log;
        error_log /var/log/nginx/error.log; 
 
        location ~\.php$ {
                fastcgi_pass unix:/var/run/php5-fpm.sock;
                fastcgi_split_path_info ^(.+\.php)(/.*)$;
                fastcgi_index index.php;
                fastcgi_param SCRIPT_FILENAME $document_root$fastcgi_script_name;
                fastcgi_param HTTPS off;
                try_files $uri =404;
                include fastcgi_params;
        } 
 
        # Make site accessible from http://localhost/
        server_name localhost;
```

# Install Chromium
We will now need to install Chromium so we can utilize it's kiosk mode. Use the following command.
```
sudo apt-get install chromium
```
# Configure Autostart
Next, we can start disabling the screensaver and the energy saving settings so our screen does not go blank when not used for 5 minutes. To do this, we will need to edit the file '/home/pi/.config/lxsession/LXDE-pi/autostart' which we can do with the following command.
```
sudo nano /home/pi/.config/lxsession/LXDE-pi/autostart
```
In order to disable the screen saver we need to comment out the '@xscreensaver -no-splash' line by adding a # at the beginning and making it look like:
```
#@xscreensaver -no-splash
```
Now, in order to disable the power management we need to add the following lines underneath that line we just commented out.
```
@xset s off
@xset -dpms
@xset s noblank
```
Next, we need to make sure we prevent error messages that can occur from an improper power cycle. In the same file, add another line that matches the following.
```
@sed -i 's/"exited_cleanly": false/"exited_cleanly": true/' ~/.config/chromium/Default/Preferences
```
Finally, at the bottom of this file we can add the command that will open Chromium into kiosk mode on bootup.
```
@chromium-browser --noerrdialogs --disable-translate --kiosk http://localhost/nfc_attendance/web/index.php --incognito
```
Now let's make sure that our Pi will bootup in desktop mode by typing the following command.
```
sudo raspi-config
```
Here we can specify that we want to desktop every time.

# Setting up the UI
First, let's create a new directory to hold the webpages for our UI. This will have the same name as our kiosk command above.
```
sudo mkdir /home/pi/web
```
In this directory we will need to add file
