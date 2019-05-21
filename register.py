import random
import json
from glob import glob
import re
from colorama import Fore, Style


class Background():
	"""Stores info about the various backgrounds for reference"""

	def __init__(self, bkg):
		"""Start the process through building the object."""
		self.buildBackground(bkg)

	def __str__(self):
		"""If we call str() on the function, return it's name."""
		return self.name

	def buildBackground(self, bkg):
		"""Set up the initial variables."""
		self.bkg = bkg
		self.name = bkg['name']
		self.skillProfs = bkg['skillProficiencies']
		self.source = bkg['source']
		self.bannedBackgrounds = ["Dissenter", "Inquisitor", "Variant Criminal (Spy)", "Variant Entertainer (Gladiator)", "Variant Guild Artisan (Guild Merchant)", "Variant Sailor (Pirate)"]


class Race():
	"""Container for Race statistics"""

	def __init__(self, json, parent = None):
		"""Set up init values"""
		self.json = json
		self.name = json['name'].replace("(", "").replace(")", "")


		if parent != None:
			self.parent = parent
			self.speed = self.parent.speed
			self.source = self.parent.source
			self.pname = ' ->  ' + self.name + " | " + self.source
		else:
			if isinstance(json['speed'], dict):
				self.speed = json['speed']['walk']
			else:
				self.speed = json['speed']

			self.source = json['source']

		self.name = self.name + " | " + self.source
		self.abiInc = {}

	def __lt__(self, other):
		return self.name < other.name

	def __eq__(self, other):
		if other == None:
			return False
		else:
			return self.name == other.name

	def raceChosen(self, player):
		"""Once given a chosen race, change the player to reflect it"""
		player.race == self.name
		json = self.json
		if 'ability' in json.keys():
			for ability in json['ability']:
				if ability == "choose":
					choices = []
					for abi in json['ability']['choose'][0]['from']:
						choices.append(abi)

					i = json['ability']['choose'][0]['count']
					while i > 0:
						print(f"There are {i} choice(s) remaining.")
						choice = provideChoice(choices, None, "Stat", True)
						choices.remove(choice)
						if 'amount' in json['ability']['choose'][0]:
							self.abiInc[choice] = json['ability']['choose'][0]['amount']
						else:
							self.abiInc[choice] = 1
						i = i - 1
				else:
					self.abiInc[ability] = json['ability'][ability]

			print(self.abiInc)

			for abi in self.abiInc:
				if "str" in abi:
					player.pstr += self.abiInc[abi]
				elif "dex" in abi:
					player.dex += self.abiInc[abi]
				elif "con" in abi:
					player.con += self.abiInc[abi]
				elif "int" in abi:
					player.pint += self.abiInc[abi]
				elif "wis" in abi:
					player.wis += self.abiInc[abi]
				elif "cha" in abi:
					player.cha += self.abiInc[abi]

	def __str__(self):
		if hasattr(self, "parent"):
			return self.pname
		else:
			return self.name


class Item():
	"""Container for all item characteristics"""

	def __init__(self, item):
		"""Call the build function.

		:param item: The item JSON we are building.
		"""
		self.buildItems(item)

	def __str__(self):
		"""Return the name when str() is used"""
		return self.name

	def buildItems(self, item):
		"""Determine the type of item, then add those properties.

		:param item: Item JSON we are working on.
		"""
		self.name = item['name']
		if ('type' in item.keys()):
			self.type = item['type']

		self.source = item['source']

		if ('page' in item.keys()):
			self.page = item['page']

		if ('weapon' in item.keys()):
			# Weapon
			self.weapon = True
			self.weaponCategory = item['weaponCategory']
			if ('property' in item.keys()):
				self.property = item['property']
			if ('dmg1' in item.keys()):
				self.dmg1 =  item['dmg1']
				if len(self.dmg1) > 1:
					self.dmg1 = self.dmg1.split(" ")[1].split("}")[0]
			if ('dmg2' in item.keys()):
				self.dmg2 =  item['dmg2']
				if len(self.dmg2) > 1:
					self.dmg2 = self.dmg2.split(" ")[1].split("}")[0]
			if ('dmgType' in item.keys()):
				self.dmgType = item['dmgType']

		elif ('armor' in item.keys()):
			# Armor
			self.armor = True
			self.ac = item['ac']

		elif ('ammunition' in item.keys()):
			self.ammunition = True


class playerSubClass():
	"""Store info about subclasses for reference"""

	def __init__(self, subJSON):
		"""Make some vars for reference"""
		self.name = subJSON['name']
		self.json = subJSON

	def __str__(self):
		"""Return the name when str() is used"""
		return self.name


class PlayerClass():
	"""Store info about all classes for reference"""

	def __init__(self, classJSON):
		"""Call the starting function"""
		self.buildClass(classJSON)

	def __str__(self):
		"""Return the name when str() is used"""
		return self.name

	def buildClass(self, classJSON):
		"""Set up some vars for reference"""
		self.name = classJSON['name']
		self.json = classJSON
						

def backgroundFeatures(background, list, key, player):
	"""Choose and assign features for chosen background.

	:param background: A Background() that is the chosen background
	:param list: list of possible options the key can assume
	:param key: Name for an option (pTraits, Ideals, Bonds, Flaws)
	:param player: A Player() instance to affect
	"""
	c = None
	while True:
		c = input(f"{key}: (a) choice or (b) random?")
		if c == "a":
			for t in list:
				print(str(int(t[0]) - 1) + ": " + t[1])

			d = -10
			while d < 0 or d >= len(list):
				d = int(input("Which trait?"))

			background.fluff[key] = list[d][1]
			break

		elif c == "b":
			background.fluff[key] = list[random.randint(0, len(list) - 1)][1]
			break
		else:
			continue

	print(background.fluff[key])


def makeBKGFeatures(player):
	"""Find and provide lists of all possible options

	:param player: Instance of player() to affect
	"""
	background = player.background
	if background.name not in background.bannedBackgrounds:
		if background.source != "SCAG":
			#SCAG support requires all PHB backgrounds to be done first.
			for i in range(len(background.bkg['entries'])):
				if "name" in background.bkg['entries'][i]  and background.bkg['entries'][i]['name'] == "Suggested Characteristics":
					background.suggestChars = background.bkg['entries'][i]
					print(len(background.suggestChars['entries']))
					if len(background.suggestChars['entries']) > 4:
						background.pTraits = background.suggestChars['entries'][1]['rows']
						background.ideals = background.suggestChars['entries'][2]['rows']
						background.bonds = background.suggestChars['entries'][3]['rows']
						background.flaws = background.suggestChars['entries'][4]['rows']
						background.fluff = {}

						backgroundFeatures(background, background.pTraits, "pTrait", player)
						backgroundFeatures(background, background.ideals, "ideal", player)
						backgroundFeatures(background, background.bonds, "bond", player)
						backgroundFeatures(background, background.flaws, "flaw", player)

						player.ptraits = background.fluff['pTrait']
						player.ideals = background.fluff['ideal']
						player.bonds = background.fluff['bond']
						player.flaws = background.fluff['flaw']
						player.background = background.name


def provideChoice(list, action, name, ret = False):
	"""Allow the user to choose options.

	:param list: List of options for the user to choose from.
	:param action: Function to run upon user choosing.
	:param name: Printable name for what user is choosing.
	:param ret: Boolean for whether or not to return a value.
	:returns: User chosen value if ret = True
	"""
	for i, choice in enumerate(list):
		print(f"{Fore.BLUE}{i}:{Style.RESET_ALL} {Fore.GREEN}{str(choice)}{Style.RESET_ALL} ")

	print(f"Choose a {name} by index.")
	while True:
		c = int(input("Index?\n"))
		if c >= 0 and c <= len(list) - 1:
			if ret:
				return list[c]
			else:
				action(list[c])
			break
		else:
			continue


def buildJsonList(file, fileIndex, listAction):
	"""Build list from JSON while using a wrapper function.

	
	:param file: Path to a JSON file
	:param fileIndex: Key/indexing string for what is desired.
	:param listAction: Wrapper function for the indexed data.
	"""
	resultList = []
	with open(file) as f:
		j = json.load(f)[fileIndex]
		for i in j:
			resultList.append(listAction(i))

	return resultList


def equipFromClass(playerClass, itemList, player):
	"""Grant the player equipment based on their class.

	:param playerClass: The chosen class' JSON
	:param itemList: list of all available items
	:param player: instance of PlayerCharacter() class
	"""
	classOptions = playerClass.json
	a = classOptions['startingEquipment']['default']
	k = []
	for choice in a:
		ret = []
		i = choice.split("{@")
		lines = []
		for line in i:
			if 'item' or 'filter' in line:
				c = line.split("|")
				if (len(c) > 1):
					s = c[0].replace('item ', '').replace('filter ', '')
					lines.append(s)

		for j in lines:
			for item in itemList:
				if item.name.lower() == j:
					ret.append(item)
					break
				elif "martial" in j:
					ret.append("Martial")
					break
				elif "simple" in j:
					ret.append("Simple")
					break

		#print([r.name for r in ret])
		k.append(ret)
	chooseEquipment(k, itemList, player)


def chooseEquipment(k, itemList, player):
	"""For all equipment in starting options, give a choice.

	:param k: List of all possible choices
	:param itemList: List of all possible items.
	:param player: Instance of PlayerCharacter() class
	"""
	for b in k:
		# b is num Options to choose from
		if (len(b) > 1):
			i = 0
			if len(b) == 2:
				u = input(f"Do you want (a) a(n) {b[0]} or (b) a {b[1]}? ")
			elif len(b) == 3:
				u = input(f"Do you want (a) a(n) {b[0]} and a(n) {b[1]} or (b) a {b[2]}? ")
			if u == 'a':
				if isinstance(b[0], str) or (isinstance(b[1], str) and len(b) == 3):
					#It's a choice weapon
					if isinstance(b[0], str):
						w = b[0]
					else:
						w = b[1]
					weapons = []
					for item in itemList:
						if (hasattr(item, 'weaponCategory')):
							if w == "Martial" and item.weaponCategory == "Martial":
								weapons.append(item)
							elif w == "Simple" and item.weaponCategory == "Simple":
								weapons.append(item)

					c = provideChoice(weapons, None, "Weapon", True)
					assignEquipment(c, player)
				else:
					player.equipment.append(b[0].name)

				# It's a weapon
				if hasattr(b[i], 'weaponCategory'):
					assignEquipment(b[i], player)
			else:
				i = -1
				# Generic item OR weaponlist
				if b[i] == 'Martial' or b[i] == 'Simple':
					weapons = []
					for item in itemList:
						if (hasattr(item, 'weaponCategory')):
							if b[i] == "Martial" and item.weaponCategory == "Martial":
								weapons.append(item)
							elif b[i] == "Simple" and item.weaponCategory == "Simple":
								weapons.append(item)

					c = provideChoice(weapons, None, "Weapon", True)
					assignEquipment(c, player)
				else:
					if hasattr(b[i], 'weaponCategory'):
						print(b[i])
						assignEquipment(b[i], player)
					else:
						player.equipment.append(b[i].name)
			i = 0


def getClassAbilities(player):
	"""Get all abilities granted by reaching level X in class

	:param player: Insance of PlayerCharacter() to affect
	"""
	json = player.b['classFeatures']
	features = []
	subFeatures = []
	player.subClassLevels = []
	player.subClassFeatures = []

	for i, feature in enumerate(json):
		if i <= player.level - 1:
			for a in feature:
				if (i <= 2):
					#CHOOSE A SUBCLASS
					if 'gainSubclassFeature' in a.keys() and not hasattr(player, 'subClass'):
						print(f"Subclass gained at level {i + 1}")

						subclasses = []
						for sub in player.b['subclasses']:
							subclasses.append(playerSubClass(sub))

						c = provideChoice(subclasses, None, "Subclass", True)
						player.subClass = c

						for d in player.subClass.json['subclassFeatures']:
							if isinstance(d[0]['entries'][0], dict):
								subFeatures.append(d[0]['entries'][0])
								result = re.search('[aA]t(.*)level', d[0]['entries'][0]['entries'][0])
								if result != None:
									result = result.group(1).split("level")[0]
									player.subClassLevels.append(result)

					elif 'gainSubclassFeature' in a.keys():
						print(f"Subclass ability earned at level {i + 1}")
						for i, level in enumerate(player.subClassLevels):
							if 'r' in level:
								a = level.split('r')[0]
							elif 't' in level:
								a = level.split('t')[0]

							if int(a) <= player.level:
								player.subClassFeatures.append(subFeatures[i])
				elif a['name'] == "Ability Score Improvement":
					print(f"ASI earned at level {i + 1}")
					c = input(f"Take an (a) ASI or (b) a feat?")
				elif 'gainSubclassFeature' in a.keys():
					print(f"Subclass ability earned at level {i + 1}")
					for i, level in enumerate(player.subClassLevels):
							if 'r' in level:
								a = level.split('r')[0]
							elif 't' in level:
								a = level.split('t')[0]

							if int(a) <= player.level:
								player.subClassFeatures.append(subFeatures[i])
				else:
					fstring = str(f"{a['name']}")
					features.append(fstring)

	player.features = "Class features\n" + "-" * 10 + "\n"
	player.features += '\n'.join(features)
	player.features += '\nSubclass Features\n' + "-" * 10 + "\n"
	player.features += '\n'.join([feature['name'] for feature in player.subClassFeatures])


def assignEquipment(weapon, player):
	"""Given the chosen equipment, assign it to the character.

	:param weapon: An Item() chosen by the player
	:param player: Instance of PlayerCharacter() to affect
	"""
	if not hasattr(weapon, 'property'): weapon.property = 'None'
	if player.wpn1 == "":
		player.wpn1 = weapon.name
		if 'F' not in weapon.property:
			player.wpn1atk = player.strmod + player.prof
			player.wpn1dmg = weapon.dmg1 + " + " + str(player.strmod)
		else:
			player.wpn1atk = player.dexmod + player.prof
			player.wpn1dmg = weapon.dmg1 + " + " + str(player.dexmod)
	elif player.wpn2 == "":
		player.wpn2 = weapon.name
		if 'F' not in weapon.property:
			player.wpn2atk = player.strmod + player.prof
			player.wpn2dmg = weapon.dmg1 + " + " + str(player.strmod)
		else:
			player.wpn2atk = player.dexmod + player.prof
			player.wpn2dmg = weapon.dmg1 + " + " + str(player.dexmod)
	elif player.wpn3 == "":
		player.wpn3 = weapon.name
		if 'F' not in weapon.property:
			player.wpn3atk = player.strmod + player.prof
			player.wpn3dmg = weapon.dmg1 + " + " + str(player.strmod)
		else:
			player.wpn3atk = player.dexmod + player.prof
			player.wpn3dmg = weapon.dmg1 + " + " + str(player.dexmod)


def handleProfs(player):
	"""Given class, provide choice about proficiencies.

	:param player: Instance of PlayerCharacter() to affect
	"""
	i = int(player.b['startingProficiencies']['skills']['choose'])
	j = player.b['startingProficiencies']['skills']['from']
	prevChoices = []
	while i > 0:
		for k, choice in enumerate(j):
			print(f"{k}: {str(choice)}")

		print(f"Choose a proficiency by index.")
		i -= 1
		c = int(input("Index?\n"))
		if c >= 0 and c <= len(j) - 1 and c not in prevChoices:
			if len(j[c].lower().split(" ")) > 1:
				a = player.skillProfs[j[c].lower().split(" ")[0]]
				if not a[0]:
					a[0] == True
					a[1] += player.prof
				else:
					print(f"You are already proficient in this already")
					i += 1
			elif j[c].lower() in player.skillProfs:
				a = player.skillProfs[j[c].lower()]
				if not a[0]:
					a[0] == True
					a[1] += player.prof
				else:
					print(f"You are already proficient in this already")
					i += 1

			prevChoices.append(c)
		else:
			print("Please select a different index.")
			i += 1


def filterBKGList(bkgList):
	"""Filter the list of Backgrounds to only include supported.

	:param bkgList: List of all available Background()s
	"""
	newBKGList = []

	for background in bkgList:
		if background.name not in background.bannedBackgrounds:
			if background.source != "SCAG":
				#SCAG support requires all PHB backgrounds to be done first.
				for i in range(len(background.bkg['entries'])):
					if "name" in background.bkg['entries'][i]  and background.bkg['entries'][i]['name'] == "Suggested Characteristics":
						background.suggestChars = background.bkg['entries'][i]
						if len(background.suggestChars['entries']) > 4:
							newBKGList.append(background)

	return newBKGList

def addSubRaces(raceList):
	""" Add the Sub Races from each race

	:param raceList: List of Race(s) to add to.
	"""
	newRaces = raceList
	for race in raceList:
		if 'subraces' in race.json.keys():
			for subRace in race.json['subraces']:
				if len(subRace) != 0:
					tSubRace = Race(subRace, race)
					tSubRace.name = race.name + " - " + tSubRace.name + " (" + tSubRace.source + ")"
					newRaces.append(tSubRace)

	return newRaces

def filterRaces(raceList):
	""" Remove all non supported races.

	:param raceList: List of Race(s) to filter
	"""
	trimRaces = []
	for race in raceList:
		# The in operator behaves off of __eq__
		# __eq__ is overriden to test for names
		if race not in trimRaces: 
			trimRaces.append(race)
	return trimRaces


def registerOptions(player):
	"""Main method to "build" the player character.

	:param player: Instance of PlayerCharacter() to affect
	"""

	races = buildJsonList("data/races.json", 'race', Race)
	races = addSubRaces(races)
	races = filterRaces(races)
	races.sort()
	playerRace = provideChoice(races, None, "Race", True)
	items = buildJsonList("data/items.json", 'basicitem', Item)
	items2 = buildJsonList("data/items2.json", 'item', Item)
	items = [*items, *items2]

	playerClasses = []
	for i in glob('data/classes/*.json'):
		with open(i) as file:
			player.json = json.load(file)['class']
			player.b = player.json[0]


		playerClasses.append(PlayerClass(player.b))

	playerClass = provideChoice(playerClasses, None, "Class", True)
	player.b = playerClass.json

	player.buildCharacter()
	playerRace.raceChosen(player)
	handleProfs(player)
	equipFromClass(playerClass, items, player)

	bkgList = buildJsonList("data/backgrounds.json", 'background', Background)
	bkgList = filterBKGList(bkgList)
	player.background = provideChoice(bkgList, makeBKGFeatures, "Background", True)
	makeBKGFeatures(player)

	getClassAbilities(player)