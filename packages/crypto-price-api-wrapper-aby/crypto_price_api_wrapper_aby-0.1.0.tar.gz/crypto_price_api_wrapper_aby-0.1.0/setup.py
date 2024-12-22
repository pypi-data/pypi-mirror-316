from setuptools import setup, find_packages

setup(
    name='crypto-price-api-wrapper-aby',
    version="0.1.0",  
    description="A Python library to fetch cryptocurrency prices from CoinMarketCap",
    author="Aby Varghese",
    author_email="edxfr3q@gmail.com",  
    url="https://github.com/AbyvargheseMandapathel/Crypto-Package",  
    packages=find_packages(where="crypto_price"),  
    package_dir={'': 'crypto_price'},  
    install_requires=[
        "requests>=2.25.1",  
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
   
    package_data={
        '': ['*.py'],
    },
    exclude_package_data={
        '': ['main.py'],  
    }
)
