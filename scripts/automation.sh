#!/bin/bash

python scrapping.py; python combining.py && python replacing.py; python entityParsing.py
