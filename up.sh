#!/bin/bash
docker compose build

docker compose up --build --remove-orphans -d double-model-api