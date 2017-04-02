import simplejson as json
from flask import Flask, g, jsonify, render_template
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

@app.route("/available/<int:station_id>")
def get_station_data(station_id):
    engine = get_db()
    data = []
    rows = engine.execute("SELECT available_bikes from stations where number = {};".format(station_id))
    for row in rows:
        data.append(dict(row))

    return json.dumps(available=data)


@app.route('/')
def main():
    return render_template('Index.html')


@app.route('/station/<int:station_id>')
def station(station_id):
    # show the station with the given id, the id is an integer

    # this line would just return a simple string echoing the station_id
    # return 'Retrieving info for Station: {}'.format(station_id)

    # select the station info from the db
    sql = """
    select * from StationData where number = {}
    """.format(station_id)
    engine = get_db() 
    rows = engine.execute(sql).fetchall()  # we use fetchall(), but probably there is only one station
    res = [dict(row.items()) for row in rows]  # use this formula to turn the rows into a list of dicts
    return jsonify(data=res)  # jsonify turns the objects into the correct respose

@app.route("/stations") 
def get_stations():
    sql = """
    select * from StationData;
    """
    engine = get_db()
    allrows = engine.execute(sql).fetchall()
    stations = [dict(row.items()) for row in allrows]
    return jsonify(stations=stations)


@app.route("/dbinfo")
def get_dbinfo():
    # this function shows the tables in your database
    sql = """
    SELECT table_name FROM information_schema.tables
    where table_schema='{}';
    """.format(config.DB)
    engine = get_db()
    rows = engine.execute(sql).fetchall()
    res = [dict(row.items()) for row in rows]
    print(res)
    return jsonify(data=res);
   

if __name__ == "__main__":
    """
    The URLs you should visit after starting the app:
    http://1270.0.0.1/ is working - removed
    http://1270.0.0.1/hello is working - removed for now
    http://1270.0.0.1/user - was not working so updated to render tempates and returned the index page that way
    http://1270.0.0.1/dbinfo - - need to change to the pysql done -working
    http://1270.0.0.1/station/42 - need to change to the pysql done - need to include join -done -working
    """
    app.run(debug=True)