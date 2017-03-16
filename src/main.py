'''
Created on 15 Mar 2017

@author: user
'''
import requests
import traceback
import json
import argparse
import time
from sqlalchemy import create_engine
import os
import pymysql

APIKEY = 'a360b2a061d254a3a5891e4415511251899f6df1'
NAME = "Dublin"
STATIONS_URI = "https://api.jcdecaux.com/vls/v1/stations"

def main():
    
    parser=argparse.ArgumentParser()
    parser.add_argument('--input', help='no inputs needed to run code')
    args=parser.parse_args()
    tester=webcrawler()
    #tester.create_table(tester.connection)
    tester.store_data(tester.r,tester.data,tester.engine, tester.connection)
    
    
class webcrawler:
    
    
    r = requests.get(STATIONS_URI, params={"apiKey": APIKEY,
                                                           "contract": NAME})
    data = (json.loads(r.text))
    engine = create_engine("mysql+pymysql://Project1Team13:Renault4@project1team13.cldi9otgx37k.us-west-2.rds.amazonaws.com:3306/Project1Team13")
    connection = engine.connect() 

    #def create_table(self, connection):
        #result_create = connection.execute("CREATE TABLE IF NOT EXISTS DublinBikes(number int NOT NULL,name varchar(255),address varchar(255),position varchar(255),banking varchar(255),bonus varchar(255),status varchar(255),contract_name varchar(255),bike_stands int,available_bike_stands int,available_bikes int,last_update datetime);") 
        
    def store_data(self, r, data, engine, connection):
        for row in data:
            number = row['number']
            name = row['name']
            address = row['address']
            position = row['position']
            banking = row['banking']
            bonus = row['bonus']
            status = row['status']
            contract_name = row['contract_name']
            bike_stands = row['bike_stands']
            available_bike_stands = row['available_bike_stands']
            available_bikes = row['available_bikes']
            last_update = row['last_update']
            starttime=time.time()
            while True:
                try:
                    result_insert = connection.execute('INSERT INTO DublinBikes (number,name,address,position,banking,bonus,status,contract_name,bike_stands,available_bike_stands,available_bikes,last_update) VALUES (number,name,address,position,banking,bonus,status,contract_name,bike_stands,available_bike_stands,available_bikes,last_update)')
                    time.sleep(5*60)
                except:
                    print (traceback.format_exc())
            return

    #http://pythondata.com/collecting-storing-tweets-python-mysql/ 
    
    def plain_text_backup(self, data):
    
            with open(os.environ['HOME'] + "/data/{}") as f:
                f.write(data)
                f.close()
        
if __name__ == '__main__':
    pass

main()  