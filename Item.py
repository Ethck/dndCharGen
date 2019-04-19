import json

class Item():
	def __init__(self, items):
		self.buildItems(items)

	def __str__(self):
		return self.name

	def buildItems(self, item):
		self.name = item['name']
		self.type = item['type']
		self.source = item['source']
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