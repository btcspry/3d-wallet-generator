from distutils.core import setup
setup(
  name = '3d_wallet',
  packages = ['3d_wallet'], # this must be the same as the name above
  version = '0.1.1',
  description = 'A tool to help you design and export 3D-printable wallets',
  author = 'BTC Spry',
  author_email = 'btcspry@bitforwarder.com',
  url = 'https://github.com/btcspry/3d-wallet-generator',
  download_url = 'https://github.com/btcspry/3d-wallet-generator/tarball/0.1',
  keywords = ['bitcoin','litecoin','dogecoin','wallet','3d printer','cryptocurrency','altcoin','money'],
  classifiers = ["Programming Language :: Python :: 3","License :: OSI Approved :: MIT License","Operating System :: OS Independent","Intended Audience :: End Users/Desktop","Environment :: Console","Development Status :: 4 - Beta","Topic :: Utilities"],
)