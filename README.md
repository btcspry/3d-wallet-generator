# 3D Wallet Generator
##This project helps you design and export 3D-printable wallets, similar to paper wallets (but they won't die in a flood)

Everyone who's seriously serious about bitcoin has tried paper wallet generators.  While the idea is great, paper isn't a great medium out of which to make something that stores significant value.  This this in mind, we set out to make a simple, easy-to-use software that can design and export 3D-printable wallets, with a variety of configuration options.

## Dependencies
- Python3: this project is designed for Python3, not Python2
- PyBitcoin, just run `sudo pip3 install bitcoin`
- PyQRCode, just run `sudo pip3 install pyqrcode`
- OpenSCAD 2015 (or higher), just install from their website, and the program should find it automatically (submit an issue if it doesn't)

## Features
- Supports a variety of configuration and size options
- Exports wallets as STL
- Export keys as CSV-file for import into other software (for big batches)
- Set the configuration and let it generate millions of **random** wallets for you
- Support for other cryptocurrencies, including:
  - Bitcoin
  - Litecoin
  - Dogecoin
  - Any other currency (as long as you know the version bit for address generation)

## Instructions (releases coming soon - not yet available)
### *Windows*
1. Download the Windows binary from the `Releases` folder.
2. Run the executable file, and enjoy!

### *Mac*
1. Download the Mac binary (DMG archive) from the `Releases` folder.
2. Drag the application to your applications folder.
3. Run the application, and enjoy!

### *Linux*
We recommend you run the linux version off of a LiveUSB for maximum security (just as you would with a normal paper wallet)
1. Connect to the internet.
2. Run `sudo apt-get install 3d-wallet-generator` in a Terminal.
3. *Disconnect from the internet!*
4. Run `gen3dwallet` in a Terminal.
5. Enjoy!  Don't connect this device to the internet again after you have created your wallet.

## Miscellaneous
- If you have any comments, questions, or feature requests, either submit an issue or contact us at btcspry@bitforwarder.com
- We always accept donations at **1MF7hKShzq2iSV9ZZ9hEx6ATnHQpFtM7cF!!**  Please donate, this project took a bunch of effort and we want to make sure it was worth it.

## To Do / Features Coming Soon
- Add pictures
- Add option to import your own addresses/private keys
- Offset the white in the QR code (instead of just offsetting the black)