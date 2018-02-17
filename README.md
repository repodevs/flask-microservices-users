# FLASK MICROSERVICES

[![Build Status](https://travis-ci.org/repodevs/flask-microservices-users.svg?branch=master)](https://travis-ci.org/repodevs/flask-microservices-users)

This project is based on [testdriven.io](http://testdriven.io/) Microservices with Docker, Flask and React

### Structure
1. _[flask-microservices-main](https://github.com/repodevs/flask-microservices-main)_ Docker Compose files, Nginx, admin scripts
2. _[flask-microservices-users](https://github.com/repodevs/flask-microservices-users)_ Flask App
3. _[flask-microservices-client](https://github.com/repodevs/flask-microservices-client)_ client-side based on ReactJS
---

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
Init flask migration folder:
```bash
$ docker-compose run users-services python manage.py db init
Migrate database:
```bash
$ docker-compose run users-services python manage.py db migrate
Apply migration to database:
```bash
$ docker-compose run users-services python manage.py db upgrade
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
---
Create virtual environment
```bash
$ python3.6 -m venv env
```
Activate virtual environment
```bash
$ source env/bin/activate
```
Export local environment
```bash
(env)$ export APP_SETTINGS=project.config.DevelopmentConfig
(env)$ export DATABASE_URL=postgres://postgres:postgres@localhost:5432/flask_users_dev
(env)$ export DATABASE_TEST_URL=postgres://postgres:postgres@localhost:5432/flask_users_test
(env)$ export SECRET_KEY="S3Cr3Tk3Y"
```
