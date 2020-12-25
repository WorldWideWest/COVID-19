#!/bin/bash

mkdir dataSet scripts notebooks && touch README.md

cd dataSet && mkdir rawData cleanData
cd ..
ls -la

echo "Folder and Files are created!"

git init
git remote add origin git@github.com:WorldWideWest/COVID-19.git

