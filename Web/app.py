#!/bin/python3

from flask import (
    Flask,
    request,
    Response,
    render_template,
    send_from_directory,
    send_file,
    url_for,
    jsonify
)
from app_exceptions import *
from flask_googlemaps import GoogleMaps, Map
import os
import sys
import pdb
sys.path.insert(0, '../')
import json
from Factory import *
from rpc_client import *


basedir = os.path.abspath(os.path.dirname(__file__))

app = Flask(__name__)
# you can set key as config
app.config['GOOGLEMAPS_KEY'] = "AIzaSyAZzeHhs-8JZ7i18MjFuM35dJHq70n3Hx4"

# Initialize the extension
GoogleMaps(app)
#Rpc client
with open('./static/config.json') as config_file:
    config = json.load(config_file)
rpc_client = RpcClient(config['HOST_CMC'], config['QUEUE_RPC'])

from logging import Formatter, FileHandler
handler = FileHandler(os.path.join(basedir, 'log.txt'), encoding='utf8')
handler.setFormatter(
    Formatter("[%(asctime)s] %(levelname)-8s %(message)s", "%Y-%m-%d %H:%M:%S")
)
app.logger.addHandler(handler)

app.config['UPLOAD_FOLDER'] = app.root_path +'/upload'
app.config['ALLOWED_EXTENSIONS'] = set(['jpg', 'jpeg', 'JPG', 'JPEG'])

def allowed_file(filename):
  return '.' in filename and \
         filename.rsplit('.', 1)[1] in app.config['ALLOWED_EXTENSIONS']

@app.context_processor
def override_url_for():
  return dict(url_for=dated_url_for)

def dated_url_for(endpoint, **values):
  if endpoint == 'js_static':
    filename = values.get('filename', None)
    if filename:
      file_path = os.path.join(app.root_path,
                               'static/js', filename)
      values['q'] = int(os.stat(file_path).st_mtime)
  if endpoint == 'css_static':
    filename = values.get('filename', None)
    if filename:
      file_path = os.path.join(app.root_path,
                               'static/css', filename)
      values['q'] = int(os.stat(file_path).st_mtime)
  if endpoint == 'fonts_static':
    filename = values.get('filename', None)
    if filename:
      file_path = os.path.join(app.root_path,
                               'static/fonts', filename)
      values['q'] = int(os.stat(file_path).st_mtime)
  return url_for(endpoint, **values)

@app.route('/css/<path:filename>')
def css_static(filename):
  return send_from_directory(app.root_path + '/static/css/', filename)

@app.route('/upload/<path:filename>')
def img_file(filename):
  return send_from_directory(app.config['UPLOAD_FOLDER'], filename)

@app.route('/js/<path:filename>')
def js_static(filename):
  return send_from_directory(app.root_path + '/static/js/', filename)

@app.route('/fonts/<path:filename>')
def fonts_static(filename):
  return send_from_directory(app.root_path + '/static/fonts/', filename)

@app.route('/', methods=['GET','POST'])
def index():
  points = [{"lat": -34.618696, "lng": -58.435593}]
  return render_template("index.html", points=json.dumps(points))
@app.route('/trajectory', methods=['POST'])
def trajectory_request():
    if request.method == 'POST':
      requestManager= RequestManagerFactory.createRequestManager(json.loads(request.data.decode('utf-8')), rpc_client);
      return requestManager.processRequest();
@app.route('/uploadajax', methods=['POST'])
def upldfile():
  if request.method == 'POST':
    requestManager= RequestManagerFactory.createRequestManager(request.form, rpc_client);
    files = request.files.getlist('file[]')
    for f in files:
      if f and allowed_file(f.filename):
        requestManager.appendImage(f);
      else:
        app.logger.info('ext name error')
        return jsonify(error='ext name error')
    return requestManager.processRequest();

@app.errorhandler(VoidRequest)
def handle_void_request(error):
    response = jsonify(error.to_dict())
    response.status_code = error.status_code
    return response

if __name__ == '__main__':
  app.run(debug=True)
  print("voy a borrar")
  print(os.system("ls ./static/images/"))
