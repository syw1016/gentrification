import json
from collections import OrderedDict
from flask import (Flask, render_template,
      make_response,
      redirect,
      request)

app = Flask(__name__)

#################################################
# Database Setup
#################################################
from flask_sqlalchemy import SQLAlchemy

#################################################
# Flask Routes
#################################################
@app.route('/')
def index():
  return render_template('index.html')

@app.route('/migration')
def migrationHome():
  return render_template('migration.html')
  
@app.route('/migration/<stmtId>')
@app.route('/migration/<int:stmtId>/<st>')
def migration(stmtId, st=None):
  """stmtId: statement identifier
  st: state

  """
  lmt = 10
  results = db.session.query(migration.c.County_Name,
                            migration.c.State_Name,
                            migration.c.Geo_Lng, 
                            migration.c.Geo_Lat,
                            migration.c.Color, 
                            migration.c.Total)
  if stmtId == '-1':
    # all migrating
    results = results.order_by(migration.c.Total).limit(50).all()
  elif stmtId == 0:
      # filter includes migration going to the selected state
      results = results.filter(migration.c.State_Name == st).order_by(migration.c.Total).limit(lmt).all()
  elif stmtId == 1:
      # filter excludes migration going to the selected state
      #variable limit query results for those leaving, excludes a particular state
      results = results.filter(migration.c.State_Name != st).order_by(migration.c.Total).limit(lmt).all()
  elif stmtId == 10:
    # asian, Top 10
    results = results.order_by(migration.c.Asian_Alone).limit(lmt).all()
  elif stmtId == 11:
    # black Top 10
    results = results.order_by(migration.c.Black_or_African_American_Alone).limit(lmt).all()
  elif stmtId == 12:
    # hispanic Top 10
    results = results.order_by(migration.c.Hispanic_or_Latino).limit(lmt).all()
  elif stmtId == 13:
    # white Top 10
    results = results.order_by(migration.c.White_Alone).limit(lmt).all()
  elif stmtId == 3:
    # correlate Top 10
    pass
  migration_routes = []
  for index, res in enumerate(results):
    destination_county = res[0]
    lng = res[2]
    lat = res[3]
    colour = res[4] 
    
    route = OrderedDict()
  
    if index == 0: 
        route = {'from':[-118.2705,33.9984],'to':[lng, lat],'labels':['Los Angeles', destination_county], 'color': "{}".format(colour)}
    else:
        route = {'from':[-118.2705,33.9984],'to':[lng, lat],'labels':['', destination_county], 'color': "{}".format(colour)}

    migration_routes.append(route)

  return make_response(json.dumps(migration_routes))

if __name__ == "__main__":
    app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///migration.sqlite"

    db = SQLAlchemy(app)

    db.metadata.reflect(db.engine)
    #create tables
    migration = db.metadata.tables['migration']

    #app.run(debug=True)
    app.run()