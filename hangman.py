import re
#try:
import os
import sys
import time
import json
import socket
import random
import ctypes
#import colorama
import datetime
import subprocess 
#import PIL
# import pyautogui
# import cryptography
import sqlite3
from threading import Thread
from datetime import datetime
# except ModuleNotFoundError:
# 	path = "C:\\Users\\israe\\Documents\\Evil_Tech\\requirements.txt"
# 	os.system(f"pip install -r {path}")
	

current_dir = os.getcwd()

with open(f"C:\\Users\\israe\\Documents\\Evil_Tech\\hangman_cli\\words.txt", "r") as file:
	words = file.readlines()

with open(f"C:\\Users\\israe\\Documents\\Evil_Tech\\hangman_cli\\database.json") as f:
	contents = json.load(f)


words = [word.strip("\n") for word in words]
secret_word = random.choice(words)
rep = [secret.replace(secret, "*") for secret in secret_word]
sec_wrds = [i.lower() for i in secret_word]
length = len(sec_wrds)
wrong_guesses = []
correct = list(rep)
colors = [5, 6, 7, 9, 4, 2, 3, 1, "c", "e", "b"]
colors_choice = random.choice(colors)
invalid = []
qx = ["exit", "quit"]
swallow_graph = []
file_name = os.path.basename(__file__)
game_username = []
usernames = []

ADDR = "<your_ip_address>"
PORT = 4444



logo = """
		 _   _    _    _   _  ____ __  __    _    _   _ 
		| | | |  / \  | \ | |/ ___|  \/  |  / \  | \ | |
		| |_| | / _ \ |  \| | |  _| |\/| | / _ \ |  \| |
		|  _  |/ ___ \| |\  | |_| | |  | |/ ___ \| |\  |
		|_| |_/_/   \_\_| \_|\____|_|  |_/_/   \_\_| \_|
                                                
"""



def swallow_board():

	body = ["O", "|", "/", "\\"]  
	"""
		O
	   /|\
	  / | \
	   / \
	  /   \
	"""
	swallow = ["_________________","|\t\t|",
		   	"|\t\t|",
			"|",
			"|",
			"|",
			"|",
			"|",
			"|",
			"|",
			"|\n"]
	

	if wrong_guesses:
		# Every time we add an character on the wrong_guess we will print one of the parts of the body on the body list variable
		# I have to make sure I don't exceed the the wrong_guess list, so how am I going to make this work
		# the nackle of the swallow
		nackle = f"|\t\t{body[1]}"

		# left arm of the swallow graph
		left_arm = f"|\t       {body[2]}{body[1]}"
		left1_arm =  f"|\t      {body[2]} {body[1]}"
		
		# right arm of the swallow graph
		right_arm = f"|\t       {body[2]}{body[1]}{body[-1]}"
		right1_arm = f"|\t      {body[2]} {body[1]} {body[-1]}"

		# left leg
		left_leg = f"|\t       {body[2]}"
		left1_leg = f"|\t      {body[2]}"
		# right leg
		right_leg = f"|\t       {body[2]} {body[-1]}"
		right1_leg = f"|\t      {body[2]}   {body[-1]}" 

		#if len(wrong_guesses) >=  
		swallow[3] = f"|\t\t{body[0]}"
		if len(wrong_guesses) >= 2:
			swallow[4] = nackle
			swallow[5] = nackle

		if len(wrong_guesses) >= 3:
			swallow[4] = left_arm
			swallow[5] = left1_arm
		
		if len(wrong_guesses) >= 4:
			swallow[4] = right_arm
			swallow[5] = right1_arm

		if len(wrong_guesses) >= 5:
			swallow[6] = left_leg
			swallow[7] = left1_leg

		if len(wrong_guesses) >= 6:
			swallow[6] = right_leg
			swallow[7] = right1_leg

		# if len(wrong_guesses) == 4:
		# 	swallow[6] = right_arm

	for n, i in enumerate(swallow):
		print(f"{i}")
		


def clear_up():
	# this function is going to clean up either the correct or wrong guesss when user press y to restart
	
	wrong_guesses.clear()
	rep.clear()
	
	
# I think the only way to solve this problem is by sperating the code into functions
def secret_code(guess):
	index = []
	if guess in sec_wrds:
		for idx in range(len(sec_wrds)):
			# every time a user makes the right guess we get the position of the letter in the secret_word
			if sec_wrds[idx] == guess: # let's get a position of each word in the sec_wrds list
				rep[idx] = guess
	secs = "".join(i for i in rep)
	pr = f"\nSecret Word: {secs}"
	

	# Next problem that must be solved, instead of placing two equal words at the same time
	# we will place the first and then the last item.

def wrong_guess(guess):
	if guess not in sec_wrds:
		
		wrong_guesses.append(guess)	
	
	wrds = ", ".join(words for words in wrong_guesses)
	wrong  = f"Wrong guesses: {wrds}"
	return wrong


def invalid_guess(guess, chance):
	inv = [";", ":", "'", '"', "/", "?",
		  "!", "~", "`", "#", "$", "^", "&", "()", "-", "_", "=", "+",
		  "|", "<>", ",", ".", "@"]
	
	guess_length = [x for x in guess]
	if guess not in sec_wrds:
		
		if guess in qx:
			print("Quitting...")
			time.sleep(2)
			sys.exit()
		
		elif len(guess_length) > 1:
			# Every time a user times an invalid words we wont count we will pass
			chance+=1
			invalid.append(guess)
			print("[!] Invalid guess")
			time.sleep(1)
		
		elif guess.isdigit():
			invalid.append(guess)
			print("[!] Invalid guess")
			time.sleep(1)
		
		elif guess in inv:
			invalid.append(guess)
			print("[!] Invalid guess")
			time.sleep(1)

		# let's make sure that no two same letters must be added to the wrong_guesses
		elif guess in wrong_guesses:
			idx = wrong_guesses.index(guess)
			wrong_guesses[idx] = guess
			#wrong_guesses.append(guess)

			print("You've already typed the letter {}".format(guess))
			time.sleep(1)

		elif len(guess_length) == 1:
			wrong_guess(guess)

def correct_guess(guess):
	# Let's add each word to its current position in the list
	if guess in sec_wrds:
		for x in range(len(correct)):
			if sec_wrds[x] == guess: # interate in the list and if guess is in the list
				correct[x] = guess # then append that guess or that letter and x here becomes the position of the list
				
		if "*" not in correct:
			os.system("cls" if os.name == "nt" else "clear")
			print(logo)
			print(f"Secret Word: {secret_word}")
			print(wrong_guess(guess))
			print("You won!!! :)".upper())
			restart()
			

def hangman_display():
	chance = len(sec_wrds)
	
	try:
		while True:
			os.system(f"color {colors_choice}")
			chance -= 1
			os.system("cls" if os.name == "nt" else "clear")
			#time.sleep(.1)
			
			print(logo)
			

			swallow_board()

			s = "".join(wd for wd in rep)
			w = ", ".join(ws for ws in wrong_guesses)
			 
	
			#print(secret_word)
			print(f"Username: {game_username[0]}")
			print(f"Secret Word: {s}")
			print(f"Wrong guesses: {w}")
			
			
			guess = input("\nGuess a letter\n>>> ").lower()
			
			invalid_guess(guess, chance)
			secret_code(guess)
			correct_guess(guess)
			
			
			# we have to modify this code below because we won't use chance anymore
			if len(wrong_guesses) >= 6:
				rpx = "".join(y for y in correct)
				os.system("cls" if os.name == "nt" else "clear")
				print(logo)
				swallow_board()
				print(f"Secret word: {secret_word}")
				print(f"Your correct guesses: {rpx}")
				print(wrong_guess(guess))
				print("You lost ):")
				break
			
			if guess in qx:
				time.sleep(2)
				print("\nQuitting...")
				sys.exit()
				
			else:
				pass

	except KeyboardInterrupt:
		print("\nQuitting...")
		sys.exit()

# How am I going to solve this problem.

def restart():
	display = hangman_display()

	user_input = input("\nDo you want to restart (Y/n):\n>>> ")

	if user_input.upper() == "Y":
		path = os.getcwd()
		clear_up()
		# for i in os.listdir(path): 
		# 	if "hangman.py" in i:
		file = os.path.basename(__file__)
		current_path = "/".join((path, file))
		
		hangman_display()
		#os.system(f"python {current_path}" if os.name == "nt" else f"python3 {current_path}")
				#sys.exit()
	
	elif user_input == "n":
		print(f"user admin is loging out...")
		print("Quitting...")
		time.sleep(2)
		sys.exit()
	else:
		print("[!] Invalid input")
		restart()




"""---------------------------------Login and Registrations-------------------------------------------"""

temporary = []
class Register:
		
	def __init__(self, full_name, username, email, age, gender, password):
		self.full_name = full_name
		self.username = username
		self.email = email
		self.age = int(age)
		self.gender = gender
		self.password = password



	def register(self):  


		users = "database"
		databases = {}

		if len(self.full_name.split(" ")) < 2:
			print("Full name must be 2 names not one")
			sys.exit()
		
		if not self.email.endswith("@gmail.com"):
				print("Invalid email")
				sys.exit()

		if len(self.password) < 6:
				print("The length of the password must be greater than 6")
				sys.exit()

		if self.gender not in ["male", "female"]:
				print("Invalid options")
				sys.exit()


		data = {
					
				users: [
						{
							"Full name:": self.full_name,
							"Username:":  self.username,
							"Email:": self.email,
							"Age:": self.age,
							"Gender:": self.gender,
							"Password:": self.password
						}
				]
			}
		# temporary login details being added to a list
		for i in data["database"]:
        
			for j in i.values(): 
				temporary.append(j)

		if os.stat("C:\\Users\\israe\\Documents\\Evil_Tech\\hangman_cli\\database.json").st_size == 0:
				with open("Login/database.json", "w") as f:
					json.dump(data, f, indent=2)
				
		
		else:

			with open("C:\\Users\\israe\\Documents\\Evil_Tech\\hangman_cli\\database.json", "+r") as files:
				contents = json.load(files)

				for i in data[users]:
					databases.update(i)

				contents['database'].append(databases)

				files.seek(0) # ?

				json.dump(contents, files, indent=2)

				print("Creating the account....")
				
				time.sleep(3)

				os.system("cls" if os.name == "nt" else "clear")
				print(logo)
				print("-" * 50)
				
				try:
					username = str(input("Username: ")).lower()
					password = input("Password: ")

					

					log = Login(username, password)
					log.loged_in()

					game_username.append(username)

				except KeyboardInterrupt:
					print("\nQuiting...")
					time.sleep(1)
				#os.system(f"python {file_name}" if os.name == "nt" else f"python3 {file_name}")
                
            
class Login:
		
	def __init__(self, username, password):
			self.username = username
			self.password = password

	def loged_in(self):

			
		info = []
		with open("C:\\Users\\israe\\Documents\\Evil_Tech\\hangman_cli\\database.json", "r") as file:
				content = json.load(file)
		
		for i in content['database']:
			for x in i.values():
				info.append(x)

		if self.username in info or self.username in temporary and self.password in info or self.password in temporary:
			usernames.append(self.username)
			print("Logged in sucessfully :)")
			time.sleep(1)

			try:
				#play = restart()
				threads = Thread(target=restart)
				threads.start()
				
				
			except KeyboardInterrupt:
				print("Quitting...")
				sys.exit()

		else:
		
			print(f"the account {self.username} was not found ):")
			create = str(input("Do you want to create an account [y/n]: ")).lower()

			if create == "y":
				os.system("cls" if os.name == "nt" else "clear")
				print(logo)
				print("-" * 50)
				print("[!] warning make sure your email ends with @gmail.com and your password length must be greater than 6")
				reg = Register(str(input("Full name: ")), str(input("Username: ").lower()), str(input("Email: ")), int(input("Age: ")), str(input("Gender: ")), input("Password: "))
				reg.register()

			elif create == "n":
				print("Quiting...")
				time.sleep(2)
				sys.exit()
			
			else: 
				print("[!] invalid input")
				sys.exit()
def handle_users():
	pass

"""---------------------------------Client-------------------------------------------"""

# First the user must login before he gets added to the server.
def client():
	
	client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	client.connect((ADDR, PORT))

	connected = True
	
	while connected:
		
		msg = client.recv(1024).decode("utf-8")
		
		if msg == "client_name":
			client.send("admin".encode("utf-8"))
		
		if msg == "exit":
			sys.exit()

		print(logo)
		print("-" * 50)
		
		try:
			username = str(input("Username: ")).lower()
			password = input("Password: ")

			

			log = Login(username, password)
			log.loged_in()

			game_username.append(username)


		except KeyboardInterrupt:
			print("\nQuiting...")
			time.sleep(1)

	client.close()



if __name__ == "__main__":

	
	os.system("cls" if os.name == "nt" else "clear")
	print("[+] hangman client is starting....")
	time.sleep(2)

	try:
		cl = client()
		#display = hangman_display()
		
			#print("[!] server is down ")
	except Exception:
		print("[-] hangman server it's currently down!")
		sys.exit()


	

# Project completed in 22 days.
