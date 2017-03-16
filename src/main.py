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
        for row in data:
            print(row)
            name = row['name']
            status = row['status']
            bike_stands = row['bike_stands']
            available_bike_stands = row['available_bike_stands']
            available_bikes = row['available_bikes']
            last_update = row['last_update']
                    
            starttime=time.time()
            engine = create_engine("mysql+pymysql://Project1Team13:Renault4@project1team13.cldi9otgx37k.us-west-2.rds.amazonaws.com:3306/Project1Team13")
            connection = engine.connect()
           
            while starttime<1489680980800:
                
                try:
                    result_insert = connection.execute('INSERT INTO DublinBikes (name,status,bike_stands,available_bike_stands,available_bikes,last_update) VALUES (name,status,bike_stands,available_bike_stands,available_bikes,last_update)')
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