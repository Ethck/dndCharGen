#! /usr/bin/python3

import os
import pdfrw

templatePath = 'template.pdf'

annotKey = '/Annots'
aFieldKey = '/T'
subtypeKey = '/Subtype'
wSubKey = '/Widget'

def writePDF(inputPath, outputPath, dataDict):
	templatePDF = pdfrw.PdfReader(inputPath)
	annotations = templatePDF.pages[0][annotKey]
	for annotation in annotations:
		if annotation[subtypeKey] == wSubKey:
			if annotation[aFieldKey]:
				key = annotation[aFieldKey][1:-1]
				if key in dataDict.keys():
					annotation.update(pdfrw.PdfDict(V='{}'.format(dataDict[key])))

	pdfrw.PdfWriter().write(outputPath, templatePDF)


dataDict = {
	'CharacterName': 'TBD',
	'STR': 10,
	'STRmod': 0,
	'DEX': 10,
	'DEXmod ': 0,
	'CON': 10,
	'CONmod': 0,
	'INT': 10,
	'INTmod': 0,
	'WIS': 10,
	'WISmod': 0,
	'CHA': 10,
	'CHamod': 0,
	'ClassLevel': [['Fighter', 1], ['Wizard', 10]],
	'Background': None,
	'PlayerName': None,
	'Race ': "Aasimar",
	'Alignment': None,
	'XP': 0,
	'AC': 10,
	'Initiative': 0,
	'Speed': 30,
	'HPMax': 10,
	'HPCurrent': 10,
	'HPTemp': 0,
	'HDTotal': 1,
	'HD': 1,
	'PersonalityTraits ': "abc",
	'Ideals': "a",
	'Bonds': "a",
	'Flaws': "a",
	'Passive': 10, #Passive Perception
	'ProficienciesLang': ["a"],
	'Features and Traits': ["a"],
	'Equipment': "Studded Leather Armor\n Shield\n",
	'CP': 0,
	'SP': 0,
	'EP': 0,
	'GP': 0,
	'PP': 0,
	'AttacksSpellcasting': "a",
	'Wpn Name': "a",
	'Wpn Name 2': "a",
	'Wpn Name 3': "a",
	'Wpn1 AtkBonus': 0,
	'Wpn2 AtkBonus ': 0,
	'Wpn3 AtkBonus  ': 0,
	'Wpn1 Damage': "a",
	'Wpn2 Damage ': "a",
	'Wpn3 Damage ': "a",
	'Inspiration': "0",
	'ProfBonus': 2,
	'ST Strength': 0,
	'ST Dexterity': 0,
	'ST Constitution': 0,
	'ST Intelligence': 0,
	'ST Wisdom': 0,
	'ST Charisma': 0,
	'Acrobatics': 0,
	'Animal': 0,
	'Arcana': 0,
	'Athletics': 0,
	'Deception ': 0,
	'History ': 0,
	'Insight': 0,
	'Intimidation': 0,
	'Investigation ': 0,
	'Medicine': 0,
	'Nature': 0,
	'Perception ': 0,
	'Performance': 0,
	'Persuasion': 0,
	'Religion': 0,
	'SleightofHand': 0,
	'Stealth ': 0,
	'Survival': 0
}

writePDF(templatePath, "test.pdf", dataDict)