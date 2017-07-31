import sys
import hashlib
import Utils.const as CONST

def compute_sha1_from_file(file_path):
    sha1 = hashlib.sha1()
    with open(file_path, 'rb') as f:
        while True:
            data = f.read(CONST.BUFFER_SIZE)
            if not data:
                break
            sha1.update(data)
    return sha1.hexdigest()
def compute_sha1_hole_byte_at_once(image_byte):
    sha1 = hashlib.sha1()
    sha1.update(image_byte.encode('utf-8'))
    return sha1.hexdigest()
