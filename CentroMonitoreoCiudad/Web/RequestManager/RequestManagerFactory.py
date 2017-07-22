import const
import UploadManager
import ExistanceManager
import TrajectoryManager
class RequestManagerFactory:
    @staticmethod
    def createRequestManager(type, file, basedir):
        if type == const.REQUESTUPLOAD:
            return UploadManager.UploadManager(file, basedir);
        elif type == const.REQUESTEXISTANCE:
            return ExistanceManager.ExistanceManager(file, basedir);
        elif type == const.REQUESTTRAJECTORY:
            return TrajectoryManager.TrajectoryManager(file, basedir);
