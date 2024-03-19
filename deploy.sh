#!/bin/bash

stage=$1

if [ -d ".build" ]; then
  rm -rf .build
fi

mkdir .build
mkdir .build/lib

cp package.json package-lock.json .build
cp -r src .build

if [ "$stage" = "local" ]; then
  cp .env .build/.env
else
  cp .env.${stage} .build/.env
fi

cp requirements.txt .build/lib
cp deploy/serverless.${stage}.yml .build/serverless.yml

cd .build/lib
npm ci
pip install -r requirements.txt -t .
cd ..

set -a
source .env
set +a

npx serverless deploy --stage $stage --force