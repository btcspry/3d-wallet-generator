#!/usr/bin/python3

import pyqrcode # sudo pip3 install pyqrcode

def getQRArray(text, errorCorrection):
	""" Takes in text and errorCorrection (letter), returns 2D array of the QR code"""
	# White is True (1)
	# Black is False (0)
	# ECC: L7, M15, Q25, H30

	# Create the object
	qr = pyqrcode.create(text, error=errorCorrection)

	# Get the terminal representation and split by lines (get rid of top and bottom white spaces)
	plainOut = qr.terminal().split("\n")[5:-5]

	# Initialize the output 2D list
	out = []

	for line in plainOut:
		thisOut = []
		for char in line:
			if char == u'7':
				# This is white
				thisOut.append(1)
			elif char == u'4':
				# This is black, it's part of the u'49'
				thisOut.append(0)
		# Finally add everything to the output, stipping whitespaces at start and end
		out.append(thisOut[4:-4])

	# Everything is done, return the qr code list
	return out