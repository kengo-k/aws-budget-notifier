#!/bin/bash

stage=$1

if [ -d ".build" ]; then
  rm -rf .build
fi

mkdir .build
mkdir .build/lib

cp package.json package-lock.json .build
cp -r src .build
cp .env.${stage} .build/.env
cp requirements.txt .build/lib

if [ "$stage" = "local" ]; then
  cp deploy/serverless.local.yml .build/serverless.yml
else
  cp deploy/serverless.yml .build
fi

cd .build/lib
npm ci
pip install -r requirements.txt -t .
cd ..

set -a
source .env
set +a

npx serverless deploy --stage $stage --force