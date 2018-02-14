# Centro de Monitoreo Barrial

# Install

Élsistema esta pensando para correr dentro de una distribución de Linux. Las dependencias principales son:
* Python3
* Pika (AMPQ client)
* OpenCV

Para instalar todas las dependencias necesarias en Debian/Ubuntu, correr el siguiente comando:

```
sudo ./install.sh
```
# Configuración

Antes de ejecutar un CMB es recomendable configurar los parámetros en el archivo config.json. Allí se puede especificar:
* network:
  * camera_host: ip donde se encuetra el broker que conecta con las cámaras pertinentes 
  * topic_camera: tópico que utiliza Rabbitmq (No modificar) 
  * routing_key_camera: tópico que utiizan las cámaras con el cual distinguen a que CMB envían
  * queue: camToCMB
  * cmc_host: ip donde se encuentra el broker que conecta con el CMC
  * topic_cmc: tópico que utilizan los mensajes de tipo imagen para el CMC
* logger:
  * level: nivel de loggeo
  * save_image: decide si guardar o no todas las imagenes que le lleguen 
* face_cropper:
  * scale_factor : factor de escala para HaarCascadeClassifier
  * min_neighbours : mínima cantidad de vecinos para HaarCascadeClassifier
  * min_size : tamaño mínimo de matriz de pixeles que se espera encontrar la cara
  * default_size : tamaño estándar de foto
  * shrink_factor: factor de recorte de las imagenes
  
# Run

```
python3 main.py
``` 

# Overview

El CMB recibe usando un cliente AMQP los mensajes de las cámaras. Distingue cuales cámaras escucha según la routing key. Esta tiene que coincidir con el tópico de los mensajes MQTT que envían las camaras. Una vez que llega un mensaje trata de buscar caras en la imagén. Para esto ocurre un preprocesamiento en cual la imagén pasa a blanco y negro y se equaliza la luz. Con la imagen resultante se utiliza el clasificador en cascada de Haar que ofrece OpenCV, el cual devuelve un vector de las caras encontradas. Finalmente, se envía un mensaje json del siguiente tipo:

```javascript
{ "timestamp": "17-07-2017||01:09:07.434053", "location": [-34.5884843, -58.3962122], "frame": "base64_image", "faces": [base64_face1, base64_face2, ...]}
```
Este mensaje solo se envia si se detecto alguna cara. Utiliza AMQP como protocolo ya que estamos asumiendo que los CMB van a ser computadoras con mas recursos que las camaras.