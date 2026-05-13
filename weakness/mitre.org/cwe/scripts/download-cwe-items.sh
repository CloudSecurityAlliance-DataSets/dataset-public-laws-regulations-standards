#!/bin/bash

wget https://cwe.mitre.org/data/csv/699.csv.zip
wget https://cwe.mitre.org/data/csv/1194.csv.zip
wget https://cwe.mitre.org/data/csv/1000.csv.zip

unzip 699.csv.zip
unzip 1194.csv.zip
unzip 1000.csv.zip

mv 1000.csv CWE-Research-Concepts-1000.csv
mv 699.csv CWE-Software-Development-699.csv
mv 1194.csv CWE-Hardware-Design-1194.csv


wget https://cwe.mitre.org/data/xml/views/699.xml.zip
wget https://cwe.mitre.org/data/xml/views/1194.xml.zip
wget https://cwe.mitre.org/data/xml/views/1000.xml.zip


unzip 699.xml.zip
unzip 1194.xml.zip
unzip 1000.xml.zip

yq -p xml -o json 699.xml > CWE-Software-Development-699.json
yq -p xml -o json 1194.xml > CWE-Hardware-Design-1194.json
yq -p xml -o json 1000.xml > CWE-Research-Concepts-1000.json

rm -f 1000.csv.zip	1000.xml.zip	1194.csv.zip	1194.xml.zip	699.csv.zip	699.xml.zip
rm -f 1000.xml	1194.xml	699.xml

