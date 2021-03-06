#! /usr/bin/python3

import os
import pdfrw
import PlayerCharacter as pc
import json
import register

templatePath = 'template.pdf'

annotMarker = '/Annots'
fieldMarker = '/T'
subMarker = '/Subtype'
widgetMarker = '/Widget'

def writePDF(inputPath, outputPath, dataDict):
	"""Function to fill in the forms of a PDF with values from Dict.
	
	:param inputPath: Path of template PDF
	:param outputPath: Path to make new PDF at
	:param dataDict: Dictionary with keys with same name as form fields.
	"""
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
register.registerOptions(player)

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
	'Equipment': "\n".join(player.equipment),
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
	'Acrobatics': player.skillProfs['acrobatics'][1],
	'Animal': player.skillProfs['animal'][1],
	'Arcana': player.skillProfs['aracna'][1],
	'Athletics': player.skillProfs['athletics'][1],
	'Deception ': player.skillProfs['deception'][1],
	'History ': player.skillProfs['history'][1],
	'Insight': player.skillProfs['insight'][1],
	'Intimidation': player.skillProfs['intimidation'][1],
	'Investigation ': player.skillProfs['investigation'][1],
	'Medicine': player.skillProfs['medicine'][1],
	'Nature': player.skillProfs['nature'][1],
	'Perception ': player.skillProfs['perception'][1],
	'Performance': player.skillProfs['performance'][1],
	'Persuasion': player.skillProfs['persuasion'][1],
	'Religion': player.skillProfs['religion'][1],
	'SleightofHand': player.skillProfs['sleight'][1],
	'Stealth ': player.skillProfs['stealth'][1],
	'Survival': player.skillProfs['survival'][1],
	'Passive': player.passivep #Passive Perception
}

writePDF(templatePath, "test.pdf", defaultData)