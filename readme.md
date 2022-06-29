## Comandos para la ejecucion

```
docker build -t api_image .
docker run -d --name api_docker -p 80:80 api_image
```

### Base de datos
```
docker run --name some-mysql -e MYSQL_ROOT_PASSWORD=password -d mysql:latest --character-set-server=utf8mb4 --collation-server=utf8mb4_unicode_ci
```

Acceder por consola
```
docker ps
docker exec -i -t d83c525a65b3  /bin/bash
```


 docker-compose -f mysql-composer.yml up -d