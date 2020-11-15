#! /bin/bash

wget -O /home/hackohio2020/hackohio2020/raw/covid_confirmed_usafacts.csv https://static.usafacts.org/public/data/covid-19/covid_confirmed_usafacts.csv
wget -O /home/hackohio2020/hackohio2020/raw/covid_deaths_usafacts.csv https://static.usafacts.org/public/data/covid-19/covid_deaths_usafacts.csv
python3 daily_load.py
