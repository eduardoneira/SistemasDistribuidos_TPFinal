# Sistemas Distribuidos 1: TP Final

Repositorio para el TP final de Sistemas Distribuidos 1

# Autores
  - Luis Ali
  - Eduardo Neira

# Arquitectura

Este trabajo práctico consta de varios componentes que pueden trabajar de manera distribuida.
Estos componentes son:  
- Cámaras
- Centro de Monitoreo Barrial(CMB)
- Centro de Monitoreo Ciudad(CMC)
- Web Server  


Para la comunicación entro los distintos sistemas se utilizó como broker RabbitMQ, usando clientes con distintos protocolos según las limitaciones de cada sistema. Para el preprocesamiento de imagenes y el reconocimiento facial se utilizó OpenCV. 

# Overview

Las cámaras se encargan de capturar fotos a través de una cámara real y envía un mensaje con la posición, el tiempo y la imagén a un CMB. La "cámara" utiliza MQTT como protocolo y está pensado para ser utilizado dentro de una Raspberry Pi.

Desde los centro de monitoreo barrial, se reciben fotos de las distintas cámaras según tópico y se las procesa una por una, buscando caras. El reconocmiento de caras utiliza un clasificador en cascada de haar, priorizando caras de frente. Luego, publica un mensaje con un tópico para el CMC.  

En el CMC se encuentran 2 procesos corriendo al mismo tiempo. Uno es el Image Listener que escucha mensajes de los CMB. Todas las caras que llegan en el mensaje se comparan contra la base de datos de imagenes. Las que son suficientemente parecidas se almacenan mientras que las otras se descartan. El otro proceso es el Web Listener, que maneja las request del servidor web. Ambos procesos utilizan el FaceRecognizer, un wrapper de OpenCV con los principales algortimos para reconocimiento facial. Las fotos son persistidas en el file system en caso de estar relacionadas y también se tiene un schema de base de datos para guardar toda la data relacionada.  

Finalmente el web server es el q recibe los requets de las páginas web y se las envía al HTTP Listener para que las interprete. Se encarga de resolver todos los pedidos de las páginas web utiliza RPC a través de colas de RabbitMQ para recibir la respuesta.   