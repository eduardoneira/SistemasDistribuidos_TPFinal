# Centro de Monitoreo Ciudad

# Install

Él sistema esta pensando para correr dentro de una distribución de Linux.
Para instalar todas las dependencias necesarias en Debian/Ubuntu, correr el siguiente comando:

```
./install.sh
./Database/create_database.sh
```

Estos comandos se encargan de instalar todas las dependecias necesarias para correr el CMC y a su vez crean una base de datos limpia para almacenar los datos.

# Configuration

Antes de levantar al CMC, es necesario configurar los distintos parámetros de cada módulo. Estos se encuentran en ImageListener/config.json y HTTPListener/config.json. Para más información de los parámetros, leer el README que se encuentra en dichos módulos.

# Run

Para correr al CMC es necesario levantar workers, al menos uno para el ImageListener y otro para el HTTPListener. Para levantar el ImageListener, utilizar los siguientes comandos:

```
cd ImageListener/
./worker.py
```
En cuanto al HTTPListener, utilizar los siguientes comandos:

```
cd HTTPListener/
./worker.py
```

# Overview

El CMC se compone de tres módulos principales: el ImageListener, que se encarga de escuchar mensajes de todas los CMB, el HTTPListener, que se encarga de escuchar requests que le lleguen desde el cliente web, y el FaceRecognizer, que es un wrapper de opencv con algoritmos útiles para reconocimiento facial.
Utiliza una base de datos relacional (Postgresql) para guardar toda la metadata de las imágenes con resultados positivos y las imágenes se almacenan en el disco duro.

La base de datos se compone de 4 tablas:
* Person: Datos de todas las personas a buscar
* BigPicture: Datos de las fotos que tienen resultados positivos
* PersonImage: Tabla de relación entre personas y fotos en donde se las vió
* Face: Datos sobre las caras dentro de las fotos que se encontro

En cuanto a la organización del disco duro para almacenar las imágenes, la jerarquía de carpetas es la siguiente:

```
image_database
|--- bigpics
|--- keypoints
|--- found
      |-- id1
      |-- id2
      |-- ...  
|--- people
      |-- id1
      |-- id2
      |-- ...    
```

Dentro de people/id1/ se encuentran las imagenes que se cargan al momento de querer buscar a una persona. Cuando se sube una imagen a la base de datos de busqueda, se almacena en keypoints una serialización de los datos principales de cada una de las imagenes enviadas. Una vez que se encuentra un match, en found/id1/ se va a guardar la cara recortada de la imagen original y el bigpics se va a guardar la imagen original.

Los módulos ImageListener y HTTPListener están diseñados de manera de que interactuan con ambas bases de datos. Utilizan un esquema de workers, los cuales son completamente paralelizables. Esto nos permite levantar la cantidad de workers que creamos convenientes según el uso del sistema. 