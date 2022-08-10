# Proyecto Clima - Tecnologias emergentes

Puede descargar docker desde el siguiente link: [docker-desktop](https://www.docker.com/products/docker-desktop/)

## Comandos para la ejecucion

Para correr el proyecto ejecute el comando

```shell
 docker-compose -f clima-composer.yml up -d 
```

## Accesos

- <http://127.0.0.1> = Main aplication.
- <http://127.0.0.1/docs> = Swagger interfaz
- <http://localhost:8080> = Adminer de la base de datos

## Sobre los directorios

En el proyecto se encuentran los siguientes directorios

- app: Incluye todos los archivos para el funcionamiento de la api rest 
- arduino: Aca se encuentran los archivos c y las librerias necesarias para el funcionamiento del Arduino.
- data: Directorio de persistencia de datos de la base. `Preferiblemente no modificar`
- datos_mosquitto: Directorios de persistencia MQTT Mosquitto, con esto vamos a configurar nuestro docker.

## Sobre el desarrollo

## Comandos utiles Docker

```shell
docker build -t api_image .
docker run -d --name api_docker -p 80:80 api_image
```

### Base de datos

```shell
docker run --name some-mysql -e MYSQL_ROOT_PASSWORD=password -d mysql:latest --character-set-server=utf8mb4 --collation-server=utf8mb4_unicode_ci
```

Acceder por consola

```shell
docker ps
docker exec -i -t d83c525a65b3  /bin/bash
```

## Uso de Mosquito MQTT

en la consola del contenedor para suscribirse al topic:

```shell
mosquitto_sub -h localhost -t clima
```

para publicar los datos:

```shell
 mosquitto_pub -h localhost -t clima -m '{"ano": "2022","mes": "08","dia": "09","hora": "13","temp": "12", "humidity": "85", "location_id": "1"}'
```

### Consideraciones a tener en cuenta

En el codigo del arduino hay definidas un conjuntos de variables que hay que definir para asegurarse que funcione todo.

Nombre de la red a la que se conectara:

```shell
const char* ssid = "xxxxxxxx";
```

Contraseña de la red:

```shell
const char* password = "xxxxxxxxxxx";
```

Servidor MQTT:

```shell
const char* mqtt_server = "XXXXXXXXXXXX";
```
