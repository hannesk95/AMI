


import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

from os import listdir
import os
from os.path import isfile, join

import requests
from zipfile import ZipFile



def download_url(url, save_path):
    #function from: https://stackoverflow.com/questions/9419162/download-returned-zip-file-from-url/14260592
    
    chunk_size=128
    r = requests.get(url, stream=True)
    with open(save_path, 'wb') as fd:
        for chunk in r.iter_content(chunk_size=chunk_size):
            fd.write(chunk)

def DownloadHourData_BAST(CounterNumber, year, FolderSave):

    BAST_Link = 'https://www.bast.de/videos/' + str(year) + '/zst' + str(CounterNumber) + '.zip'
    FileName = FolderSave + 'zst' + str(CounterNumber) + '_' + str(year) + '.zip'

    download_url(BAST_Link, FileName)

    try:
        #unzip file
        zf = ZipFile(FileName, 'r')
        zf.extractall(FolderSave)
        zf.close()
    except:
        print('File ' + FileName + ' does not work to unzip.')

    #remove zip file
    os.system('rm ' + FileName)



def ProcessDailyMonthlyValues(path):

    df = pd.read_csv(path, delimiter=';') 

    var = ['Datum', 'Stunde', 'KFZ_R1']
    for column in df:
        if column not in var:
            df = df.drop(column, axis=1)

    dates = df.Datum.drop_duplicates()

    DailyValues = np.zeros((365,), 'int32')

    i = 0
    for da in dates:
        if da != 160229 and da != 120229 and da != 80229 and da != 40229: #drop values of "Schaltjahr"
            val = np.sum(df[df.Datum == da].KFZ_R1.values)
            #print(val)
            DailyValues[i] = val
            i = i + 1

    months = np.array(['J', 'F', 'M', 'A', 'M', 'J', 'J', 'A', 'S', 'O', 'N', 'D'])
    MonthsStart = np.array([1, 31, 59, 90, 120, 151, 181, 212, 243, 273, 304, 334])
    MonthsEnde = np.array([32, 60, 91, 121, 152, 182, 213, 244, 274, 305, 335, 366])

    MonthlyValues = np.zeros((12,))

    for i in range(0,12):
        MonthlyValues[i] = np.sum(DailyValues[MonthsStart[i]:MonthsEnde[i]])

    return DailyValues, MonthlyValues


def Process(DZ_Nr_unique, years, path, keepOrigData):

    if not os.path.exists(path):
        os.system('mkdir ' + path)

    ####initialize arrays

    #initialization of Dataframes
    months = np.arange(1,13)
    days = np.arange(1,366)
    #years = np.arange(years[0], years[-1])

    #dataframe for monthly data
    months_arr = []
    years_arr = []
    for i in range(0,len(years)):
        months_arr = np.append(months_arr, months)
        year = years[i] + i
        for k in range(0,12):
            years_arr = np.append(years_arr, year)

    df_month = pd.DataFrame()
    df_month['year'] = years_arr
    df_month['month'] = months_arr

    #dataframe for daily data
    days_arr = []
    years_arr = []
    for i in range(0,len(years)):
        days_arr = np.append(days_arr, days)
        year = years[i] + i
        for k in range(0,365):
            years_arr = np.append(years_arr, year)

    df_day = pd.DataFrame()

    df_day['year'] = years_arr
    df_day['day'] = days_arr

    #DZ_Nr_unique = np.array([9140])

    total_count = len(DZ_Nr_unique)

    print('All counter stations: ', DZ_Nr_unique)
    print('In total # = ', total_count)
    count = 1
    #for nr in range(0,20):
    for nr in range(0,len(DZ_Nr_unique)):
    #for DZ_Nr in DZ_Nr_unique:
        DZ_Nr = DZ_Nr_unique[nr]
        print('Processing ' , count, ' of ', total_count)
        count = count + 1
        df_month.insert(2, str(DZ_Nr), np.nan)
        
        val_month = []
        val_day = []
        for year in years:
            try:
                DownloadHourData_BAST(DZ_Nr, year, path)

                files = [f for f in listdir(path) if f.endswith(".csv") and
                        isfile(join(path, f)) and not f.startswith('.')]
                files.sort()

                f = 'zst' + str(DZ_Nr) + '_' + str(year) + '.csv'

    
                DailyValues, MonthlyValues = ProcessDailyMonthlyValues(path + f)

                val_month = np.append(val_month, MonthlyValues)
                val_day = np.append(val_day, DailyValues)

                if not keepOrigData:
                    os.system('rm ' + path + f)
            except:

                MonthlyValues = np.zeros((12,))
                MonthlyValues[:] = np.nan
                val_month = np.append(val_month, MonthlyValues)

                DailyValues = np.zeros((365,))
                DailyValues[:] = np.nan
                val_day = np.append(val_day, DailyValues)

        df_month[str(DZ_Nr)] = val_month
        df_day[str(DZ_Nr)] = val_day


    df_month.to_csv('monthly_test.csv', index=False)
    df_day.to_csv('daily_test.csv', index=False)   


def DownloadAllData(keepOrigData):

    fileJahresdaten = 'Zeitreihe.csv'
    Zeitreihen_URL = 'https://www.bast.de/BASt_2017/DE/Verkehrstechnik/Fachthemen/v2-verkehrszaehlung/Daten/2018_1/Jawe2018.csv?view=renderTcDataExportCSVAlleJahre&cms_strTyp=A'

    path = './test/'
    if not os.path.exists(path):
        os.system('mkdir ' + path)

    download_url(Zeitreihen_URL, path + fileJahresdaten)
    df_Jahresdaten = pd.read_csv(path + fileJahresdaten, encoding='latin-1', delimiter=';') 

    #remove unused columns
    var = ['DZ_Nr', 'Jahr']
    for column in df_Jahresdaten:
        if column not in var:
            df_Jahresdaten = df_Jahresdaten.drop(column, axis=1)

    DZ_Nr_unique = np.array(df_Jahresdaten.DZ_Nr.drop_duplicates())
    years = np.array(df_Jahresdaten.Jahr.drop_duplicates(), 'int16')

    Process(DZ_Nr_unique, years, path, keepOrigData)

def DownloadPartOfData(DZ_Nr_arr, years, keepOrigData):
    path = 'test/'
    Process(DZ_Nr_arr, years, path, keepOrigData)


def PrintInfo():
    print('######## Info BAST download ########')
    print('This script atomatically downloads data from the BAST database for counting stations.')
    print('The script uses the hourly data and processes it to monthly and daily values')
    print('Data source: https://www.bast.de/BASt_2017/DE/Verkehrstechnik/Fachthemen/v2-verkehrszaehlung/zaehl_node.html')
    print('')
    print('Specifications:')
    print('     - the script creates a folder named temp/ in your current directory.')
    print('     - the processed data is stored in .csv files named monthly.csv and daily.csv')
    print('')
    print('Functions:')
    print('DownloadAllData(keepOrigData)')
    print('     keepOrigData: if True the hourly data is not deleted after processing')
    print('     This function downloads and processes all available data from the BAST database. That means all available counting stations and all years.')
    print('')
    print('DownloadPartOfData(DZ_Nr_arr, years, keepOrigData)')
    print('     DZ_Nr_arr: numpy array to specify the counting station numbers you are interested to download.')
    print('     years: numpy array to specify the years you are interested to download.')
    print('     keepOrigData: if True the hourly data is not deleted after processing')
    print('')
    print('All other functions in this script are not included in the API and only helpers for the mentioned API functions above.')
    

if __name__ == "__main__":
    DZ_Nr_arr = np.array([9140]) # counting station: AK-München West O
    years = np.array([2018]) # year we are interesed in
    keepOrigData = False # hourly data should be deleted
    DownloadPartOfData(DZ_Nr_arr, years, keepOrigData)