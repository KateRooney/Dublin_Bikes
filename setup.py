#this initiates the python web scraper but for dynamic data only. 
#static data was served via the static_station_data file as it was to be run just once. 
from setuptools import setup

setup(name="Bikes",
     version ="0.4",
     description="Dublin Bikes Project Team 13",
     url="",
     author="Kate Rooney",
     author_email="kate.rooney1@ucdconnect.ie",
     license="none",
     packages=['src'],
     entry_points={
        'console_scripts':['Bikes=src.main:main']
        },
      )