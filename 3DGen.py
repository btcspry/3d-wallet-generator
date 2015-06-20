#!/usr/bin/python3

import time
from libs import qr_tools as qrTools
import argparse

def parse_args():
	parser = argparse.ArgumentParser(description='Generate an STL file of a 3D-printable bitcoin, litecoin, dogecoin, or other type of coin.', formatter_class=argparse.RawTextHelpFormatter)
	parser.add_argument('-ve', '--version', dest='version', type=int, default=0, help='Version Bit of the address (for other altcoins).\nBitcoin: 0\n Litecoin: 48\n Dogecoin: 30')
	parser.add_argument('-ct', '--coin-title', dest='coinTitle', type=str, default="Bitcoin", help='Title of the coin, used for design purposes')
	parser.add_argument('-ls', '--layout-style', dest='layoutStyle', type=int, default=1, help="Layout style of the wallet.\n1) Both QR Codes on the Front\n2) Address on the Front, Private Key on the back\n3) Private Key Only\n4) Address Only (don't forget to export the Private Keys after)")
	parser.add_argument('-wi', '--width', dest='walletWidth', type=float, default=54.0, help='The width of the wallet in mm. The length is calculated automatically. Default option is approximately standard credit card legnth and width.')
	parser.add_argument('-he', '--height', dest='walletHeight', type=float, default=8.0, help='The height of the wallet in mm.')
	parser.add_argument('-bo', '--black-offset', dest='blackOffset', type=int, default=-30, help='The percentage of the height that the black part of the QR code, and the text, will be raised or lowered by.\nNegative number for lowered, positive for raised.  This number works best when: -50 < option < 50')
	parser.add_argument('-rc', '--round-corners', dest='roundCorners', action='store_true', help="Round the coners (four short edges) of the wallet.")
	parser.add_argument('-re', '--round-edges', dest='roundEdges', action='store_true', help="Round the eight long edges of the wallet.")
	parser.add_argument('-co', '--copies', dest='copies', type=int, default=5, help='The number of wallets to generate. These will all be unique and randomly-generate wallets (not copies).')
	parser.add_argument('-o', '--stl-folder', dest='outputSTLFolder', type=str, default="./WalletsOut/", help='The output folder to export the STL files into')
	parser.add_argument('-oc', '--scad-folder', dest='outputSCADFolder', type=str, default='', help='The output folder to store the SCAD generation files in (optional, only used for debugging)')
	parser.add_argument('-ea', '--export-address-csv', dest='exportAddressCSV', type=str, default='', help='The output CSV file to export the address list to (optional)')
	parser.add_argument('-ep', '--export-privkey-csv', dest='exportPrivkeyCSV', type=str, default='', help='The output CSV file to export the private key list to (optional)')
	parser.add_argument('-eap', '--export-address-privkey-csv', dest='exportAPCSV', type=str, default='', help='The output CSV file to export the address and private key list to, in the format of "address,privkey" (optional)')
	parser.add_argument('-epa', '--export-privkey-address-csv', dest='exportPACSV', type=str, default='', help='The output CSV file to export the address and private key list to, in the format of "privkey,address" (optional)')
	return parser.parse_args()

args = parse_args()
