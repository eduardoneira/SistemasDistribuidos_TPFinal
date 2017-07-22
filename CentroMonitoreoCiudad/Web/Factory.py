import const
from RequestManager import *
class RequestManagerFactory:
    @staticmethod
    def createRequestManager(type, file, basedir):
        if type == const.REQUESTUPLOAD:
            return UploadManager(file, basedir);
        elif type == const.REQUESTEXISTANCE:
            return ExistanceManager(file, basedir);
        elif type == const.REQUESTTRAJECTORY:
            return TrajectoryManager(file, basedir);
