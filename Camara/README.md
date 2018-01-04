# Cámara de Vigilancia

# Install

Este sistema esta pensado para correr dentro de una raspberry pi con Raspbian con python3. Sin embargo, se puede utilizar también desde cualquier computadora con linux mockeando la cámara con una carpeta del FileSystem. Para instalar todas las dependencias necesarias en Ubuntu/Debian, correr el siguiente comando:

```
./install.sh
```
# Configuración

Antes de correr la cámara es recomendable configurar los parámetros en el archivo config.json. Allí se puede especificar:
* Network
  * cmb_host: la ip donde se encuentra el broker que comunica con el CMB
  * topic: el tópico que utiliza para distinguir entre distintas zonas barriales
* Logger
  * level: el nivel de loggeo (10 -> debug, 20 -> info, 30 -> warning, 40 -> error)
* Camera
  * FPS:  cantidad de fotos por segundo que va a tomar la cámara
  * location: latitud y longitud global donde está ubicada la cámara
  * type: tipo de cámara ("mock" es para usar una carpeta como cámara y "pi" es para usar la RaspCam) 

# Run 

Para lanzar una cámara, correr el siguiente comando. 

```
./main.py
```

# Overview

El sistema de cámara de vigilancia utiliza rabbitMQ con MQTT como protocolo para enviar mensajes a su respectivo CMB. La manera de diferenciar entre distintos CMB es tanto a través de la IP del broker como del tópico. Las imagenes las consigue utilizando la RaspCam, las convierte a base64 y las adjunta en un mensaje json con el timestamp y la ubicación. Los mensajes que se envian siguen con el siguiente formato:

```javascript
{ "timestamp": "17-07-2017||01:09:07.434053", "location": [-34.5884843, -58.3962122], "frame": "base64_image"}
```
