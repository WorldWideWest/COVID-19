#!/bin/bash

python3 scrapping.py; python3 combining.py && python3 replacing.py; python3 entityParsing.py
