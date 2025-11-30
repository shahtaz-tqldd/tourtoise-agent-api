#!/bin/sh

# clean docker
docker system prune --force

# create docker network (ignore error if exists)
echo "Creating Docker network"
docker network create tourtoise-network || true

echo "closing dev docker"
docker compose -f docker-compose.yml down || true

echo "running docker compose for webserver"
docker compose -f docker-compose.yml up --build --remove-orphans