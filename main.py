#! /usr/bin/python3

import os
import pdfrw
import PlayerCharacter as pc
import json
import Item

templatePath = 'template.pdf'

annotMarker = '/Annots'
fieldMarker = '/T'
subMarker = '/Subtype'
widgetMarker = '/Widget'

def writePDF(inputPath, outputPath, dataDict):
	templatePDF = pdfrw.PdfReader(inputPath)
	annotations = templatePDF.pages[0][annotMarker]
	for annotation in annotations:
		if annotation[subMarker] == widgetMarker:
			if annotation[fieldMarker]:
				key = annotation[fieldMarker][1:-1]
				if key in dataDict.keys():
					annotation.update(pdfrw.PdfDict(V='{}'.format(dataDict[key])))

	pdfrw.PdfWriter().write(outputPath, templatePDF)

# Make a Character
player = pc.PlayerCharacter()

# Instantiate all items.
items = []

with open("items.json") as j:
	ItemsList = json.load(j)['basicitem']

for item in ItemsList:
	w = Item.Item(item)
	items.append(w)

#print(items)
player.cleanEquipment(items)

defaultData = {
	'CharacterName': player.name,
	'STR': player.pstr,
	'STRmod': player.strmod,
	'DEX': player.dex,
	'DEXmod ': player.dexmod,
	'CON': player.con,
	'CONmod': player.conmod,
	'INT': player.pint,
	'INTmod': player.intmod,
	'WIS': player.wis,
	'WISmod': player.wismod,
	'CHA': player.cha,
	'CHamod': player.chamod,
	'ClassLevel': player.classes,
	'Background': player.background,
	'PlayerName': player.pname,
	'Race ': player.race,
	'Alignment': player.alignment,
	'XP': player.xp,
	'AC': player.ac,
	'Initiative': player.init,
	'Speed': player.speed,
	'HPMax': player.hpmax,
	'HPCurrent': player.hpcurrent,
	'HPTemp': player.hptemp,
	'HDTotal': player.hptotal,
	'HD': player.hd,
	'PersonalityTraits ': player.ptraits,
	'Ideals': player.ideals,
	'Bonds': player.bonds,
	'Flaws': player.flaws,
	'ProficienciesLang': player.profs,
	'Features and Traits': player.features,
	'Equipment': player.equipment,
	'CP': player.cp,
	'SP': player.sp,
	'EP': player.ep,
	'GP': player.gp,
	'PP': player.pp,
	'AttacksSpellcasting': player.attacks,
	'Wpn Name': player.wpn1,
	'Wpn Name 2': player.wpn2,
	'Wpn Name 3': player.wpn3,
	'Wpn1 AtkBonus': player.wpn1atk,
	'Wpn2 AtkBonus ': player.wpn2atk,
	'Wpn3 AtkBonus  ': player.wpn3atk,
	'Wpn1 Damage': player.wpn1dmg,
	'Wpn2 Damage ': player.wpn2dmg,
	'Wpn3 Damage ': player.wpn3dmg,
	'Inspiration': player.inspir,
	'ProfBonus': player.prof,
	'ST Strength': player.ststr,
	'ST Dexterity': player.stdex,
	'ST Constitution': player.stcon,
	'ST Intelligence': player.stint,
	'ST Wisdom': player.stwis,
	'ST Charisma': player.stcha,
	'Acrobatics': player.skillProfs['acrobatics'],
	'Animal': player.skillProfs['animal'],
	'Arcana': player.skillProfs['aracna'],
	'Athletics': player.skillProfs['athletics'],
	'Deception ': player.skillProfs['deception'],
	'History ': player.skillProfs['history'],
	'Insight': player.skillProfs['insight'],
	'Intimidation': player.skillProfs['intimidation'],
	'Investigation ': player.skillProfs['investigation'],
	'Medicine': player.skillProfs['medicine'],
	'Nature': player.skillProfs['nature'],
	'Perception ': player.skillProfs['perception'],
	'Performance': player.skillProfs['performance'],
	'Persuasion': player.skillProfs['persuasion'],
	'Religion': player.skillProfs['religion'],
	'SleightofHand': player.skillProfs['sleight'],
	'Stealth ': player.skillProfs['stealth'],
	'Survival': player.skillProfs['survival'],
	'Passive': player.passivep #Passive Perception
}

writePDF(templatePath, "test.pdf", defaultData)