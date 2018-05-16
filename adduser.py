import subprocess
import MySQLdb
import sys
import time
from unidecode import unidecode

#Function that is used to connect to our MySql Database
def connect():
    # Mysql connection setup. Insert your values here
    return MySQLdb.connect(host="localhost", user="", passwd="", db="TimeCard")

#Function that is called in order to read the card and clean up the output.
def read():
    #Read the users ID card
    p = subprocess.Popen(["nfc-mfsetuid"], stdout=subprocess.PIPE)
    output, err = p.communicate()
    #Convert the output into a string
    output = str(output)
    #Replace character and split until we have a clean array of strings
    output = output.replace('"', "")
    output = output.replace("\n ", "  y")
    output = output.replace("\n", "  y")
    output = output.split("  y")
    #Return that array
    return output

#Function that will insert a new user into the database
def addUser(name, surname):
    #Connect to the database
    db = connect()
    cur = db.cursor()
    #Run the insert command for the user name
    cur.execute("""INSERT INTO users (name, surname, active) VALUES (%s, %s, %s)""",(name, surname, "1"))
    #Commit the command
    db.commit()
    #Close the database
    db.close()

#Function that will insert a new card into the database
def addCard(cardId, name, surname):
    #Connect to the database
    db = connect()
    cur = db.cursor()
    #Select the userId from the database based on the name
    cur.execute("SELECT id FROM users WHERE name=%s AND surname=%s",(name, surname))
    #Fetch the results
    row = cur.fetchone();
    #Print the userId
    print(row[0])
    #Insert the userId and tagId into the cards database
    cur.execute("INSERT INTO cards (userId, tagID) VALUES (%s, %s)", (row[0], cardId))
    #Commit the command
    db.commit()
    #Close the database
    db.close()

#Our Main function
def main():
    #Get the first name of the new user
    name = raw_input("What is the first name of the new user: ")
    #Get the last name of the new user
    surname = raw_input("What is the last name of the new user: ")
    #Print out the name
    print(name, surname)
    #Add the user to the database
    addUser(name, surname)
    #Promt the user to scan the new card
    print("Scan the card now.")
    #Set readSuccess to false
    readSuccess = False
    #While we failed to read properly
    while readSuccess == False:
        #Call read and set the returned array to output
        output = read()
        #If it was read successfully
        if(output[2][0] == "R"):
            #Set cardId to what was read from the card
            cardId = output[13].split(": ")[1]
            #If the read was valid and does not have a space or 0000 in it
            if(' ' not in cardId and '0000' not in cardId):
                #Set readSuccess to True
                readSuccess = True
                #Print carId
                print(cardId)
                #Add the card to the database
                addCard(cardId, name, surname)
                #Added sleep so user has time to remove the card after a successful read
                time.sleep(3)
                

main()







	
