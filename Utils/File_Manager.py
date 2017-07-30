import os
import Utils.const
from Utils.Hash import compute_sha1_hole_byte_at_once
"""
Pre: Recibe el contenido de la imagen como una tira de bytes.
Post: Calcula el hash de los bytes recibido. El hash es el nombre del archivo.
Si el archivo ya existia en la carpeta contenedora, entonces devuelve el hash de
correspondiente, true indicando que es cierto que el archivo ya existia y el filepath.
Si el archivo no existia, lo crea y devuelve el has correspondiente, false
indicando que el archivo no existia de antemano y el filepath
"""
def save_data_to_file(image_data, container_folder):
    hash_file = compute_sha1_hole_byte_at_once(image_data)
    basedir=os.path.dirname(os.path.abspath(__file__))
    filepath= basedir+"/../CentroMonitoreoCiudad"+container_folder+"/"+hash_file+".jpg"
    if not os.path.isfile(filepath):
        image_file = open(filepath, 'w')
        image_file.write(image_data)
        image_file.close()
        return hash_file, False, filepath
    return hash_file, True, filepath
