    #!/usr/bin/python3

from worker import *

def __create_request_upload(self, dni, state, name, surname, images):
    request = {}
    request['type'] = str(self.config['requests']['upload'])
    request['dni'] = dni
    request['state'] = str(self.config['requests'][state])
    request['name'] = name
    request['surname'] = surname
    request['images'] = {}
    for i, image in enumerate(images):
      with open(image, 'rb') as file:
        request['images'][i] = base64.b64encode(file.read()).decode('utf-8')

    return json.dumps(request)

if __name__ == '__main__':
  with open('./config.json') as config_file:
    config = json.load(config_file)

  