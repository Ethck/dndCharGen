import random
import json

class PlayerCharacter():

	def buildCharacter(self):
		#self.name = input("Name?\n")
		self.name = "Orog"
		self.pstr = rollStat()
		self.strmod = int((self.pstr - 10) / 2)
		self.dex = rollStat()
		self.dexmod = int((self.dex - 10) / 2)
		self.con = rollStat()
		self.conmod = int((self.con - 10) / 2)
		self.pint = rollStat()
		self.intmod = int((self.pint - 10) / 2)
		self.wis = rollStat()
		self.wismod = int((self.wis - 10) / 2)
		self.cha = rollStat()
		self.chamod = int((self.cha - 10) / 2)
		#self.level = int(input("What level character?\n"))
		self.level = 4
		self.classes = self.b['name'] + " " + str(self.level)
		self.background = "Merchant"
		#self.pname = input("Player Name?\n")
		self.pname = "Ethck"
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
		self.ptraits = "a" #derived from background 
		self.ideals = "a" #derived from background
		self.bonds = "a" #derived from background
		self.flaws = "a" #derived from background
		if ('armor' not in self.b['startingProficiencies'].keys()):
			self.profs = "=Weapons=\n" + ", ".join(self.b['startingProficiencies']['weapons'])
		else:
			self.profs = "=Armor=\n" + ', '.join(self.b['startingProficiencies']['armor']) + "\n=Weapons=\n" + ', '.join(self.b['startingProficiencies']['weapons'])
		self.features = "a"
		self.equipment = []
		self.cp = 0
		self.sp = 0
		self.ep = 0
		self.gp = 0
		self.pp = 0
		self.prof = -(-self.level // 4) + 1
		self.attacks = ""
		self.wpn1 = ""
		self.wpn2 = ""
		self.wpn3 = ""
		self.wpn1atk = ""
		self.wpn2atk = ""
		self.wpn3atk = ""
		self.wpn1dmg = ""
		self.wpn2dmg = ""
		self.wpn3dmg = ""
		self.inspir = 0
		self.ststr = self.strmod
		self.stdex = self.dexmod
		self.stcon = self.conmod
		self.stint = self.intmod
		self.stwis = self.wismod
		self.stcha = self.chamod
		self.skillProfs = {
			'acrobatics': [False, self.dexmod],
			'animal': [False, self.wismod],
			'aracna': [False, self.intmod],
			'athletics': [False, self.strmod],
			'deception': [False, self.chamod],
			'history': [False, self.intmod],
			'insight': [False, self.wismod],
			'intimidation': [False, self.chamod],
			'investigation': [False, self.intmod],
			'medicine': [False, self.wismod],
			'nature': [False, self.intmod],
			'perception': [False, self.wismod],
			'performance': [False, self.chamod],
			'persuasion': [False, self.chamod],
			'religion': [False, self.intmod],
			'sleight': [False, self.dexmod],
			'stealth': [False, self.dexmod],
			'survival': [False, self.wismod]
		}
		self.passivep = 10 + self.skillProfs['perception'][1] #Passive Perception

def rollStat():
	a = random.randint(2,6)
	b = random.randint(2,6)
	c = random.randint(2,6)
	d = random.randint(2,6)

	return a + b + c + d - min(a, b, c, d)