import random
import json

class PlayerCharacter():
	def __init__(self):
		self.loadOptions()
		self.buildCharacter()
		self.handleProfs()
		self.cleanEquipment()
		print("You have a character!")

	def loadOptions(self):
		with open("barbarian.json") as file:
			a = json.load(file)
			# name, source, hd, proficiency, classTableGroups, startingProficiencies, startingEquipment,
			# multiclassing, classFeatures, subclassTitle, subclasses, fluff
			self.b = a['class'][0]

	def rollStat(self):
		a = random.randint(2,6)
		b = random.randint(2,6)
		c = random.randint(2,6)
		d = random.randint(2,6)

		return a + b + c + d - min(a, b, c, d)

	def handleProfs(self):
		i = int(self.b['startingProficiencies']['skills']['choose'])
		j = self.b['startingProficiencies']['skills']['from']
		while i > 0:
			print(f"Choose a prof by index." + ', '.join(self.b['startingProficiencies']['skills']['from']))
			i -= 1
			c = int(input("Index?\n"))

			if j[c] == "Acrobatics":
				self.acrobatics += self.prof
			elif j[c] == "Animal Handling":
				self.animal += self.prof
			elif j[c] == "Arcana":
				self.arcana += self.prof
			elif j[c] == "Athletics":
				self.athletics += self.prof
			elif j[c] == "Deception":
				self.deception += self.prof
			elif j[c] == "History":
				self.history += self.prof
			elif j[c] == "Insight":
				self.insight += self.prof
			elif j[c] == "Intimidation":
				self.intimidation += self.prof
			elif j[c] == "Investigation":
				self.investigation += self.prof
			elif j[c] == "Medicine":
				self.medicine += self.prof
			elif j[c] == "Nature":
				self.nature += self.prof
			elif j[c] == "Perception":
				self.perception += self.prof
			elif j[c] == "Performance":
				self.performance += self.prof
			elif j[c] == "Persuasion":
				self.persuasion += self.prof
			elif j[c] == "Religion":
				self.religion += self.prof
			elif j[c] == "Sleight of Hand":
				self.sleight += self.prof
			elif j[c] == "Stealth":
				self.stealth += self.prof
			elif j[c] == "Survival":
				self.survival += self.prof
			else:
				print("Unknown proficiency")

	def cleanEquipment(self):
		a = self.b['startingEquipment']['default']
		for choice in a:
			print(choice)
			i = choice.split("{@")
			print(i)


	def buildCharacter(self):
		self.name = input("Name?\n")
		self.pstr = self.rollStat()
		self.strmod = int((self.pstr - 10) / 2)
		self.dex = self.rollStat()
		self.dexmod = int((self.dex - 10) / 2)
		self.con = self.rollStat()
		self.conmod = int((self.con - 10) / 2)
		self.pint = self.rollStat()
		self.intmod = int((self.pint - 10) / 2)
		self.wis = self.rollStat()
		self.wismod = int((self.wis - 10) / 2)
		self.cha = self.rollStat()
		self.chamod = int((self.cha - 10) / 2)
		self.level = int(input("What level character?\n"))
		self.classes = self.b['name'] + " " + str(self.level)
		self.background = "Merchant"
		self.pname = input("Player Name?\n")
		self.race = "Human"
		self.alignment = "CN"
		self.xp = 0
		self.ac = 10
		self.init = self.dexmod
		self.speed = 30
		self.hd = int(self.b['hd']['faces'])
		self.hpmax = int((self.hd + self.conmod) + ((self.level - 1) * (-(-self.hd / 2) + 1 + self.conmod)))
		self.hpcurrent = self.hpmax
		self.hptemp = 0
		self.hptotal = self.level
		self.ptraits = "a" 
		self.ideals = "a"
		self.bonds = "a"
		self.flaws = "a"
		self.profs = "=Armor=\n" + ', '.join(self.b['startingProficiencies']['armor']) + "\n=Weapons=\n" + ', '.join(self.b['startingProficiencies']['weapons'])
		self.features = "a"
		self.equipment = ', '.join(self.b['startingEquipment']['default'])
		self.cp = 0
		self.sp = 0
		self.ep = 0
		self.gp = 0
		self.pp = 0
		self.prof = -(-self.level // 4) + 1
		self.attacks = ""
		self.wpn1 = "Longsword"
		self.wpn2 = 0
		self.wpn3 = 0
		self.wpn1atk = self.strmod + self.prof
		self.wpn2atk = 0
		self.wpn3atk = 0
		self.wpn1dmg = self.strmod
		self.wpn2dmg = 0
		self.wpn3dmg = 0
		self.inspir = 0
		self.ststr = self.strmod
		self.stdex = self.dexmod
		self.stcon = self.conmod
		self.stint = self.intmod
		self.stwis = self.wismod
		self.stcha = self.chamod
		self.acrobatics = self.dexmod
		self.animal = self.wismod
		self.aracna = self.intmod
		self.athletics = self.strmod
		self.deception = self.chamod
		self.history = self.intmod
		self.insight = self.wismod
		self.intimidation = self.chamod
		self.investigation = self.intmod
		self.medicine = self.wismod
		self.nature = self.intmod
		self.perception = self.wismod
		self.performance = self.chamod
		self.persuasion = self.chamod
		self.religion = self.intmod
		self.sleight = self.dexmod
		self.stealth = self.dexmod
		self.survival = self.wismod
		self.passivep = 10 + self.perception #Passive Perception