from flask import (
    jsonify
)
import os
import Manager
import const
class UploadManager(Manager.Manager):
    def __init__(self, file, basedir):
        super(UploadManager, self).__init__(file, basedir)
    def processRequest(self):
        if self.fileExists:
            return self.responseAlreadyExists();
        self.file.save(os.path.join(self.updir, self.filename))
        return jsonify(operation=const.RESPONSECORRECTLYUPLOADED)
