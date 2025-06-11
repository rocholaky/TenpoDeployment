#!/bin/bash
export COMPOSE_BAKE=true
docker compose build

docker compose up --build --remove-orphans -d double-model-api