# Centro de Monitoreo Barrial

# Install

Él sistema esta pensando para correr dentro de Fedora. Para instalar todas las herramientas necesarias, correr el siguiente comando:

```
sudo ./install.sh
```

# Run

En el archivo config.json se pueden modificar valores para cambiar el comportamiento del CMB. Para correr un CMB usar el siguiente comando :

```
python3 main.py
``` 

# Overview

El CMB recibe usando un cliente AMQP los mensajes de las camaras. Distingue de que camaras agarrar según routing key, que tiene que coincidir con el topico de los mensajes MQTT que envian las camaras. Luego utiliza el CascadeClassifier con haarcascade de OpenCV para encontrar rostros y cortarlos. Luego envia en un mensaje json :

```javascript
{ "timestamp": "17-07-2017||01:09:07.434053", "location": [-34.5884843, -58.3962122], "frame": "base64_image", "faces": [base64_face1, base64_face2, ...]}
```
Este mensaje solo se envia si se detecto alguna cara. Utiliza AMQP como protocolo ya que estamos asumiendo que los CMB van a ser computadoras con mas recursos que las camaras.