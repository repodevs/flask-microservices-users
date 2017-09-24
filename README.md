# FLASK MICROSERVICES

## How To Run
----
1. create docker-machine (with driver digitalocean based on ubuntu 14.04)   
```bash
$ docker-machine create --driver digitalocean --digitalocean-access-token=DO_TOKEN --digitalocean-image ubuntu-14-04-x64 devbox
```
2. activate docker-machone   
```bash
$ eval "$(docker-machine env devbox)"
```
3. build image   
```bash
$ docker-compose build
```
4. fire up the container   
```bash
$ docker-compose up
```
_bisa tambahkan `-d` jika ingin di jalankan pada daemon_   
5. copy local file ke host digitalocean   
```bash
$ docker-machine scp -r ./app devbox:/root
```
6. melihat logs   
```bash
$ docker-compose logs -f users-service
```
----

## Other Commands

Create the database:
```bash
$ docker-compose run users-services python manage.py recreate_db
```
Seed the database:
```bash
$ docker-compose run users-services python manage.py seed
```
Run the tests:
```bash
$ docker-compose run users-services python manage.py test
```
To stop Docker container:
```bash
$ docker-compose stop
```
To bring down the container:
```bash
$ docker-compose down
```
Force build:
```bash
$ docker-compose build --no-cache
```
Remove image:
```bash
$ docker rmi $(docker images -q)
```
---
Access database via psql:
```bash
$ docker exec -ti users-db psql -U postgres -W
```

