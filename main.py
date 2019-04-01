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
					annotation.update(pdfrw.PdfDict(V='{}'.format(dataDct[key])))

	pdfrw.PdfWriter().write(outputPath, templatePDF)


dataDict = {
	'name': 'TBD',
	'str': 10,
	'dex': 10,
	'con': 10,
	'int': 10,
	'wis': 10,
	'cha': 10,
	'strMod': 0,
	'dexMod': 0,
	'conMod': 0,
	'intMod': 0,
	'wisMod': 0,
	'chaMod': 0,
	'class': [['Fighter', 1]],
	'hp': 10,
	'ac': 10,
	'tempHp': 0
}

