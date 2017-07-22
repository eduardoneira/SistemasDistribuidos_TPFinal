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
class TrajectoryManager(Manager):
    def __init__(self, file, basedir):
        super(TrajectoryManager, self).__init__(file, basedir)
    def processRequest(self):
        if not self.fileExists:
            return jsonify(operation=const.RESPONSEDOESNTEXIST)
        return jsonify(operation=const.RESPONSETRAJECTORY)
class UploadManager(Manager):
    def __init__(self, file, basedir):
        super(UploadManager, self).__init__(file, basedir)
    def processRequest(self):
        if self.fileExists:
            return self.responseAlreadyExists();
        self.file.save(os.path.join(self.updir, self.filename))
        return jsonify(operation=const.RESPONSECORRECTLYUPLOADED)
class ExistanceManager(Manager):
    def __init__(self, file, basedir):
        super(ExistanceManager, self).__init__(file, basedir)
    def processRequest(self):
        if self.fileExists:
            return self.responseAlreadyExists();
        return jsonify(operation=const.RESPONSEDOESNTEXIST)
