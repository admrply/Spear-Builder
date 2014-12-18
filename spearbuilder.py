#################
# START IMPORTS #
#################
from termcolor import colored
# For coloured terminal text
import time
# For terminal display timings (including loading bar)
import re
# For email and input validation (regex: regular expression)
import twitter
# Obvious.
from TwitterAPI import TwitterAPI
# Less obvious... This is a separate wrapper for the REST and Streaming APIs
import os
# For clearing screen/building files/directories
import shutil
import fileinput
# For copying template file into the spear and modifying placeholder texts ($WORDS)
import sys
import threading
# For multithreading for loading bars for automated pulling of random targetable users


##############################
# START OPENING ASCII HEADER #
##############################
os.system('cls' if os.name == 'nt' else 'clear')
# Clears the screen before starting the program.
print colored('***********************************************************','white')
print colored('*       ______   ______   ______   ______   ______        *','white')
print colored('*      |  ____| |  __  | |  ____| |  __  | |  __  |       *','white')
print colored('*      | |____  | |__| | | |__    | |__| | | |__| |       *','white')
print colored('*      |_____ | |  ____| |  __|   |  __  | |  _  /        *','white')
print colored('*       _____ | | |      | |____  | |  | | | | \ \        *','white')
print colored('*      |______| |_|      |______| |_|  |_| |_|  \_\       *','white')
print colored('*                                                         *','white')
print colored('*         B U I L D E R    //   Proof Of Concept          *','white')
print colored('*                                                         *','white')
print colored('***********************************************************','white')
print ""
print colored('Python Script written by Adam Rapley (Red Dot Innovations)','white')
print colored('@AutomatedRandom // me [at] adamrapley [dot] com','white')
print ""
print colored('***********************************************************\n','white')


################################
# GLOBAL VARIABLE DECLARATIONS #
################################
global email
global targetHandle
global account
global name
global picture
global url


############################
# BEGIN METHOD DEFINITIONS #
############################
def inputDetails():
# Method for checking valid data entry for the email and username input later on
	while True:
		global email
		email = raw_input("\nType the target's email address: ")
		if len(email) > 6:
			if re.match("^.+\\@(\\[?)[a-zA-Z0-9\\-\\.]+\\.([a-zA-Z]{2,3}|[0-9]{1,3})(\\]?)$", email) != None:
			# If email follows proper format, continue
				break
			else:
				print colored('Error: Email address is invalid, please try again.', 'red', attrs=['bold'])
		else:
			print colored('Error: Email address is too short, please try again.', 'red', attrs=['bold'])

	while True:
		global targetHandle
		targetHandle = raw_input("Type target's Twitter handle: @")
		# Creates and stores global Twitter handle. Global to be instantiated in accountPopulation
		if len(targetHandle) < 16:
			# If Twitter handle is valid, continue
			break
		print colored('Error: Twitter handle is too long, please check and try again.', 'red', attrs=['bold'])

	if menu == "2":
	# If the semi-automated option is selected
		global account
		account = api.GetUser(screen_name=targetHandle)
		# Populates the account variable with the details from the previously specified account
		global name
		name = account.name
		global picture
		picture = account.profile_image_url
		global url
		url = account.url
		# Populates global vars with Twitter parameters

	elif menu == "3":
	# Fully manual option
		# global name
		name = raw_input("Enter the target's name: ")
		print colored('[Optional]: Profile image URL', 'yellow')
		print colored('Note: this makes the spear more convincing as it contains more specific information related to the user.', 'yellow')
		print colored('Hit enter to skip', 'yellow')
		global picture
		picture = raw_input("http://")
		picture = str("http://"+picture)
		# Gets user inputted URL for the profile image of the user
		global url
		url = str("http://www.twitter.com/"+targetHandle)
		# Grabs URL from twitterHandle inputted before
	accountPopulation()
	return

def accountPopulation():
	checkOutput = str("\n   User name: " + name +
	                  "\n   Email address: " + email +
										"\n   Twitter handle: @" + targetHandle +"\n")
	print colored(checkOutput, 'yellow', attrs=['bold'])
# print account.profile_image_url
	print "Is this correct? (Y)es, (N)o.\n"
	while True:
		global detailsCheck
		detailsCheck = raw_input(" >>> ")
		if detailsCheck in ["Y","y","N","n"]:
			break
		print colored('\nError: Please choose a valid menu option!\n', 'red', attrs=['bold'])
# Verifies and returns if user approves input
	return

def modifySpear():
	for line in destinationTitle:
		with open(destinationTitle, "wt") as newSpear:
			with open("email.emlx", "rt") as template:
				for line in template:
					newSpear.write(line.replace('$NAME',name).replace('$EMAIL',email).replace('$USRNAME','@'+targetHandle).replace('$PROFILEIMG',picture).replace('$PROFILEURL',url))
					# Replaces the template values with inputted variables
	return

def createFilepath():
	if not os.path.exists('spears'):
		os.makedirs('spears')
	global destinationTitle
	destinationTitle = str("spears/"+name+" - Generated Spear.emlx")
	open(destinationTitle, 'a').close()
	shutil.copy('email.emlx', destinationTitle)
	modifySpear()

def genCon():
	generationConfirmation = str("\n   Email successfully created in:\n     << "+destinationTitle+" >>\n")
	print colored(generationConfirmation, 'green', attrs=['bold'])
	time.sleep(1)
	print "----------------\n"


################################
# BEGIN THREADED LOADING CLASS #
################################
class progress_bar_loading(threading.Thread):
  def run(self):
    global stop
    global kill
    print '\nPlease wait. Press q to quit and return to the menu\nSharpening spears...  ',
    sys.stdout.flush()
    i = 0
    while stop != True:
      if (i%4) == 0:
        sys.stdout.write('\b/')
      elif (i%4) == 1:
        sys.stdout.write('\b-')
      elif (i%4) == 2:
        sys.stdout.write('\b\\')
      elif (i%4) == 3:
        sys.stdout.write('\b|')

      sys.stdout.flush()
      time.sleep(0.2)
      i+=1

    if kill == True:
      print '\b\b\b\bSpear sharpening aborted!'
    else:
      print '\b\b Done!'


######################
# BEGIN MAIN PROGRAM #
######################
api = twitter.Api(consumer_key='Eyr58CtIG2WUUc4hCrnXeg',
									consumer_secret='nyHA5OaqKDbcrcdA9fKrdf1vEfNmVTtcx6GvmLVsTfU',
									access_token_key='86166020-VM2e2UOAsVgeOJE78RbOxITKlatoVyi8Z5hXknGQj',
									access_token_secret='MbbPss7d7g3a7eBx10NnyVPOJGbFQo572DEXvFhwVjIVG')
streamingapi = TwitterAPI('Eyr58CtIG2WUUc4hCrnXeg',
													'nyHA5OaqKDbcrcdA9fKrdf1vEfNmVTtcx6GvmLVsTfU',
													'86166020-VM2e2UOAsVgeOJE78RbOxITKlatoVyi8Z5hXknGQj',
													'MbbPss7d7g3a7eBx10NnyVPOJGbFQo572DEXvFhwVjIVG')
user = twitter.User
# Instatiates the Twitter APIs and creates a User class for calling user specific details

while True:
	print "Please choose attack vector:\n1. Automated Random\n2. Targeted\n3. Manual (Without internet connection)\n4. Exit\n"
	while True:
		menu = raw_input(" >>> ")
		if menu in ["1","2","3","4"]:
			break
		print colored('\nError: Please choose a valid menu option!\n', 'red', attrs=['bold'])

	if menu == "1":
		kill = False
		stop = False
		p = progress_bar_loading()
		p.start()
		try:
			r = streamingapi.request('statuses/filter')
			for item in r:
				print(item['text'] if 'text' in item else item)
			# stop = True
			time.sleep(8)
			print "\n----------------\n"
		except KeyboardInterrupt or EOFError:
			kill = True
			stop = True

	if menu == "2":
		while True:
			inputDetails()
			if detailsCheck in ["Y","y"]:
				createFilepath()
				break
		genCon()

	if menu == "3":
		while True:
			inputDetails()
			if detailsCheck in ["Y","y"]:
				createFilepath()
				break
		genCon()

	if menu == "4":
		os.system('cls' if os.name == 'nt' else 'clear')
		exit()

# ----------------------------
#            TO-DO
# ----------------------------
#
# Fix regex for email to allow TLDs greater than 3 characters.
# Add option 1, checks for email addresses in tweet user's descriptions for email crafting.
#
# ----------------------------
