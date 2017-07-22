from flask import (
    jsonify
)
import const
import Manager
class ExistanceManager(Manager.Manager):
    def __init__(self, file, basedir):
        super(ExistanceManager, self).__init__(file, basedir)
    def processRequest(self):
        if self.fileExists:
            return self.responseAlreadyExists();
        return jsonify(operation=const.RESPONSEDOESNTEXIST)
