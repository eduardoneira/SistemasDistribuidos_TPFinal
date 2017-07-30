import const
from Hash import compute_sha1_hole_byte_at_once
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
    filepath= container_folder+"/"+hash_file+".jpg"
    if not os.path.isfile(file_path):
        image_file = open(file_path, 'w')
        image_file.write(image_data)
        image_file.close()
        return hash_file, false, file_path
    return hash_file, true, file_path
