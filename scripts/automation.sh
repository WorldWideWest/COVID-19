#!/bin/bash

python scrapping.py; python combining.py && python replacing.py;

python imputer.py
