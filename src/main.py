'''
Created on 15 Mar 2017

@author: user
'''
import requests
import traceback
import json
from pprint import pprint
import argparse
import time
from sqlalchemy import create_engine

APIKEY = 'a360b2a061d254a3a5891e4415511251899f6df1'
NAME = "Dublin"
STATIONS_URI = "https://api.jcdecaux.com/vls/v1/stations"

def main():
    
    parser=argparse.ArgumentParser()
    parser.add_argument('--input', help='no inputs needed to run code')
    args=parser.parse_args()
    
   
    
    while True:
        try:
            r = requests.get(STATIONS_URI, params={"apiKey": APIKEY,
                                                   "contract": NAME})
            data = (json.loads(r.text))

            engine = create_engine("mysql+mysqldb://project1team13.cldi9otgx37k.us-west-2.rds.amazonaws.com:3306:3306/Project1Team13")
            connection = engine.connect()
            result = connection.execute("CREATE TABLE DublinBikes(Number int,Name varchar(255),Address varchar(255),Position varchar(255),Banking varchar(255),Bonus varchar(255),Status varchar(255),ContractName varchar(255),BikeStands int,AvailableBikeStands int,AvailableBikes int,LastUpdate datetime)");

            for row in data:
                print (row['number'])
                print (row['name'])
                print (row['address'])
                print (row['position'])
                print (row['banking'])
                print (row['bonus'])
                print (row['status'])
                print (row['contract_name'])
                print (row['bike_stands'])
                print (row['available_bike_stands'])
                print (row['available_bikes'])
                print (row['last_update'])
            
            time.sleep(5*60)
        
            connection.close()
        except:
            print (traceback.format_exc())
    return
    


if __name__ == '__main__':
    pass