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
We need to install a web server that will support PHP and MySql. I used nginx.
Install nginx by using the following command.
```
sudo apt-get install nginx
```
We can also install the PHP packages that we need at this point with the following.
```
sudo apt-get install php7.0-fpm
```
Now we will need to edit the configuration file. Open this file with the following command.
```
sudo nano /etc/nginx/sites-available/default
```
Once this file is open we need to change it to look like the following and make sure there is only one 'root';
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
                include snippets/fastcgi-php.conf;
                fastcgi_pass unix:/var/run/php/php7.0-fpm.sock;
        } 
 
        # Make site accessible from http://localhost/
        server_name localhost;
```
Next, we will need to change a PHP initalization file, open it with this command.
```
sudo nano /etc/php/7.0/fpm/php.ini
```
We will need to find 'cgi.fix_pathinfo=0' and change it to the following. Remove the ';' if neccesary.
```
cgi.fix_pathinfo=1
```
We can now install what we need to run MySql. Use the following command.
```
sudo apt-get install mysql-server mysql-client php7.0-mysql phpmyadmin
```
This will take some time. 

During the install it will ask you what web server you are using, in this case we want to keep it blank.

It will also ask you if you would like the configure phpMyAdmin, select 'yes'.

Next, it will ask you to create and confirm a password for the database and should be finished shortly after that.

Next, we will reload these two services with the following.
```
sudo service nginx reload
sudo service php7.0-fpm reload
```
We will need to create that root folder for the web server with the following command.
```
sudo mkdir /var/www
```
Once that has completed we need to link our database interface with our web server folder with the following command.
```
sudo ln -s /usr/share/phpmyadmin /var/www/phpmyadmin
```
We should now be able to access our database from 'http://localhost/phpmyadmin/index.php' in a browser. If you do not have a browser installed, complete the next step and try again.
# Install Chromium
If it is not already installed, we will now need to install Chromium so we can utilize it's kiosk mode. Use the following command.
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
First, we will need to get our webpages onto the pi so let's copy the repo with the following commands.
```
cd ~
sudo git clone https://github.com/LucasShaffer/nfc_attendance
```
Now that we have the webpages that we are going to use let's link them with the web server's root folder with this command.
```
sudo ln -s /home/pi/nfc_attendance /var/www/
```
Now you should be able to see the UI at the 'http://localhost/nfc_attendance/web/index.php' address.

We can now reboot the pi and we should see it automatically boot to our web UI that has the date, time, and prompt to have the user scan their ID card. To exit this UI just use ALT+F4.

# Setting up the RFID reader
### This is where we will see differences in steps. Each RFID reader will have the own way to be set up but for this I will go through the steps to set up the [Sunfounder PN532](https://www.amazon.com/SunFounder-Module-Reader-Arduino-Android/dp/B01N8TWIF8).

The Sunfounder PN532 can be setup to communicate with I2C or SPI. The instruction for setting up this module can be found on their [wiki](http://wiki.sunfounder.cc/index.php?title=PN532_NFC_RFID_Module) or follow the following steps for SPI setup. 

To do this we will need to enable the SPI interface on the pi. Open the configuration tool.
```
sudo raspi-config
```
Next, select 'Interfacing Options' > 'SPI' > 'Yes' to enable. Select 'Finish' to exit.

We will now need to install some dependent packages.
```
sudo apt-get update
sudo apt-get install libusb-dev libpcsclite-dev i2c-tools
```
Now, we will download and unzip the source code package of libnfc.
```
cd ~
wget http://dl.bintray.com/nfc-tools/sources/libnfc-1.7.1.tar.bz2
tar -xf libnfc-1.7.1.tar.bz2 
```
We can now compile and install this package.
```
cd libnfc-1.7.1
./configure --prefix=/usr --sysconfdir=/etc
make
sudo make install
```
Next we need to create the configuration file for NFC communication with the following commands.
```
cd /etc
sudo mkdir nfc
sudo nano /etc/nfc/libnfc.conf
```
We will need to populate this file with the following text.
```
# Allow device auto-detection (default: true)
# Note: if this auto-detection is disabled, user has to set manually a device
# configuration using file or environment variable
allow_autoscan = true

# Allow intrusive auto-detection (default: false)
# Warning: intrusive auto-detection can seriously disturb other devices
# This option is not recommended, user should prefer to add manually his device.
allow_intrusive_scan = false

# Set log level (default: error)
# Valid log levels are (in order of verbosity): 0 (none), 1 (error), 2 (info), 3 (debug)
# Note: if you compiled with --enable-debug option, the default log level is "debug"
log_level = 1

# Manually set default device (no default)
# To set a default device, you must set both name and connstring for your device
# Note: if autoscan is enabled, default device will be the first device available in device list.
device.name = "_PN532_SPI"
device.connstring = "pn532_spi:/dev/spidev0.0:50000"
#device.name = "_PN532_I2c"
#device.connstring = "pn532_i2c:/dev/i2c-1"
```
Next, we will need to configure the hardware. On the module there are two switches, the proper settings for SPI use is as follows.

| SEL0 | SEL1 |
| --- | --- |
| L | H |

We can now connect the module to the pi. Here is the wiring.

| PN532 | Raspberry |
| --- | --- |
| 5V | 5V |
| SCK | SCKL |
| MISO | MISO |
| MOSI | MOSI |
| NSS | CE0 |

Now we need to check wether or not the SPI is open by running this command.
```
ls /dev/spidev0.*
```
We should see '/dev/spidev0.0 /dev/spidev0.1' and we can now check the module itself using the following command.
```
nfc-list
```
This should say that the pn532 device was opened. The Sunfounder wiki states that there is a known error here that may state that there is a 'TFI Mismatch'. I did not get this error.

Next, we can try and read a card. Place a card near the module and use the following command.
```
nfc-poll
```
This should return information about the card including a UID which is what we will use to identify each card.

# Setup the database
We will now need to create a database that will work with what we are trying to do. We will need to have a table for the reading, users, and the cards.

To do this we will need to start out by going to 'http://localhost/myphpadmin/index.php' and loggin in using the roto credentials that were set during the install.

Next, click on the 'New' button on the left to start a new database. We can not name it as 'TimeCard' and select 'utf8_general_ci' as the collation. If the new database is not selected, select it now.

Next, click the 'import' tab at the top of the webpage. Here, we can choose the 'mysql.sql' file from this repo in order to create the tables in database.

We should now have a new database that has a table called 'cards' which will hold information about the id cards and who they are linked with.  Also, the 'readings' table will hold all of the readings we get from the users when they clock in or out. Lastly, the 'users' table will hold the name of the user and their unique id.

We should now be able to add users to the database.

# Adding users to the database
We can add users to the database manually if you but this could cause unwanted results when trying to link a RFID card to the user.

Another option is to use the 'adduser.py' script. To do this use the following commands to install MySQLdb and unidecode then run the script.
```
sudo apt-get install python-mysqldb
sudo pip install unidecode
cd ~
sudo python nfc_attendance/python/adduser.py
```
This script will ask you to enter the first and last name of the user and then scan their new id card. This will add the user to the database as well as the card and link them to each other.

This can be repeated for each user. Once every user is in the database we can run our script that will constantly look for a user id card as well as update the UI.

# Setting up our main script
We now will need to make a script that will be constantly looking for a user to swipe their card, updating the message section of the UI, and the date section of the UI.

The script that I use is in the python folder and called myatten.py. This works for the NFC chip and cards that I picked for my project. Alterations will need to be made if your hardware differs.


