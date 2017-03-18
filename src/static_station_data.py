import requests
import json
from sqlalchemy import create_engine
import os
import pymysql     

APIKEY = 'a360b2a061d254a3a5891e4415511251899f6df1'
NAME = "Dublin"
STATIONS_URI = "https://api.jcdecaux.com/vls/v1/stations"
r = requests.get(STATIONS_URI, params={"apiKey": APIKEY,
                                                            "contract": NAME})
data = (json.loads(r.text))
engine = create_engine("mysql+pymysql://Project1Team13:Renault4@project1team13.cldi9otgx37k.us-west-2.rds.amazonaws.com:3306/Project1Team13")
connection = engine.connect()

for row in data:
    name = row['name']
    lat = row['position']['lat']
    lon = row['position']['lng']
    #connection.execute('INSERT INTO StationData(name, lat, lon) VALUES (%s,%s, %s)', (name, lat, lon))  
    print([lat, lon, name])
