# Nascar / IndyCar Lap Times

## Installation

You must have Python 3 and Git installed.

- Clone this repository: `git clone https://github.com/JeMorriso/nascar.git`
- Download the dependencies: `pip install -r /path/to/cloned_directory/requirements.txt`

## Usage

First go to the cloned directory: `cd /path/to/cloned_directory`
To get Nascar lap times while a race is on, run `python src/nascar/nascar.py`

This will get lap data from Nascar every 5 seconds, outputting any new laps to a .xlsx file. The .xlsx is located in `./data/nascar` directory. Its name will be the current date. Use this .xlsx file as an [external data connection](https://support.microsoft.com/en-us/office/refresh-an-external-data-connection-in-excel-1524175f-777a-48fc-8fc7-c8514b984440) in Excel and you should see the Excel sheet updating in real time.

The program will continue running until you manually stop it (Ctrl-C).

Similarly for IndyCar:
run: `python src/indycar/indycar.py`
data directory: `/path/to/cloned_directory/data/indycar`

## Nascar Configuration

The Nascar data URL changes for each race, so you need to update `config.json` with the new URL before each race.

### Finding the URL

1. Go to Nascar Race Center using Google Chrome
2. Right-click and click on 'Inspect'
3. Click on the 'Network' tab in the 'Inspect' menu
4. Click on the 'XHR' tab inside the 'Network' page
5. Look for a file titled `lap-times.json`
6. Right-click on it, and then select 'Copy link address'
7. Paste the link address into `config.json`

## Output Data

Output data is stored in a .xslx file with 2 sheets, 1 for Lap Time, and the other for Running Position.
