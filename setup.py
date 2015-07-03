from setuptools import setup

long_description = open('README.rst').read()

setup(
    name = '3d-wallet-generator',
    packages = ['gen_3dwallet'],
    version = '0.1.21',
    description = 'A tool to help you design and export 3D-printable bitcoin/cryptocurrency wallets',
    long_description=long_description,
    author = 'BTC Spry',
    author_email = 'btcspry@bitforwarder.com',
    url = 'https://github.com/btcspry/3d-wallet-generator',
    install_requires=["bitcoin>=1.1.29","PyQrCode>=1.1"],
    keywords = ['bitcoin','litecoin','dogecoin','wallet','3d printer','cryptocurrency','altcoin','money'],
    classifiers = ["Programming Language :: Python :: 3 :: Only","License :: OSI Approved :: MIT License","Operating System :: OS Independent","Intended Audience :: End Users/Desktop","Environment :: Console","Development Status :: 4 - Beta","Topic :: Utilities"],
    entry_points={
        'console_scripts': [
            '3dwallet = gen_3dwallet.base:main',
        ],
    },
)
