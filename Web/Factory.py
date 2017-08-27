from RequestManager import *
import sys
sys.path.insert(0, '../')
import Utils.const as CONST

class RequestManagerFactory:
  @staticmethod
  def createRequestManager(formData,rpc_client):
    type = int(formData['operation']);
    if type == CONST.REQUESTUPLOAD:
      return UploadManager(rpc_client, formData);
    elif type == CONST.REQUESTEXISTANCE:
      return ExistanceManager(rpc_client,formData);
    elif type == CONST.REQUESTTRAJECTORY:
      return TrajectoryManager(rpc_client,formData);
