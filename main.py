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

