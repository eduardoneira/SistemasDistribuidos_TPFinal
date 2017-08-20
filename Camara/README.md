# Cámara de Vigilancia

# Install

Él sistema esta pensando para correr dentro de Fedora. Para instalar todas las herramientas necesarias, correr el siguiente comando:

```
sudo ./install.sh
```

# Run 

Configurar el archivo config.json en base a lo necesitado.

```
python3 main.py
```

# Tests

```
cd tests/
python3 camera_test.py
```

# Configuración

Para configurar la cámara se pueden modificar varios parámetros en el archivo config.json. Allí se puede especificar el host donde se encuentra el broker que comunica con el CMB, el tópico con el cual va a publicar, la cantidad de frames por segundo que va a enviar la cámara, las posiciones en latitud y longitud en las que se encuentra la cámara y el tipo de cámara que se quiere usar. En caso de querer usar un mock en el fs, usar como value de "camara": "mock". Si se quiere usar la cámara de las raspberrypi, usar "camara":"rasrpi"

# Overview

El sistema de cámara de vigilancia usa rabbitMQ usando MQTT como protocolo para enviar mensajes a su respectivo CMB. Los mensajes que se envian son json con el siguiente formato:

```javascript
{ "timestamp": "17-07-2017||01:09:07.434053", "location": [-34.5884843, -58.3962122], "frame": "base64_image"}
```
