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

