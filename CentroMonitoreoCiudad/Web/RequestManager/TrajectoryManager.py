from flask import (
    jsonify
)
import Manager
import const
class TrajectoryManager(Manager.Manager):
    def __init__(self, file, basedir):
        super(TrajectoryManager, self).__init__(file, basedir)
    def processRequest(self):
        if not self.fileExists:
            return jsonify(operation=const.RESPONSEDOESNTEXIST)
        return jsonify(operation=const.RESPONSETRAJECTORY)
