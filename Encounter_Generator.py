import json
import tkinter

# Error catching for the user inputs
def get_pos_num(st):
	isNotValid = True
	while isNotValid:
		try:
			num = int(input(st))
			if num < 1:
				print("Enter a positive integer.")
				num = int(input(st))
			else:
				isNotValid = False
		except:
			print("Enter an integer.")
	return num

#	Initialize the number of players and their level, and
#	how many mosters if they would like
player_count = get_pos_num("How many players do you have?")

avg_level = get_pos_num("What is the aproximate average level of your party?")

monster_num = get_pos_num("How many monsters would you prefer, if a specific amount?")


#   Using the above inputs, generate a number to search for monsters
#	with appropriate Challenge Rating for the party in the dictionary
if player_count > 5:
	CR_Balance = avg_level + (player_count - 5)
elif player_count >= 3 and player_count <= 5:
	CR_Balance = avg_level
elif player_count < 3:
	CR_Balance = avg_level - 1
elif player_count < 3 and avg_level == 1:
	CR_Balance = 1

#	Open the file with a error catch
try:
	monsters = open("5e_Monsters.json", "r")
except:
	print("Error reading '5e_Monsters' file")

#	Reading the file
monster_list = json.loads(monsters.read())

#	Create a list to add results from the balancing math
#	and the monster_list

result_list = []

#	Iterate over the list of monsters setting the challenge
# 	rating against the CR_Balance from earlier, adding the
#	results to result_list

for amonster in monster_list:
	if monster_num > 1:
		if amonster["challenge_rating"] == (CR_Balance//monster_num):
			result_list.append(amonster)
	if amonster["challenge_rating"] == CR_Balance:
		result_list.append(amonster)

#   Print the names and challenge ratings of the monsters
#   that have the right CR_Balance
for result in result_list:
	print(result["name"],result["challenge_rating"])

#   Ask for a specific monster and print that monster's details
info_request = input("Enter the name of the monster you would like information on:")
for result in result_list:
	if info_request.lower() == result["name"].lower():
		the_chosen_one = result
print(json.dumps(the_chosen_one, indent = 2))
