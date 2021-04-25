# Nascar / IndyCar Lap Times

## Installation

You must have Python 3 and Git installed.

- Clone this repository: `git clone https://github.com/JeMorriso/nascar.git`
- Download the dependencies: `pip install -r /path/to/cloned_directory/requirements.txt`

## Usage

First go to the cloned directory: `cd /path/to/cloned_directory`
To get Nascar lap times while a race is on, run `python src/nascar/nascar.py`

This will get lap data from Nascar every 5 seconds, outputting any new laps to a .csv file. The .csv is located in `./data/nascar` directory. Its name will be the current date. Use this .csv file as an [external data connection](https://support.microsoft.com/en-us/office/refresh-an-external-data-connection-in-excel-1524175f-777a-48fc-8fc7-c8514b984440) in Excel and you should see the Excel sheet updating in real time.

The program will continue running until you manually stop it (Ctrl-C).

Similarly for IndyCar:
run: `python src/indycar/indycar.py`
data directory: `/path/to/cloned_directory/data/indycar`

## Output Data

Output data is in table form with Name, Lap Number, Running Position, and Lap Time as the columns.

E.G:

```
Name,Lap Number,Running Position,Lap Time
BJ McLeod(i),111,29,50.555
Cody Ware(i),110,34,50.346
Corey LaJoie,111,26,50.146
Erik Jones,111,28,50.255
JJ Yeley(i),111,27,50.314
Joey Gase(i),108,36,49.973
Josh Bilicki,101,38,50.221
Justin Haley(i),110,35,50.21
Kevin Harvick,111,22,48.36
Kurt Busch,104,37,853.161
Ross Chastain,111,24,49.838
Ryan Newman,111,25,49.845
```
