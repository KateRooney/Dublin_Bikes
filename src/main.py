'''
Created on 15 Mar 2017

this is the web crawler for the dynamic occupancy data for Dublin Bikes 

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
from sqlalchemy.sql.functions import current_timestamp

def main():
    
    parser=argparse.ArgumentParser()
    parser.add_argument('--input', help='no inputs needed to run code')
    args=parser.parse_args()
    tester=webcrawler()
    tester.store_data()

    
class webcrawler:
         

    def store_data(self):
        APIKEY = 'a360b2a061d254a3a5891e4415511251899f6df1'
        NAME = "Dublin"
        STATIONS_URI = "https://api.jcdecaux.com/vls/v1/stations"
        
        r = requests.get(STATIONS_URI, params={"apiKey": APIKEY,
                                                                   "contract": NAME})
        data = (json.loads(r.text))
    
                    
        starttime=time.time()
        #engine = create_engine("mysql+pymysql://Project1Team13:Renault4@project1team13.cldi9otgx37k.us-west-2.rds.amazonaws.com:3306/Project1Team13")
        engine = create_engine("mysql+pymysql://Project3:Project3@project3.ckjtcpr4fsnl.us-west-2.rds.amazonaws.com:3306/Bikes")
        connection = engine.connect()
       
        while starttime<1489680980800:
            
            try:
                for row in data:
                    number= row['number']
                    name = row['name']
                    status = row['status']
                    bike_stands = row['bike_stands']
                    available_bike_stands = row['available_bike_stands']
                    available_bikes = row['available_bikes']
                    banking = row['banking']
                    last_update = row['last_update']
                    connection.execute('INSERT INTO DublinBikes (number, name, status, bike_stands, available_bike_stands,available_bikes, banking, last_update) VALUES (%s,%s, %s, %s,%s, %s, %s, %s)', (number, name, status, bike_stands, available_bike_stands, available_bikes, banking, last_update))
                time.sleep(5*60)
            except:
                print (traceback.format_exc())
        
        return

    #http://pythondata.com/collecting-storing-tweets-python-mysql/ 
    
    def plain_text_backup(self, data):
    
            with open(os.environ['HOME'] + data) as f:
                f.write(data)
                f.close()
        
if __name__ == '__main__':
    pass
main()


