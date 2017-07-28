from RequestManager import *
import sys
sys.path.insert(0, '../../')
import Utils.const as CONST
class RequestManagerFactory:
    @staticmethod
    def createRequestManager(type, file, basedir):
        if type == CONST.REQUESTUPLOAD:
            return UploadManager(file, basedir);
        elif type == CONST.REQUESTEXISTANCE:
            return ExistanceManager(file, basedir);
        elif type == CONST.REQUESTTRAJECTORY:
            return TrajectoryManager(file, basedir);
