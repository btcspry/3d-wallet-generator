#!/usr/bin/python3

try:
    import qr_tools as qrTools # Module for this project
except:
    import gen_3dwallet.qr_tools as qrTools
    
try:
    import TextGenerator as textGen # Module for this project
except:
    import gen_3dwallet.TextGenerator as textGen

import bitcoin # sudo pip3 install bitcoin
import argparse
import time
import math
import sys
import os
import distutils.spawn

def parse_args():
    parser = argparse.ArgumentParser(description='Generate an STL file of a 3D-printable bitcoin, litecoin, dogecoin, or other type of coin.', formatter_class=argparse.RawTextHelpFormatter)
    parser.add_argument('-ve', '--version', dest='versionByte', type=int, default=0, help='Version Bit of the address (for other altcoins).\nBitcoin: 0 (Default)\n Litecoin: 48\n Dogecoin: 30')
    parser.add_argument('-ct', '--coin-title', dest='coinTitle', type=str, default="Bitcoin", help='Title of the coin, used for design purposes \n(Default: Bitcoin)')
    parser.add_argument('-ls', '--layout-style', dest='layoutStyle', type=int, default=1, help="Layout style of the wallet.\n1) Address on the Front, Private Key on the Back (Default)\n2) Private Key Only\n3) Address Only (don't forget to export the Private Keys after)")
    parser.add_argument('-wi', '--width', dest='walletWidth', type=float, default=54.0, help='The width of the wallet in mm. The length is calculated automatically. Default option is approximately standard credit card legnth and width. \n(Default: 54.0)')
    parser.add_argument('-he', '--height', dest='walletHeight', type=float, default=8.0, help='The height of the wallet in mm. \n(Default: 8)')
    parser.add_argument('-bo', '--black-offset', dest='blackOffset', type=int, default=-30, help='The percentage of the height that the black part of the QR code, and the text, will be raised or lowered by.\nNegative number for lowered, positive for raised.  Option must be greater than -90. \n(Default: -20)')
    parser.add_argument('-ec', '--qr-error-correction', dest='errorCorrection', type=str, default="M", help='The percentage of the QR codes that can be destroyed before they are irrecoverable\nL) 7 percent\nM) 15 percent (Default)\nQ) 25 percent\nH) 30 percent')
    parser.add_argument('-dc', '--disable-round-corners', dest='roundCorners', action='store_false', help="Round the coners (four short edges) of the wallet. \n(Default: disabled)")
    parser.add_argument('-co', '--copies', dest='copies', type=int, default=5, help='The number of wallets to generate. These will all be unique and randomly-generate wallets (not copies). \n(Default: 5)')
    parser.add_argument('-sd', '--openscad-exe', dest='scadExe', type=str, default="openscad", help='The location and filename of the command line tools for OpenSCAD (leave as default if it is installed as a command [ie. Linux])\nIn most cases on Windows and Mac, the executable will be found automatically.')
    parser.add_argument('-o', '--stl-folder', dest='outputSTLFolder', type=str, default="./WalletsOut/", help='The output folder to export the STL files into\n(Default: ./WalletsOut/)')
    parser.add_argument('-oc', '--scad-folder', dest='outputSCADFolder', type=str, default='', help='The output folder to store the SCAD generation files in (optional, only used for debugging)\n(Default: disabled)')
    parser.add_argument('-ea', '--export-address-csv', dest='exportAddressCSV', type=str, default='', help='The output CSV file to export the address list to (optional)\n(Default: disabled)')
    parser.add_argument('-ep', '--export-privkey-csv', dest='exportPrivkeyCSV', type=str, default='', help='The output CSV file to export the private key list to (optional)\n(Default: disabled)')
    parser.add_argument('-eap', '--export-address-privkey-csv', dest='exportAPCSV', type=str, default='', help='The output CSV file to export the address and private key list to, in the format of "address,privkey" (optional)\n(Default: disabled)')
    parser.add_argument('-epa', '--export-privkey-address-csv', dest='exportPACSV', type=str, default='', help='The output CSV file to export the address and private key list to, in the format of "privkey,address" (optional)\n(Default: disabled)')
    return parser.parse_args()


def main():
    args = parse_args()

    # Set DEBUG variable for testing purposes (changing styling)
    # If true, prints the SCAD to the terminal and then breaks after first generation
    DEBUG = False

    # Generate the addresses
    if args.copies < 1:
        print("Please enter a valid number of copies (-co flag), and try again.")
        sys.exit()
    else: # Use an else statement here just in case we add the option to import a CSV file with the keys (generated somewhere else)
        walletDataList = []
        for i in range(args.copies):
            thisData = {}

            # Generate the addresses with keys
            thisData["privateKey"] = bitcoin.main.random_key() # Secure: uses random library, time library and proprietary function
            thisData["wif"] = bitcoin.encode_privkey(thisData["privateKey"], "wif", args.versionByte)
            thisData["address"] = bitcoin.privkey_to_address(thisData["privateKey"], args.versionByte)

            # Generate the QR codes
            if args.errorCorrection.upper() not in ["L","M","Q","H"]:
                print("Please select a valid QR Error Correction value (L, M, Q, or H).")
                sys.exit()
            thisData["wifQR"] = qrTools.getQRArray(thisData["wif"], args.errorCorrection.upper())
            thisData["addressQR"] = qrTools.getQRArray(thisData["address"], args.errorCorrection.upper())

            # Reverse them or else they appear backwards (unknown reason)
            thisData["wifQR"] = list(reversed(thisData["wifQR"]))
            thisData["addressQR"] = list(reversed(thisData["addressQR"]))

            # Append ALL the wallet information, just in case we want to do something with it later
            walletDataList.append(thisData) 

    # Validate other args and set some constants
    walletWidth = args.walletWidth
    walletHeight = args.walletHeight
    if args.layoutStyle == 1 or args.layoutStyle == 2 or args.layoutStyle == 3:
        walletLength = walletWidth*1.6 # Approximately the same ratio as a credit card
    else:
        print("Please choose a valid layout style option.")
        sys.exit()
    if args.blackOffset < -90.0:
        print("Please ensure that --black-offset (-bo flag) is set correctly, and is greater than -90.")
        sys.exit()
    textDepth = (args.blackOffset/100) * walletHeight

    # Check the openscad command
    scadExe = args.scadExe
    if args.scadExe == "openscad" and not distutils.spawn.find_executable("openscad"):
        if os.path.isfile("/Applications/OpenSCAD.app/Contents/MacOS/OpenSCAD"):
            print("Info: OpenSCAD found in Applications folder on Mac")
            scadExe = "/Applications/OpenSCAD.app/Contents/MacOS/OpenSCAD"
        elif os.path.isfile("%PROGRAMFILES%\OpenSCAD\openscad.exe"):
            print("Info: OpenSCAD found in Program Files on Windows")
            scadExe = "%PROGRAMFILES%\OpenSCAD\openscad.exe"
        elif os.path.isfile("%PROGRAMFILES(x86)%\OpenSCAD\openscad.exe"):
            print("Info: OpenSCAD found in Program Files (x86) on Windows")
            scadExe = "%PROGRAMFILES(x86)%\OpenSCAD\openscad.exe"
    if not distutils.spawn.find_executable(scadExe):
        print("Please install OpenSCAD or specify the location of it with --openscad-exe.")
        sys.exit()

    # Set the master SCAD variable
    masterSCAD = "// SCAD Code Generated By 3DGen.py - 3D Wallet Generator\n\n" # The beginning of the wallet are identical
    scadOutputs = [] # Generated from loop for each wallet (different addresses)

    # Include some modules at the beginning
    masterSCAD += "// Import some modules\n"
    masterSCAD += """
    $fn=100;
    module createMeniscus(h,radius)difference(){translate([radius/2+0.1,radius/2+0.1,0]){cube([radius+0.2,radius+0.1,h+0.2],center=true);}cylinder(h=h+0.2,r=radius,center=true);}
    module roundCornersCube(x,y,z)translate([x/2,y/2,z/2]){difference(){r=((x+y)/2)*0.052;cube([x,y,z],center=true);translate([x/2-r,y/2-r]){rotate(0){createMeniscus(z,r);}}translate([-x/2+r,y/2-r]){rotate(90){createMeniscus(z,r);}}translate([-x/2+r,-y/2+r]){rotate(180){createMeniscus(z,r);}}translate([x/2-r,-y/2+r]){rotate(270){createMeniscus(z,r);}}}}
    """ # The rounding corners modules for creating a rounded rectangle

    masterSCAD += "\n"

    # Draw the main prism
    if args.roundCorners:
        mainCube = "roundCornersCube(" + str(walletLength) + "," + str(walletWidth) + "," + str(walletHeight) + ");"
    else:
        mainCube = "cube([" + str(walletLength) + "," + str(walletWidth) + "," + str(walletHeight) + "]);"
    mainCube += "\n\n"

    # Init a variable to keep all the additive/subtractive parts
    finalParts = []

    # Init variables to keep the CSV output data in
    addressOut = []
    privkeyOut = []
    APOut = []
    PAOut = []

    # Set a counter for naming the files
    filenameCounter = 1

    # Break into the loop for each wallet
    for data in walletDataList:
        # 'data' = wif, address, wifQR, addressQR

        # Generate the texts
        addressLine1 = data["address"][:math.ceil(len(data["address"])/2.0)]
        addressLine2 = data["address"][math.ceil(len(data["address"])/2.0):]
        wifLine1 = data["wif"][:17]
        wifLine2 = data["wif"][17:34]
        wifLine3 = data["wif"][34:]

        addressLine1Dots = textGen.getArray(addressLine1)
        addressLine2Dots = textGen.getArray(addressLine2)
        privkeyLine1Dots = textGen.getArray(wifLine1)
        privkeyLine2Dots = textGen.getArray(wifLine2)
        privkeyLine3Dots = textGen.getArray(wifLine3)

        bigTitle = textGen.getArray("3D " + args.coinTitle + " Wallet")
        addressTitle = textGen.getArray("Address")
        privkeyTitle = textGen.getArray("Private Key")

        # Create the big title union so that it can be sized and moved
        bigTitleUnion = ""
        for rowIndex in range(len(bigTitle)):
            row = bigTitle[rowIndex]
            for colIndex in range(len(row)):
                if row[colIndex] == '1':
                    translateHeight = walletHeight if textDepth>0 else walletHeight+textDepth
                    bigTitleUnion += "translate([colIndex,rowIndex,translateHeight]){cube([1,1,textDepth]);}".replace('colIndex',str(colIndex)).replace('rowIndex',str(rowIndex)).replace('textDepth',str(abs(textDepth))).replace('translateHeight',str(translateHeight))

        # Translate the title to where it goes
        bigTitleFinal = "translate([(1/17)*length,(14/17)*width,0]){resize([(15/17)*length,0,0],auto=[true,true,false]){bigTitleUnion}}".replace('length',str(walletLength)).replace('width',str(walletWidth)).replace('bigTitleUnion',bigTitleUnion)
        finalParts.append(bigTitleFinal+"\n\n")
        if args.layoutStyle == 1:
            # Need to copy it on to the backside as well - rotate then move it, and then create a union of the two titles (front and back)
            bigTitle2 = "translate([length,0,height]){rotate(180,v=[0,1,0]){bigTitleFinal}}".replace('length',str(walletLength)).replace('height',str(walletHeight)).replace('bigTitleFinal',bigTitleFinal).replace('translateHeight',str(translateHeight))
            finalParts.append(bigTitle2+"\n\n")
        
        # Draw the word "Address" on the front, and draw on the actual address
        if args.layoutStyle == 1 or args.layoutStyle == 3:
            # Draw the address on the front
            addressParts = []

            # Create the address title union and size/move it
            addressTitleUnion = "union(){"
            for rowIndex in range(len(addressTitle)):
                row = addressTitle[rowIndex]
                for colIndex in range(len(row)):
                    if row[colIndex] == '1':
                        translateHeight = walletHeight if textDepth>0 else walletHeight+textDepth
                        addressTitleUnion += "translate([colIndex,rowIndex,translateHeight]){cube([1,1,textDepth]);}".replace('colIndex',str(colIndex)).replace('rowIndex',str(rowIndex)).replace('textDepth',str(abs(textDepth))).replace('translateHeight',str(translateHeight))
            addressTitleUnion += "}"
            addressTitleFinal = "translate([(10/17)*length,(6/11)*width,0]){resize([0,(4/55)*width,0],auto=[true,true,false]){addressTitleUnion}}\n\n".replace('length',str(walletLength)).replace('width',str(walletWidth)).replace('addressTitleUnion',addressTitleUnion)
            addressParts.append(addressTitleFinal)

            # Create the first line of the address
            addressLine1Union = "union(){"
            for rowIndex in range(len(addressLine1Dots)):
                row = addressLine1Dots[rowIndex]
                for colIndex in range(len(row)):
                    if row[colIndex] == '1':
                        translateHeight = walletHeight if textDepth>0 else walletHeight+textDepth
                        addressLine1Union += "translate([colIndex,rowIndex,translateHeight]){cube([1,1,textDepth]);}".replace('colIndex',str(colIndex)).replace('rowIndex',str(rowIndex)).replace('textDepth',str(abs(textDepth))).replace('translateHeight',str(translateHeight))
            addressLine1Union += "}"
            addressLine1Final = "translate([(8.2/17)*length,(5/11)*width,0]){resize([0,(3/55)*width,0],auto=[true,true,false]){addressLine1Union}}\n\n".replace('length',str(walletLength)).replace('width',str(walletWidth)).replace('addressLine1Union',addressLine1Union)
            addressParts.append(addressLine1Final)

            # Create the second line of the address
            addressLine2Union = "union(){"
            for rowIndex in range(len(addressLine2Dots)):
                row = addressLine2Dots[rowIndex]
                for colIndex in range(len(row)):
                    if row[colIndex] == '1':
                        translateHeight = walletHeight if textDepth>0 else walletHeight+textDepth
                        addressLine2Union += "translate([colIndex,rowIndex,translateHeight]){cube([1,1,textDepth]);}".replace('colIndex',str(colIndex)).replace('rowIndex',str(rowIndex)).replace('textDepth',str(abs(textDepth))).replace('translateHeight',str(translateHeight))
            addressLine2Union += "}"
            addressLine2Final = "translate([(8.2/17)*length,(4.1/11)*width,0]){resize([0,(3/55)*width,0],auto=[true,true,false]){addressLine2Union}}\n\n".replace('length',str(walletLength)).replace('width',str(walletWidth)).replace('addressLine2Union',addressLine2Union)
            addressParts.append(addressLine2Final)

            # Create the QR code
            addressQRUnion = "union(){"
            for rowIndex in range(len(data["addressQR"])):
                row = data["addressQR"][rowIndex]
                for colIndex in range(len(row)):
                    if row[colIndex] == 0:
                        translateHeight = walletHeight if textDepth>0 else walletHeight+textDepth
                        addressQRUnion += "translate([colIndex,rowIndex,translateHeight]){cube([1,1,textDepth]);}".replace('colIndex',str(colIndex)).replace('rowIndex',str(rowIndex)).replace('textDepth',str(abs(textDepth))).replace('translateHeight',str(translateHeight))
            addressQRUnion += "}"
            addressQRFinal = "translate([(0.6/17)*length,(0.6/11)*width,0]){resize([0,(8/12)*width,0],auto=[true,true,false]){addressQRUnion}}\n\n".replace('length',str(walletLength)).replace('width',str(walletWidth)).replace('addressQRUnion',addressQRUnion)
            addressParts.append(addressQRFinal)
            
            finalParts.extend(addressParts)

        # Draw all the things having to do with the private key
        if args.layoutStyle == 1 or args.layoutStyle == 2:
            privkeyParts = []

            # Create the privkey title union and size/move it
            privkeyTitleUnion = "union(){"
            for rowIndex in range(len(privkeyTitle)):
                row = privkeyTitle[rowIndex]
                for colIndex in range(len(row)):
                    if row[colIndex] == '1':
                        translateHeight = walletHeight if textDepth>0 else walletHeight+textDepth
                        privkeyTitleUnion += "translate([colIndex,rowIndex,translateHeight]){cube([1,1,textDepth]);}".replace('colIndex',str(colIndex)).replace('rowIndex',str(rowIndex)).replace('textDepth',str(abs(textDepth))).replace('translateHeight',str(translateHeight))
            privkeyTitleUnion += "}"
            privkeyTitleFinal = "translate([(8.7/17)*length,(7/11)*width,0]){resize([0,(4/55)*width,0],auto=[true,true,false]){privkeyTitleUnion}}\n\n".replace('length',str(walletLength)).replace('width',str(walletWidth)).replace('privkeyTitleUnion',privkeyTitleUnion)
            privkeyParts.append(privkeyTitleFinal)

            # Create the first line of the privkey
            privkeyLine1Union = "union(){"
            for rowIndex in range(len(privkeyLine1Dots)):
                row = privkeyLine1Dots[rowIndex]
                for colIndex in range(len(row)):
                    if row[colIndex] == '1':
                        translateHeight = walletHeight if textDepth>0 else walletHeight+textDepth
                        privkeyLine1Union += "translate([colIndex,rowIndex,translateHeight]){cube([1,1,textDepth]);}".replace('colIndex',str(colIndex)).replace('rowIndex',str(rowIndex)).replace('textDepth',str(abs(textDepth))).replace('translateHeight',str(translateHeight))
            privkeyLine1Union += "}"
            privkeyLine1Final = "translate([(8.2/17)*length,(6/11)*width,0]){resize([0,(3/55)*width,0],auto=[true,true,false]){privkeyLine1Union}}\n\n".replace('length',str(walletLength)).replace('width',str(walletWidth)).replace('privkeyLine1Union',privkeyLine1Union)
            privkeyParts.append(privkeyLine1Final)

            # Create the second line of the privkey
            privkeyLine2Union = "union(){"
            for rowIndex in range(len(privkeyLine2Dots)):
                row = privkeyLine2Dots[rowIndex]
                for colIndex in range(len(row)):
                    if row[colIndex] == '1':
                        translateHeight = walletHeight if textDepth>0 else walletHeight+textDepth
                        privkeyLine2Union += "translate([colIndex,rowIndex,translateHeight]){cube([1,1,textDepth]);}".replace('colIndex',str(colIndex)).replace('rowIndex',str(rowIndex)).replace('textDepth',str(abs(textDepth))).replace('translateHeight',str(translateHeight))
            privkeyLine2Union += "}"
            privkeyLine2Final = "translate([(8.2/17)*length,(5.1/11)*width,0]){resize([0,(3/55)*width,0],auto=[true,true,false]){privkeyLine2Union}}\n\n".replace('length',str(walletLength)).replace('width',str(walletWidth)).replace('privkeyLine2Union',privkeyLine2Union)
            privkeyParts.append(privkeyLine2Final)

            # Create the third line of the privkey
            privkeyLine3Union = "union(){"
            for rowIndex in range(len(privkeyLine3Dots)):
                row = privkeyLine3Dots[rowIndex]
                for colIndex in range(len(row)):
                    if row[colIndex] == '1':
                        translateHeight = walletHeight if textDepth>0 else walletHeight+textDepth
                        privkeyLine3Union += "translate([colIndex,rowIndex,translateHeight]){cube([1,1,textDepth]);}".replace('colIndex',str(colIndex)).replace('rowIndex',str(rowIndex)).replace('textDepth',str(abs(textDepth))).replace('translateHeight',str(translateHeight))
            privkeyLine3Union += "}"
            privkeyLine3Final = "translate([(8.2/17)*length,(4.2/11)*width,0]){resize([0,(3/55)*width,0],auto=[true,true,false]){privkeyLine3Union}}\n\n".replace('length',str(walletLength)).replace('width',str(walletWidth)).replace('privkeyLine3Union',privkeyLine3Union)
            privkeyParts.append(privkeyLine3Final)

            # Create the QR code
            privkeyQRUnion = "union(){"
            for rowIndex in range(len(data["wifQR"])):
                row = data["wifQR"][rowIndex]
                for colIndex in range(len(row)):
                    if row[colIndex] == 0:
                        translateHeight = walletHeight if textDepth>0 else walletHeight+textDepth
                        privkeyQRUnion += "translate([colIndex,rowIndex,translateHeight]){cube([1,1,textDepth]);}".replace('colIndex',str(colIndex)).replace('rowIndex',str(rowIndex)).replace('textDepth',str(abs(textDepth))).replace('translateHeight',str(translateHeight))
            privkeyQRUnion += "}"
            privkeyQRFinal = "translate([(0.6/17)*length,(0.6/11)*width,0]){resize([0,(8/12)*width,0],auto=[true,true,false]){privkeyQRUnion}}\n\n".replace('length',str(walletLength)).replace('width',str(walletWidth)).replace('privkeyQRUnion',privkeyQRUnion)
            privkeyParts.append(privkeyQRFinal)

            if args.layoutStyle == 2:
                # Just add it all to the finalParts
                finalParts.extend(privkeyParts)
            elif args.layoutStyle == 1:
                # Rotate it all and then add it to the finalParts
                privkeyPartsNew = []
                for part in privkeyParts:
                    privkeyPartsNew.append("translate([length,0,height]){rotate(180,v=[0,1,0]){part}}".replace('length',str(walletLength)).replace('height',str(walletHeight)).replace('part',part).replace('translateHeight',str(translateHeight)))
                finalParts.extend(privkeyPartsNew)

        # Put it all together
        finalSCAD = masterSCAD
        if textDepth < 0:
            finalSCAD += "difference() {\n\n"
        else:
            finalSCAD += "union() {\n\n"
        finalSCAD += mainCube
        finalSCAD += "".join(finalParts)
        finalSCAD += "}"

        if DEBUG:
            print(finalSCAD)
            break

        if args.outputSCADFolder:
            try:
                os.makedirs(args.outputSCADFolder)
            except FileExistsError:
                pass
            scadOutFile = open(args.outputSCADFolder + '/wallet' + str(filenameCounter) + '.scad','w')
            scadOutFile.write(finalSCAD)
            scadOutFile.close()

        # Log some info
        print("Status: Done generating data for wallet #" + str(filenameCounter) + "...Starting generating STL file")

        if args.outputSTLFolder:
            try:
                os.makedirs(args.outputSTLFolder)
            except FileExistsError:
                pass
            scadOutFile = open('temp.scad','w')
            scadOutFile.write(finalSCAD)
            scadOutFile.close()
            os.system(scadExe + " -o " + args.outputSTLFolder + "/wallet" + str(filenameCounter) + ".stl temp.scad")
            try:
                os.remove('temp.scad')
            except:
                pass
        else:
            print("Please provide a folder to output the STL files.")

        # Update the CSV file variables
        addressOut.append(data["address"])
        privkeyOut.append(data["wif"])
        APOut.append(data["address"] + "," + data["wif"])
        PAOut.append(data["wif"] + "," + data["address"])

        # Print some more stats
        print("Status: Done generating STL file (" + str(round(filenameCounter/args.copies*100)) + "% done)")

        filenameCounter += 1

    # Export the CSV files
    if args.exportAddressCSV:
        csvFile = open(args.exportAddressCSV,'a')
        csvFile.write(','.join(addressOut))
        csvFile.close()

    if args.exportPrivkeyCSV:
        csvFile = open(args.exportPrivkeyCSV,'a')
        csvFile.write(','.join(privkeyOut))
        csvFile.close()

    if args.exportAPCSV:
        csvFile = open(args.exportAPCSV,'a')
        csvFile.write('\n'.join(exportAPCSV))
        csvFile.close()

    if args.exportPACSV:
        csvFile = open(args.exportPACSV,'a')
        csvFile.write('\n'.join(exportPACSV))
        csvFile.close()


