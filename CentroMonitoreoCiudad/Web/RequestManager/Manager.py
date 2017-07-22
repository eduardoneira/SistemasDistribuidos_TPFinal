from flask import (
    jsonify
)
import os
import const
from werkzeug import secure_filename
class Manager(object):
    def __init__(self, file, basedir):
        self.file=file
        self.filename = secure_filename(file.filename)
        self.updir = os.path.join(basedir, 'upload/')
        self.filePath= os.path.join(self.updir, self.filename)
        self.fileExists = os.path.isfile(self.filePath)
    def responseAlreadyExists(self):
        imageFile=open(self.filePath, "r")
        data = imageFile.read();
        outJson = {}
        outJson['img']=data.encode('base64')
        outJson['operation']= const.RESPONSEALREADYEXISTS
        imageFile.close()
        return jsonify(outJson);
