import random

class PlayerCharacter():
	def __init__(self):
		self.buildCharacter()
		print("You have a character!")

	def rollStat(self):
		a = random.randint(2,6)
		b = random.randint(2,6)
		c = random.randint(2,6)
		d = random.randint(2,6)

		return a + b + c + d - min(a, b, c, d)

	def buildCharacter(self):
		self.name = input("Name?")
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
		self.classes = "Fighter 1"
		self.background = "Merchant"
		self.pname = "IDK"
		self.race = "Human"
		self.alignment = "CN"
		self.xp = 0
		self.ac = 10
		self.init = self.dexmod
		self.speed = 30
		self.hpmax = 10
		self.hpcurrent = 10
		self.hptemp = 0
		self.hptotal = 10
		self.hd = 1
		self.ptraits = "a" 
		self.ideals = "a"
		self.bonds = "a"
		self.flaws = "a"
		self.profs = "a"
		self.features = "a"
		self.equipment = "a"
		self.cp = 0
		self.sp = 0
		self.ep = 0
		self.gp = 0
		self.pp = 0
		self.attacks = 0
		self.wpn1 = 0
		self.wpn2 = 0
		self.wpn3 = 0
		self.wpn1atk = 0
		self.wpn2atk = 0
		self.wpn3atk = 0
		self.wpn1dmg = 0
		self.wpn2dmg = 0
		self.wpn3dmg = 0
		self.inspir = 0
		self.prof = 2
		self.ststr = self.strmod
		self.stdex = self.dexmod
		self.stcon = self.conmod
		self.stint = self.intmod
		self.stwis = self.wismod
		self.stcha = self.chamod
		self.acro = self.dexmod
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