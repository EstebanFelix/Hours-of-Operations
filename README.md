# Hours-of-Operations

## Overview
This Python script cleans hourly sales data for Burger King stores. It reads raw CSV files, merges them with a master list, and performs various cleaning operations. The cleaned data is then saved to new CSV files.

### Summary
The script:
- Reads a master list of store information.
- Processes raw hourly sales data for each store, merging it with the master list.
- Cleans and organizes the data, creating a summarized and structured output.
- Provides flexibility for customization based on data structure and requirements.

## Prerequisites
- Python 3.x


## Configuration
- Ensure the master list file (BK_masterlist.csv) is located in the "Masterlists" folder.
- Place raw hourly sales data files (in CSV format) in the "RawData/Burger King/RawData" folder.

## Notes
- This script assumes a specific structure for the raw data files and master list.
- The script performs a left join, keeping all rows from the raw data and filling in missing values from the master list.
- Adjust the script according to your data structure and requirements.
