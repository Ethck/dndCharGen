import random
import json
from glob import glob
import Item

class Background():
	def __init__(self, bkg):
		self.buildBackground(bkg)

	def __str__(self):
		return self.name

	def buildBackground(self, bkg):
		self.bkg = bkg
		self.name = bkg['name']
		self.skillProfs = bkg['skillProficiencies']
		self.source = bkg['source']
		self.bannedBackgrounds = ["Dissenter", "Inquisitor", "Variant Criminal (Spy)", "Variant Entertainer (Gladiator)", "Variant Guild Artisan (Guild Merchant)", "Variant Sailor (Pirate)"]


class playerSubClass():
	def __init__(self, subJSON):
		self.name = subJSON['name']
		self.json = subJSON

	def __str__(self):
		return self.name


class PlayerClass():
	def __init__(self, classJSON):
		self.buildClass(classJSON)

	def __str__(self):
		return self.name

	def buildClass(self, classJSON):
		self.name = classJSON['name']
		self.json = classJSON
						
def backgroundFeatures(background, list, key, player):
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
	background = player.background
	if background.name not in background.bannedBackgrounds:
		if background.source != "SCAG":
			#SCAG support requires all PHB backgrounds to be done first.
			for i in range(len(background.bkg['entries'])):
				if "name" in background.bkg['entries'][i]  and background.bkg['entries'][i]['name'] == "Suggested Characteristics":
					background.suggestChars = background.bkg['entries'][i]
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
	for i, choice in enumerate(list):
		print(f"{i}: {str(choice)}")

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
	resultList = []
	with open(file) as f:
		j = json.load(f)[fileIndex]
		for i in j:
			resultList.append(listAction(i))

	return resultList


def equipFromClass(playerClass, itemList, player):
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
	# b is num Options
	for b in k:
		if (len(b) > 1):
			i = 0
			if len(b) == 2:
				u = input(f"Do you want (a) a(n) {b[0]} or (b) a {b[1]}?")
			elif len(b) == 3:
				u = input(f"Do you want (a) a(n) {b[0]} and a(n) {b[1]} or (b) a {b[2]}?")
			if u == 'a':
				player.equipment.append(b[1].name)

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
	json = player.b['classFeatures']
	features = []
	subFeatures = []
	for i, feature in enumerate(json):
		if i <= player.level -1:
			for a in feature:
				if i == 0 or i == 2:
					#CHOOSE A SUBCLASS
					if 'gainSubclassFeature' in a.keys() and not hasattr(player, 'subClass'):
						subclasses = []
						for sub in player.b['subclasses']:
							subclasses.append(playerSubClass(sub))
						c = provideChoice(subclasses, None, "Subclass", True)
						player.subClass = c
						#print(player.subClass.json)
						#for d in player.subClass.json['subclassFeatures']:
							#print(d[0]['name'])#['entries']['name'])

				elif a['name'] == "Ability Score Improvement":
					print(f"ASI earned at level {i + 1}")
					continue
				elif 'gainSubclassFeature' in a.keys():
					print(f"Subclass ability earned at level {i + 1}")
				else:
					fstring = str(f"{a['name']}")
					features.append(fstring)

	player.features = '\n'.join(features)


def assignEquipment(weapon, player):
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
				player.skillProfs[j[c].lower().split(" ")[0]][0] == True
				player.skillProfs[j[c].lower().split(" ")[0]][1] += player.prof
			elif j[c].lower() in player.skillProfs:
				player.skillProfs[j[c].lower()][0] == True
				player.skillProfs[j[c].lower()][1] += player.prof

			prevChoices.append(c)
		else:
			print("Please select a different index.")
			i += 1

def registerOptions(player):
	items = buildJsonList("data/items.json", 'basicitem', Item.Item)
	items2 = buildJsonList("data/items2.json", 'item', Item.Item)
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
	handleProfs(player)
	equipFromClass(playerClass, items, player)

	bkgList = buildJsonList("data/backgrounds.json", 'background', Background)
	player.background = provideChoice(bkgList, makeBKGFeatures, "Background", True)
	makeBKGFeatures(player)
	getClassAbilities(player)
