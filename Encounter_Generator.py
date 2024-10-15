import json
from tkinter import *
from tkinter import messagebox

# Primary Window
class Application:

	def __init__(self, root, title, geometry):
		self.root = root

		# Full window resizing, add more columns/rows 
		# as needed for frame orginization
		# Currently: 2 Columns, 1 Rows
		self.root.columnconfigure(0, weight = 1)
		self.root.columnconfigure(1, weight = 2)
		self.root.rowconfigure(0, weight = 1)

		# Title Construction
		self.root.title(title)

		# Geometry Construction
		self.root.geometry(geometry)   # Input size (XXXXxYYYY)

		# Widget Construction
		self.create_widgets()

		# Call JSON handling method
		self.format_json()

		# Create a list to add results from the balancing math
		# and the monster_list
		self.root.result_list = []

		# Bind left click within result window to
		# set the clicked name to be the chosen result.
		# and display the chosen result in the right frame's
		# text window.
		self.root.monsterResults.bind("<ButtonRelease-1>", self.select_line, add = "+")
		self.root.monsterResults.bind("<ButtonRelease-1>", self.display_results, add = "+")

		# Mainloop Construction
		self.root.mainloop()
		
	# Widget Construction Function
	def create_widgets(self):

		# Overall Frames
		self.root.leftFrame = Frame(self.root, bg = 'red')
		self.root.rightFrame = Frame(self.root, bg = 'black')
		
		# Left Frame Widgets
		self.root.numOfPlayersLbl = Label(self.root.leftFrame, text = "Hows many players do you have?")
		self.root.playersEntry = Entry(self.root.leftFrame, width= 50)
		self.root.playerLevelLbl = Label(self.root.leftFrame, text = "What is the average level of your players?")
		self.root.playerLevelEntry = Entry(self.root.leftFrame, width = 50)
		self.root.numOfMonstersLbl = Label(self.root.leftFrame, text = "How many monsters would like for the encounter?")
		self.root.numOfMonstersEntry = Entry(self.root.leftFrame, width = 50)
		self.root.crButton = Button(self.root.leftFrame, text = "Click to calculate \nChallenge Rating", command = self.on_click)
		self.root.monsterResultsLbl = Label(self.root.leftFrame, text = "List of Monsters with appropriate challenge ratings | Click chosen monster to display it's statistics")
		self.root.monsterResults = Text(self.root.leftFrame, width=60, height = 20)

		# Right Frame Widgets
		self.root.chosenMonsterLbl = Label(self.root.rightFrame, text = "Chosen Monsters Statistics:")
		self.root.chosenMonsterInfo = Text(self.root.rightFrame, width=60, height = 20)

		# Orginization

		# Frames
		self.root.leftFrame.grid(column = 0, row = 0, sticky = "NSEW")
		self.root.rightFrame.grid(column = 1, row = 0, sticky = "NSEW")

		# Left Frame Widgets
		self.root.numOfPlayersLbl.grid(column = 0, row = 0)
		self.root.playersEntry.grid(column = 0, row = 1)
		self.root.playerLevelLbl.grid(column = 0, row  = 2)
		self.root.playerLevelEntry.grid(column = 0, row = 3)
		self.root.numOfMonstersLbl.grid(column = 0, row = 4)
		self.root.numOfMonstersEntry.grid(column = 0, row = 5)
		self.root.crButton.grid(column = 0, row = 6, sticky = "E")
		self.root.monsterResultsLbl.grid(column = 0, row = 7)
		self.root.monsterResults.grid(column = 0, row = 8)

		# Right Frame Widgets
		self.root.chosenMonsterLbl.grid(column = 0, row = 0, sticky = "S", pady = 5)
		self.root.chosenMonsterInfo.grid(column = 0, row = 1, sticky = "N", pady  = 5)


		# Variables for dynamic resizing
		# of frames/allows widgets to center
		rowNum = 0
		columnNum = 0
		
		# Left Frame resizing
		for rowNum in range(self.root.leftFrame.grid_size()[1]):
			self.root.leftFrame.rowconfigure(rowNum, weight = 1)
			rowNum += 1

		for columnNum in range(self.root.leftFrame.grid_size()[0]):
			self.root.leftFrame.columnconfigure(columnNum, weight = 1)
			columnNum += 1

		# Right Frame resizing
		for rowNum in range(self.root.rightFrame.grid_size()[1]):
			 self.root.rightFrame.rowconfigure(rowNum, weight = 1)
			 rowNum += 1

		for columnNum in range(self.root.rightFrame.grid_size()[0]):
			self.root.rightFrame.columnconfigure(columnNum, weight = 1)
			columnNum += 1

	# Iterate over the list of monsters setting the challenge
	# rating against the CR_Balance, adding the results to result_list
	def determine_results(self):
		# Refresh result list
		self.root.result_list.clear()

		for self.root.aMonster in self.root.monster_list:
			if self.root.numOfMonsters > 1:
				if self.root.aMonster["challenge_rating"] == (self.root.CR_Balance//self.root.numOfMonsters):
					self.root.result_list.append(self.root.aMonster)
			if self.root.aMonster["challenge_rating"] == self.root.CR_Balance:
				self.root.result_list.append(self.root.aMonster)

		for self.root.result in self.root.result_list:
			self.root.monsterResults.insert(END, self.root.result["name"] +  "\n")


	# Function for opening and formatting
	# the json file of monster statistics
	def format_json(self):
			# Open the file with a error catch
			try:
				self.root.monsters = open("5e_Monsters.json", "r")
			except:
				messagebox.showerror('Python Error', 'Error reading file')

			#Reading the file
			self.root.monster_list = json.loads(self.root.monsters.read())
			# Test Display of all monsters if needed:
			# self.root.formatted_json = json.dumps(self.root.monster_list, indent = 2)

	
	# Error catch for user input
	def get_pos_num(self, st):
		isNotValid = True
		while isNotValid:
			try:
				num = int(st)
				if num < 1:
					messagebox.showerror('Python Error', 'Please enter a positive integer for all fields.')
					return
				else:
					isNotValid = False
			except:
				messagebox.showerror('Python Error', 'Please enter an integer for all fields.')
				return
		return num	

	# Function to determine the appropriate
	# challenge rating.
	def CR_Calculation(self):
		if self.root.numOfPlayers > 5:
			self.root.CR_Balance = self.root.playerLevel + (self.root.numOfPlayers - 5)
		elif self.root.numOfPlayers >= 3 and self.root.numOfPlayers <= 5:
			self.root.CR_Balance = self.root.playerLevel
		elif self.root.numOfPlayers < 3:
			self.root.CR_Balance = self.root.playerLevel - 1
		elif self.root.numOfPlayers < 3 and self.root.playerLevel == 1:
			self.root.CR_Balance = 1
		return self.root.CR_Balance
	
	# Get user inputs from entry fields
	# upon button click and verify with 
	# error catch
	def on_click(self):
		self.root.monsterResults.delete(1.0, END)
		self.root.numOfPlayers = self.root.playersEntry.get()
		self.root.playerLevel = self.root.playerLevelEntry.get()
		self.root.numOfMonsters = self.root.numOfMonstersEntry.get()
		self.root.numOfPlayers = self.get_pos_num(self.root.numOfPlayers)
		self.root.playerLevel = self.get_pos_num(self.root.playerLevel)
		self.root.numOfMonsters = self.get_pos_num(self.root.numOfMonsters)
		self.root.CR_Balance = self.CR_Calculation()
		self.determine_results()
	
	# Function to make left click to set Chosen
	# result within result window. 
	def select_line(self, event):
		self.root.chosenResult = self.root.monsterResults.get('insert linestart', 'insert lineend')
		
	# Function to make left click also Display
	# chosen results in final result window in 
	# the right frame.
	def display_results(self,event):
		self.root.chosenMonsterInfo.delete(1.0, END)
		for self.root.result in self.root.result_list:
			if self.root.chosenResult.lower() == self.root.result["name"].lower():
				self.root.finalResult = json.dumps(self.root.result, indent = 2)
		self.root.chosenMonsterInfo.insert(END, self.root.finalResult)
				

# Main Function
def main():
	root = Tk()
	root.columnconfigure(0, weight = 1)
	root.rowconfigure(0, weight = 1)
	testApp = Application(root, "5th Edition Encounter Generator", "1024x576")
	root.mainloop()
	return None

# Run Main Function
main()

