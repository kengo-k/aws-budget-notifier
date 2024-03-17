#!/bin/bash

if [ -d ".build" ]; then
	rm -rf .build
fi

mkdir .build
cp package.json package-lock.json .build
cp *.py .build
cp config.*.yml .build
cp .env.prd .build
cp requirements.txt .build

cd .build
npm ci
pip install -r requirements.txt -t .

npx serverless deploy --stage prd