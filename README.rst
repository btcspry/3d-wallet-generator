3D Wallet Generator
===================

This project helps you design and export 3D-printable wallets, similar to paper wallets (but they won't die in a flood)
-----------------------------------------------------------------------------------------------------------------------

Everyone who's seriously serious about bitcoin has tried paper wallet
generators. While the idea is great, paper isn't a great medium out of
which to make something that stores significant value. This this in
mind, we set out to make a simple, easy-to-use software that can design
and export 3D-printable wallets, with a variety of configuration
options.

Dependencies
------------

-  Python3: this project is designed for Python3, not Python2
-  PyBitcoin, ``sudo pip3 install bitcoin`` **(no manual installation required)**
-  PyQRCode, ``sudo pip3 install pyqrcode`` **(no manual installation required)**
-  OpenSCAD 2015 (or higher), just install from their website, and the
   program should find it automatically (submit an issue if it doesn't) - **(manual installation required)**

Features
--------

-  Supports a variety of configuration and size options
-  Exports wallets as STL
-  Export keys as CSV-file for import into other software (for big
   batches)
-  Set the configuration and let it generate millions of **random**
   wallets for you
-  Support for other cryptocurrencies, including:
	- Bitcoin
	- Litecoin
	- Dogecoin
	- Any other currency (as long as you know the version bit for address generation)

Instructions
------------

1. Install pip
	- Windows: download from their website
	- Mac: install from MacPorts or Brew
	- Linux: ``sudo apt-get install python3-pip``
2. Install OpenSCAD
	- Download from their website (OpenSCad.org/downloads.html)
	- Make sure you are running their newest version (or at least OpenSCAD 2015)
	- Contact us if you need help.  
2. Install our package
	- Try: ``pip install 3d-wallet-generator``
	- If it failes, try: ``pip install 3d-wallet-generator``
	- If it continues to fail, shoot us an email and we'll try to help.
3. Use our package
	- Run ``3dwallet -h`` to see your options
	- Try the default settings by running `3dwallet` - it will output five wallets, with the default settings, into a folder in your current directory.
	- Play with the other settings and decide how your printer, CNC, etc. likes the different styles.
	- Film it or take a picture, and give it to us! We'll add it to our collection!

We recommend you run the Linux version off of a LiveUSB for maximum
security (just as you would with a normal paper wallet).

Miscellaneous
-------------

-  If you have any comments, questions, or feature requests, either
   submit an issue or contact us at btcspry@bitforwarder.com
-  We always accept donations at
   **1MF7hKShzq2iSV9ZZ9hEx6ATnHQpFtM7cF!!** Please donate, this project
   took a bunch of effort and we want to make sure it was worth it.

To Do / Features Coming Soon
----------------------------

-  Add pictures
-  Add option to import your own addresses/private keys
-  Offset the white in the QR code (instead of just offsetting the
   black)
- If you want any of these developed faster, send us a gift to our donation address above.

