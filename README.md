# Sistemas Distribuidos 1: TP Final

Repositorio para el TP final de Sistemas Distribuidos 1


# Arquitectura

Este trabajo práctico consta de varios componentes que pueden trabajar de manera distribuida.
Estos componentes son:  
- Camaras
- Centro de Monitoreo Barrial
- Centro de Monitoreo Ciudad
- Web Server  


Para la conexión de los distintos sistemas se utilizó como broker RabbitMQ, usando clientes con distintos protocolos según las limitaciones de cada sistema. Para el reconocimiento facial, se utilizó OpenCV. En cuanto a encontrar las fotos más parecidas, se utilizó un método de reconocimiento más de moda que es Local binary patterns histograms.  


Las "cámaras" se encargan de recibir fotos de a través de una cámara real y las publica en un tópico para el CMB. La "cámara" utiliza MQTT como protocolo ya que se trataba de un componente con pocos recursos y MQTT es un protocolo con una gran variedad de clientes implementados. De esta manera, si se quiere migrar el componente a un arduino o una raspberry pi 0, es posible.   

Desde los centro de monitoreo barrial, se reciben fotos de las distintas cámaras según tópico y se las procesa una por una, buscando caras. El reconocmiento de caras utiliza un clasificador en cascada de haar, priorizando caras de frente. Luego, publica en un tópico que va a agarrar el CMC.  

En el CMC tenemos tres procesos funcionando. Uno es el Image Listener que escucha mensajes de los CMB. Estos mensajes se los envía al face recognizer que predice si esa cara pertenece a alguien o no. Si la cara es suficientemente parecida, se la agrega al entrenamiento del clasificador de caras. También se encuentra un proceso HTTP Query handler, que recibe las request del server y contesta según el estado actual del face recognizer. La comunicación entre los tres procesos es a través de colas de RabbitMQ. Las fotos son persistidas en el file system en caso de estar relacionadas y también se tiene un schema de base de datos para guardar toda la data relacionada.  

Finalmente el web server es el q recibe los requets de las páginas web y se las envía al HTTP query handler para que las interprete. Se encarga de resolver todos los pedidos de las páginas web utiliza RPC a través de colas de RabbitMQ para recibir la respuesta.   