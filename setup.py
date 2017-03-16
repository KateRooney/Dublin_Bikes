from setuptools import setup

setup(name="Bikes",
     version ="0.2",
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