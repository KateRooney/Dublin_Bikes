from flask import Flask, g, jsonify, render_template, url_for
from sqlalchemy import create_engine
import config
from flask_cors import CORS, cross_origin
app = Flask(__name__)
CORS(app)

class Flask():

    #configurations for database connection, also see 'config.py' file in this folder
    def connect_to_database(self, config):
        db_str = "mysql+pymysql://{}:{}@{}:{}/{}"
        engine = create_engine(db_str.format(config.USER,
                                            config.PASSWORD,
                                            config.URI,
                                            config.PORT,
                                            config.DB),
                               echo=True)
    
        return engine
    
    #connection to the database follows - open and close
    def get_db(self):                                                                                                                                                                                                                                                       
        engine = getattr(g, 'engine', None)                                                                                                                                                                                                                              
        if engine is None:                                                                                                                                                                                                                                                  
            engine = g.engine = self.connect_to_database()                                                                                                                                                                                                                    
        return engine                                                                                                                                                                                                                                                      
    
    @app.teardown_appcontext
    def close_connection(self, exception):
        db = getattr(g, '_database', None)
        if db is not None:
            db.close()
    
    #this creates the main index page template - our site has only one page so we have only one template
    @app.route('/')
    def main(self):
        return render_template('Index.html')
    
    #this generates live data per bike station in Dublin, for use in info window on map marker
    @app.route("/stations") 
    @cross_origin()
    def get_stations(self):
        sql = """
        SELECT available_bikes,available_bike_stands, maxDate, StationData.*
        FROM DublinBikes d INNER JOIN 
        StationData ON d.number=StationData.number INNER JOIN
        (SELECT DublinBikes.number, max(Timestamp) as maxDate
        FROM DublinBikes
        GROUP By DublinBikes.number)
        DublinBikes on d.number = DublinBikes.number and d.Timestamp = 
        DublinBikes.maxDate
        ORDER BY DublinBikes.number;
        """
        engine = self.get_db(self)
        avilrows = engine.execute(sql).fetchall()
        stations = [dict(row.items()) for row in avilrows]
        return jsonify(stations=stations)
    
    #this generates average bike availability across the city during peak hours
    #specifically Monday through Friday 8-9am or 5-6pm 
    #for use on pie chart 
    @app.route("/peak") 
    @cross_origin()
    def get_peak(self, engine):
        sql = """ 
        SELECT DublinBikes.number,FLOOR(AVG(available_bikes)) AS peak_bikes_available, FLOOR(AVG(available_bike_stands)) AS peak_bike_stands
        FROM DublinBikes
        WHERE WEEKDAY(Timestamp)<5 AND
        HOUR(Timestamp) = 8 OR HOUR(Timestamp) = 17;
        """
        peak_rows = engine.execute(sql).fetchall()
        peak = [dict(row.items()) for row in peak_rows]
        return jsonify(peak=peak)
      
    #this generates average bike availability across the city during off_peak hours
    #specifically any hours that are not Monday through Friday 8-9am or 5-6pm 
    #for use on pie chart  
    @app.route("/off_peak") 
    @cross_origin()
    def get_off_peak(self, engine):
        sql = """ 
        SELECT DublinBikes.number,FLOOR(AVG(available_bikes)) AS off_peak_bikes_available, FLOOR(AVG(available_bike_stands)) AS off_peak_bike_stands
        FROM DublinBikes
        INNER JOIN StationData ON DublinBikes.number=StationData.number
        WHERE WEEKDAY(Timestamp)>=5 AND
        HOUR(Timestamp) <> 8 OR HOUR(Timestamp) <> 17;
        """
        off_peak_rows = engine.execute(sql).fetchall()
        off_peak = [dict(row.items()) for row in off_peak_rows]
        data = jsonify(off_peak=off_peak)
        return data

#this allows the file to be run from the command line without specifying the host
if __name__ == "__main__":  
    
    app.run(debug=False, host='0.0.0.0')