from RequestManager import *
import sys

class RequestManagerFactory:
  @staticmethod
  def createRequestManager(formData,rpc_client):
     type = int(formData['operation']);
     with open('./static/config.json') as config_file:
        config = json.load(config_file)
        if type == config['REQUESTUPLOAD']:
           return UploadManager(rpc_client, formData);
        elif type == config['REQUESTEXISTANCE']:
          return ExistanceManager(rpc_client,formData);
        elif type == config['REQUESTTRAJECTORY']:
          return TrajectoryManager(rpc_client,formData);
