import sys
import hashlib
import const

class Hash:
    def __init__(self, file_path):
        self.file_path= file_path
        self.sha1 = hashlib.sha1()
    def compute(self):
        with open(self.file_Path) as f:
            while True:
                data = f.read(BUFFER_SIZE)
                if not data:
                    break
                sha1.update(data)
        return sha1.hexdigest()
