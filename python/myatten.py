import subprocess
import os, random
import mysql
import sys
import time
from time import strftime,localtime
import MySQLdb
from datetime import datetime
from unidecode import unidecode

#Function that is used to connect to our MySql database
def connect():
        # Mysql connection setup. Insert your values here
        return MySQLdb.connect(host="localhost", user="", passwd="", db="TimeCard")

#Function that will insert the card reading into the database
def insertReading(tagId,action):
        #Connect to the database
        db = connect()
        cur = db.cursor()
        #Get the current day
        currentDay = strftime("%m/%d/%Y", localtime())
        #Get the current time
        currentTime = datetime.now().strftime("%H:%M")
        #Call our insert sql command
        cur.execute("""INSERT INTO readings (tagId, day, time, action) VALUES (%s, %s, %s, %s)""",(tagId,currentDay,currentTime,action))
        #Commit the command
        db.commit()
        #Call our select sql command
        cur.execute("SELECT name,surname FROM users WHERE id = (SELECT userId FROM cards WHERE tagId=%s LIMIT 1)",(tagId))
        #Get the firt result
        row = cur.fetchone()
        #Close the database
        db.close()
        #If no name was returned
        if(row==None):
                #Return 0
                return 0
        #If we did find a matching name
        else:
                #Return the first name
                return unidecode(row[0])

#Function that will play a random mp3 from the /nfc_attendance/songs directory
#In my implementation I used 23 different Seinfeld bass rifts but having just a beep would also work
def rndmp3 ():
        #Pick the random file and set it to a variable
	randomfile = random.choice(os.listdir("/home/pi/nfc_attendance/songs/"))
	#Make the string for our CLI command and set it to a variable
	file = 'mpg123 -a hw:1,0 /home/pi/nfc_attendance/songs/'+ randomfile
	#Move to home
	os.system ('cd ~')
	#Play the mp3 file
	os.system (file)

#This class is used to determine which clock in/out the user is doing
#This can allow for custom on screen messages to the user based on which scan it is
#This is not used in this implementation because the message will always be generic, that the scan was successful
class Actions:
	incomming=1
	outcomming=2
	breakstart=3
	breakend=4
		
#Function that will read the id card format the output and return an array
def read():
        #Call our read command
        p = subprocess.Popen(["nfc-mfsetuid"], stdout=subprocess.PIPE)
        #Get the output
        output, err = p.communicate()
        #Convert the output to a string
        output = str(output)
        #Replace and split the string into a usable and consistant array
        output = output.replace('"', "")
        output = output.replace("\n ", "  y")
        output = output.replace("\n", "  y")
        output = output.split("  y")
        #Return that array
        return output

def main():
	#Our main while loop
	while True:
                #Get the current day of the week and date
                currentDay = strftime("%A - %B %d, %Y", localtime())
                #Open our date.txt file
                f = open('/home/pi/nfc_attendance/web/date.txt', 'w')
                #Update the text in this file
		f.write(currentDay)
		#Close the file
		f.close()
		#Call our read function and set the results to output
		output = read()
		#Check if we read the card successfully
	       	if(output[2][0] == "R"):
                        #Get and set the card id
        	        cardId = output[13].split(": ")[1]
        	        #Check to see if the id is valid
			if(' ' not in cardId and '0000' not in cardId):
                                #Insert the reading into our database and get back the users name
				name = insertReading(cardId,Actions.incomming)
				#Check if the name retrieved was successful
				if(name is not 0):
                                        #Open our message.txt file
                                        f = open('/home/pi/nfc_attendance/web/message.txt','w')
                                        #Update the text in the file
					f.write(name + ': Scan successful.')
					#Close the file
					f.close()
					#Play our random mp3
					song.rndmp3()
					#Sleep for 3 seconds so the user does not accidentally double scan and also has time to read the message
					time.sleep(3)
				#If the read worked but the name was not in the database
				else:
                                        #Open our message.txt file
					f = open('/home/pi/nfc_attendance/web/message.txt','w')
					#Write the error to the file so it displays on the screen
					f.write('That is not a valid ID card.')
					#Close the file
					f.close()
					#Delay 3 seconds so the user has time to read the message
					time.sleep(3)
			#If it is having a hard tile reading the card
			else:
                                #Open the message.txt file
				f = open('/home/pi/nfc_attendance/web/message.txt','w')
				#Write the message that we are trying to read the card
                                f.write('Scanning...')
                                #Close the file
                                f.close()
                #If there was no card read successfully or at all
		else:
                        #Open the message.txt file
			f = open('/home/pi/nfc_attendance/web/message.txt', 'w')
			#Update the text in the file that we want the user to scan their id
			f.write('Please scan your ID.')
			#Close the file
			f.close()
			#Delay for only 1 second so it can try reading again sooner
			time.sleep(1)

main()
