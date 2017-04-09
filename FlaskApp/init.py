import simplejson as json
from flask import Flask, g, jsonify, render_template, url_for
from sqlalchemy import create_engine
import config

app = Flask(__name__)

def connect_to_database():
    db_str = "mysql+pymysql://{}:{}@{}:{}/{}"
    engine = create_engine(db_str.format(config.USER,
                                        config.PASSWORD,
                                        config.URI,
                                        config.PORT,
                                        config.DB),
                           echo=True)

    return engine


def get_db():                                                                                                                                                                                                                                                       
    engine = getattr(g, 'engine', None)                                                                                                                                                                                                                              
    if engine is None:                                                                                                                                                                                                                                                  
        engine = g.engine = connect_to_database()                                                                                                                                                                                                                    
    return engine                                                                                                                                                                                                                                                      

@app.teardown_appcontext
def close_connection(exception):
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()

@app.route('/')
def main():
    return render_template('Index.html')

@app.route('/main')
def main_return():
    return render_template('Index.html')

@app.route('/PeakPage')
def peak_page():
    return render_template('PeakPage.html')

@app.route('/OffPeakPage')
def off_peak_page():
    return render_template('OffPeakPage.html')

@app.route("/stations") 
def get_stations():
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
    engine = get_db()
    avilrows = engine.execute(sql).fetchall()
    stations = [dict(row.items()) for row in avilrows]
    return jsonify(stations=stations)

@app.route("/peak") 
def get_peak():
    sql = """ 
    SELECT DublinBikes.number,FLOOR(AVG(available_bikes)),available_bike_stands, StationData.*
    FROM DublinBikes
    INNER JOIN StationData ON DublinBikes.number=StationData.number
    WHERE WEEKDAY(Timestamp)<5 AND
    HOUR(Timestamp) = 8 OR HOUR(Timestamp) = 17
    GROUP BY DublinBikes.number;
    """
    engine = get_db()
    peak_rows = engine.execute(sql).fetchall()
    peak = [dict(row.items()) for row in peak_rows]
    return jsonify(peak=peak)

@app.route("/off_peak") 
def get_off_peak():
    sql = """ 
    SELECT DublinBikes.number,FLOOR(AVG(available_bikes)),available_bike_stands, StationData.*
    FROM DublinBikes
    INNER JOIN StationData ON DublinBikes.number=StationData.number
    WHERE WEEKDAY(Timestamp)>=5 AND
    HOUR(Timestamp) <> 8 OR HOUR(Timestamp) <> 17
    GROUP BY DublinBikes.number;
    """
    engine = get_db()
    off_peak_rows = engine.execute(sql).fetchall()
    off_peak = [dict(row.items()) for row in off_peak_rows]
    return jsonify(off_peak=off_peak)

if __name__ == "__main__":
    
    app.run(debug=True)