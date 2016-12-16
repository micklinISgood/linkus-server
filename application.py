from flask import Flask,request, render_template, g, redirect, Response,jsonify
import os,csv, random,json
from collections import *
from sqlalchemy import *
from sqlalchemy.pool import NullPool
import traceback

tmpl_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'templates')
public_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'static')
app = Flask(__name__, template_folder=tmpl_dir, static_folder=public_dir,static_url_path='')

#connect to database

host = "104.196.175.120" 
password ="rezq8"  
user =  "cl3469" 
DATABASEURI = "postgresql://%s:%s@%s/postgres" % (user, password, host)
movie_meta = {}
genre_hash = defaultdict(lambda: [])
# defaultdict(lambda: [None, None, []])

engine = create_engine(DATABASEURI)
# import logging

# logging.basicConfig()
# logging.getLogger('sqlalchemy.engine').setLevel(logging.INFO)
@app.before_request
def before_request():
  """
  This function is run at the beginning of every web request
  (every time you enter an address in the web browser).
  We use it to setup a database connection that can be used throughout the request
  The variable g is globally accessible
  """
  try:
        g.conn = engine.connect()
  except:
        print "uh oh, problem connecting to database"
        traceback.print_exc()
        g.conn = None

@app.teardown_request
def teardown_request(exception):
  """
  At the end of the web request, this makes sure to close the database connection.
  If you don't the database could run out of memory!
  """
  try:
    g.conn.close()
  except Exception:
    pass

@app.route('/LinkusUser', methods=['GET','POST'])
def LinkusUser():
  try:
    data = json.loads(request.form["data"])
    for k, v in data.items():
      #print k, v
      if k == "id":
        try:
           #print v
           g.conn.execute("INSERT into linkusUser(fbid) values (%s)",v)
        except Exception as e:
          print e


    return jsonify(data="ok"), 200
  except  Exception as e:
         print e

@app.route('/GetLinkusUser', methods=['GET','POST'])
def GetLinkusUser():
  print request
  try:
    for k, v in request.form.items():
      print k, v
    try:
           #print v
           g.conn.execute("Update linkusUser set lat=%s, lng=%s where fbid=%s",request.form["lat"],request.form["lng"],request.form["id"])
    except Exception as e:
          print e
          g.conn.execute("INSERT into linkusUser(lat,lng,fbid) values (%s,%s,%s)",request.form["lat"],request.form["lng"],request.form["id"])
         
    

    return jsonify(data="ok")

  except  Exception as e:
         print e

@app.route('/LinkusUserAct', methods=['POST'])
def LinkusUserAct():
  try:

    return jsonify(data="ok")

  except  Exception as e:
         print e


    


if __name__ == '__main__':
    import click

    @click.command()
    @click.option('--debug', is_flag=True)
    @click.option('--threaded', is_flag=True)
    @click.argument('HOST', default='0.0.0.0')
    @click.argument('PORT', default=7666, type=int)
    def run(debug, threaded, host, port):
        """
        This function handles command line parameters.
        Run the server using

            python server.py

        Show the help text using

            python server.py --help

        """
        HOST, PORT = host, port
        print "running on %s:%d" % (HOST, PORT)
        app.run(host=HOST, port=PORT, debug=debug, threaded=threaded)
   
 
          
    # print movie_meta
    run()
