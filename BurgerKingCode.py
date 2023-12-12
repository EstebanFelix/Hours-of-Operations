# CLEANING ALL FILES FROM A FOLDER
import os
import glob
import pandas as pd 
import numpy as np
import datetime

def clean_all_hourly_sales_data(masterlist_filepath, input_folder, output_folder):
    # Read in the master list file
    burger_king = pd.read_csv(masterlist_filepath)

    # Get a list of all .csv files in the input folder
    input_files = glob.glob(os.path.join(input_folder, '*.csv'))

    # Clean each input file and save the output to a new file in the output folder
    for input_file in input_files:
        # Extract the filename without the extension
        filename = os.path.splitext(os.path.basename(input_file))[0]

        # Construct the output filepath
        output_filepath = os.path.join(output_folder, filename + '_CLEAN.csv')

        # Read in the hourly sales data
        hourly_sales_burger_king = pd.read_csv(input_file)

        # Merging the files to have CODE in the HourlySales file
        df = pd.merge(hourly_sales_burger_king, burger_king[['CODE', '#']], left_on='Store Number', right_on='#', how='left')
        df['CODE'] = df['CODE'].fillna('NNN' + df['Store Number'].astype(str))

        # Cleaning file hourly sales for Burger King
        df['QuarterHourBegin'] = df['QuarterHourBegin'].astype(str)
        df['hour_begin'] = df['QuarterHourBegin'].str.partition(':')[0]

        df['date_month'] = df['Business Date'].str.partition('/')[0]
        df['date_day'] = df['Business Date'].str.partition('/')[2]
        df['date_day'] = df['date_day'].str.partition('/')[0]
        df['date_year'] = df['Business Date'].str.rpartition('/')[2]

        df['business_date'] = df['date_year']+'-'+df['date_month']+'-'+df['date_day']

        # Drop unnecessary columns
        df = df.drop(columns=['date_day', 'date_month', 'date_year','Business Date', 
                              'QuarterHourEnd','Franchise ID Number','Franchise Site Number',
                              'Accounting Group Code','PointOfPurchaseID','QuarterHourID','#',
                              'CustomerCounts','QuarterHourBegin'])

        # Group by relevant columns and sum the 'Sales'
        df_groupby = df.groupby(['Store Number', 'business_date', 'Point Of PurchaseName', 'hour_begin',"CODE"])['Sales'].sum().reset_index()
        df_groupby["Store Number"] = df_groupby["Store Number"].astype(str)
        df_groupby["hour_begin"] = df_groupby["hour_begin"].astype(int)
        df_groupby = df_groupby.sort_values(["Store Number", "business_date", "Point Of PurchaseName", "hour_begin"])
        column_order = ['CODE', 'Store Number', 'business_date', 'Point Of PurchaseName', 'hour_begin', 'Sales']
        df_groupby = df_groupby.reindex(columns=column_order)
        df_groupby = df_groupby.rename(columns={'CODE': 'code'})

        # Save cleaned data to CSV
        df_groupby.to_csv(output_filepath, index=False)
        print(f'Cleaned {input_file} and saved output to {output_filepath}')

# Example usage
clean_all_hourly_sales_data(masterlist_filepath="Masterlists/BK_masterlist.csv", 
                            input_folder="RawData/Burger King/RawData", 
                            output_folder="RawData/Burger King/CleanData")