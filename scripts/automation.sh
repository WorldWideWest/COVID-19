#!/bin/bash

echo "Starting scrapping.py to get the data from the MCA website"

python3 scrapping.py

echo "Finished scrapping continuing on the next script parser.py"

python3 parser.py

echo "Combining all files gathered from the previous scripts"

python3 combining.py

echo "Filling missing Data"

python3 replacing.py

echo "All procesess are completed successfuly" 

