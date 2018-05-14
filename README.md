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
>sudo apt-get update

>sudo apt-get upgrade

>sudo rpi-update

We will now need to install Chromium so we can utilize it's kiosk mode. Use the following command.
>sudo apt-get install chromium

Next, we can start disabling the screensaver and the energy saving settings so our screen does not go blank when not used for 5 minutes. To do this, we will need to edit the file '/etc/xdg/lxsession/LXDE-pi/autostart' which we can do with the following command.
>sudo nano /etc/xdg/lxsession/LXDE-pi/autostart

In order to disable the screen saver we need to comment out the '@xscreensaver -no-splash' line by adding a # at the beginning and making it look like:
>#@xscreensaver -no-splash

Now, in order to disable the power management we need to add the following lines underneath that line we just commented out.
>@xset s off

>@xset -dpms

>@xset s noblank

Next, we need to make sure we prevent error messages that can occur from an improper power cycle. In the same file, add another line that matches the following.
>@sed -i 's/"exited_cleanly": false/"exited_cleanly": true/' ~/.config/chromium/Default/Preferences

Finally, at the bottom of this file we can add the command that will open Chromium into kiosk mode on bootup.
>@chromium --noerrdialogs --disable-translate --kiosk http://localhost/web/ --incognito

Now let's make sure that our Pi will bootup in desktop mode by typing the following command.
>sudo raspi-config

Here we can specify that we want to desktop every time.

# Setting up the UI
First, let's create a new directory to hold the webpages for our UI. This will have the same name as our kiosk command above.
>sudo mkdir /home/pi/web
