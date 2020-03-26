# bisbo
Bisbo is a news media organisation that converts current news into animation in several Indian languages.

Install docker:
https://www.digitalocean.com/community/tutorials/how-to-install-and-use-docker-on-ubuntu-18-04

Install docker compose:
https://docs.docker.com/compose/install/


Server Start:
docker-compose build
docker-compose down && docker-compose up -d

############# Run Migrations
docker exec -it bisbo_web_1 /bin/bash
./manage.py migrate

############# Run Server
docker exec -it bisbo_web_1 /bin/bash
./manage.py runserver 0.0.0.0:8080
