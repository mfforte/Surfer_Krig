Forte - July 2021
refactor old perl script to python for gridding FRF survey data


This script assumes that you have the program surfer installed and licensed on computer
also needs the "scripter.exe" comes with surfer installed in "C:/Temp/Scripter/Scripter.exe"

The python allows user to select the .csv file
then checks data for gridding ensuring enough lines are surveyed
setups grid parameters for surfer then calls ContourGrid_ascii.BAS (subprocess)
creates FRF coords and geographic 
writes file