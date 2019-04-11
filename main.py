#! /usr/bin/python3

import os
import pdfrw
import PlayerCharacter as pc

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

player = pc.PlayerCharacter()

defaultData = {
	'CharacterName': player.name,
	'STR': player.str,
	'STRmod': player.strmod,
	'DEX': player.dex,
	'DEXmod ': player.dexmod,
	'CON': player.con,
	'CONmod': player.conmod,
	'INT': player.int,
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
	'Passive': player.passivep, #Passive Perception
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
	'ST Dexterity': player.stdex
	'ST Constitution': player.stcon,
	'ST Intelligence': player.stint,
	'ST Wisdom': player.stwis,
	'ST Charisma': player.stcha,
	'Acrobatics': player.acro,
	'Animal': player.animal,
	'Arcana': player.aracna,
	'Athletics': player.athletics,
	'Deception ': player.deception,
	'History ': player.history,
	'Insight': player.insight,
	'Intimidation': player.intimidation,
	'Investigation ': player.investigation,
	'Medicine': player.medicine,
	'Nature': player.nature,
	'Perception ': player.perception,
	'Performance': player.performance,
	'Persuasion': player.persuasion,
	'Religion': player.religion,
	'SleightofHand': player.sleight,
	'Stealth ': player.stealth,
	'Survival': player.survival
}

writePDF(templatePath, "test.pdf", defaultData)