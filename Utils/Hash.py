import sys
import hashlib
import Utils.const as CONST

class Sha1:
    def __init__(self):
        self.sha1 = hashlib.sha1()
    def compute(self, file_path):
        self.file_path= file_path
        with open(self.file_path, 'rb') as f:
            while True:
                data = f.read(CONST.BUFFER_SIZE)
                if not data:
                    break
                self.sha1.update(data)
        return self.sha1.hexdigest()
