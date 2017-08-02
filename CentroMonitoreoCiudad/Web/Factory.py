from RequestManager import *
import sys
sys.path.insert(0, '../../')
import Utils.const as CONST

class RequestManagerFactory:
  @staticmethod
  def createRequestManager(type, file,rpc_client,state):
    if type == CONST.REQUESTUPLOAD:
      return UploadManager(file,rpc_client,type,state);
    elif type == CONST.REQUESTEXISTANCE:
      return ExistanceManager(file,rpc_client,type);
    elif type == CONST.REQUESTTRAJECTORY:
      return TrajectoryManager(file,rpc_client,type);