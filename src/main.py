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

APIKEY = 'a360b2a061d254a3a5891e4415511251899f6df1'
NAME = "Dublin"
STATIONS_URI = "https://api.jcdecaux.com/vls/v1/stations"

def main():
    
    parser=argparse.ArgumentParser()
    parser.add_argument('--input', help='no inputs needed to run code')
    args=parser.parse_args()
    tester=webcrawler()
    tester.create_table()
    tester.store_data()
    
    
class webcrawler:
    
    
    r = requests.get(STATIONS_URI, params={"apiKey": APIKEY,
                                                           "contract": NAME})
    data = (json.loads(r.text))
    engine = create_engine("mysql+mysqldb://project1team13.cldi9otgx37k.us-west-2.rds.amazonaws.com:3306:3306/Project1Team13")
    connection = engine.connect() 

    def create_table(self, connection):
        result_create = connection.execute("CREATE TEMPORARY TABLE IF NOT EXISTS DublinBikes(Number int,Name varchar(255),Address varchar(255),Position varchar(255),Banking varchar(255),Bonus varchar(255),Status varchar(255),ContractName varchar(255),BikeStands int,AvailableBikeStands int,AvailableBikes int,LastUpdate datetime, PRIMARY KEY ('number')"); 
        
    def store_data(self, r, data, engine, connection):
        number = data['number']
        name = data['name']
        address = data['address']
        position = data['position']
        banking = data['banking']
        bonus = data['bonus']
        status = data['status']
        contract_name = data['contract_name']
        bike_stands = data['bike_stands']
        available_bike_stands = data['available_bike_stands']
        available_bikes = data['available_bikes']
        last_update = data['last_update']
        starttime=time.time()
        while True:
            try:
                result_insert = connection.execute('INSERT INTO DublinBikes (number,name,address,position,banking,bonus,status,contract_name,bike_stands,available_bike_stands,available_bikes,last_update) VALUES (number,name,address,position,banking,bonus,status,contract_name,bike_stands,available_bike_stands,available_bikes,last_update)')
                time.sleep(5*60)
                connection.close()
            except:
                print (traceback.format_exc())
        return

    #http://pythondata.com/collecting-storing-tweets-python-mysql/ 
    
    def plain_text_backup(self, data):
        for row in data:
            print ("number:", row['number'],"name:", row['name'],"address:", row['address'],"position:", row['position'],"banking", row['banking'],"bonus", row['bonus'],"status", row['status'],"contract_name",row['contract_name'],"bike_stands",row['bike_stands'],"ailable_bike_stands",row['available_bike_stands'],"available_bikes", row['available_bikes'],"last_update", row['last_update'])
            starttime=time.time()
            lines=row
            filename = '/Users/user/Documents/workspace30670/Dublin_Bikes/backup.txt'
            #this will not work for EC2?
            with open(filename, 'w') as handle:
                handle.writelines(lines)
        
if __name__ == '__main__':
    pass

main()  