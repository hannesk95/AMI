import pandas as pd
import numpy as np
import matplotlib.pyplot as plt


pathApple = 'Apple/'
pathGoogle = 'Google/'
pathBAST = 'BAST/'
pathTomTom = 'TomTom/'



def GetDayOf2020ByDate(date): #date musst have form JJJJ-MM-DD!

    #array with days of each month -> 2020 is a leap year!
    MonthArr = [31, 29, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]
    
    #get year, month and day
    year = int(date[0:4])
    month = int(date[5:7])
    day = int(date[8:10])

    #caculate which day of the year this date corresponds
    days = 0
    for i in range(0, month - 1):
        days = days + MonthArr[i]
    days = days + day

    return days


#some specifications        
monthColor1 = 'cyan'
monthColor2 = 'lightcyan'

#Covid19Restrictions, dates from TomTom Munich side: https://www.tomtom.com/en_gb/traffic-index/munich-traffic 
startRestrictions = GetDayOf2020ByDate('2020-03-09')
endRestrictions = GetDayOf2020ByDate('2020-05-24')

startSeverveRestrictions = GetDayOf2020ByDate('2020-03-16')
endSeverveRestrictions = GetDayOf2020ByDate('2020-04-26')


def GetMonthlyValues(days, arr):
    #remove nans
    ind = np.where(np.isnan(arr))
    arr = np.delete(arr, ind)
    days = np.delete(days,ind)

    months = [1,2,3,4,5,6,7,8,9,10,11,12]
    MonthBins = [[1, 31], 
                    [32,60], 
                    [61,91], 
                    [92,121], 
                    [122,152], 
                    [153,182], 
                    [183,213],
                    [214,244], 
                    [245,274], 
                    [275,305], 
                    [306,335], 
                    [336,366]]

    month_sum = np.zeros(12,)
    month_count = np.zeros(12,)
    for day,val in zip(days,arr):
        k = 0
        for b in MonthBins:
            if day >= b[0] and day <= b[1]:
                break
            else:
                k = k + 1
        month_sum[k] = month_sum[k] + val
        month_count[k] = month_count[k] + 1

    month_sum[np.where(month_count == 0)] = np.nan
    month_mean = month_sum/month_count

    return months, month_mean

def UpdateTomTomData():
    ################################################
    #TomTom
    #this data is taken by hand from the TomTom Munich traffic index page: https://www.tomtom.com/en_gb/traffic-index/munich-traffic, accessed 10.06.2020
    #following code can be uncommented and updated to store new data -> maybe a webcrawler could be useful for this
    print('You need to change the values given by the newest TomTom traffic index website by hand!')

    #KW array
    KW_TomTom = np.empty([24,], dtype='S10')
    for i in range(1,25):
        KW_TomTom[i-1] = 'KW' + str(i)

    #assigned correlated day of KW in 2020
    day_TomTomMunich = np.empty([24,], dtype='int16')
    day_TomTomMunich[0] = 1
    for i in range(2,25):
        day_TomTomMunich[i-1] = day_TomTomMunich[i-2] + 7

    #values from website
    val_TomTomMunich = np.array((-0.64, -0.39, -0.15, -0.12, -0.06, 0.03, 0, 0, -0.21, -0.06, -0.15, -0.48, -0.64, -0.61, -0.61, -0.61, -0.52, -0.45, -0.39, -0.3, -0.33, -0.24, -0.33, 0))

    #build pandas dataframe and save it as csv
    data = {'KW_2020': np.arange(1,25), 'AssignedCorrDayOf2020': day_TomTomMunich, 'CongestionMunich': val_TomTomMunich}
    df = pd.DataFrame(data)
    df.to_csv('TomTomMunichMobilityReport_weekly.csv', index=False)

    month, month_val = GetMonthlyValues(day_TomTomMunich, val_TomTomMunich)
    year = np.zeros(12,)
    year[:] = 2020
    data = {'year': year, 'month': month, 'CongestionMunich': month_val}
    df = pd.DataFrame(data)
    df.to_csv('TomTomMunichMobilityReport_monthly.csv', index=False)


    
def UpdateBASTData():
    #Values from downloaded pdf taken by hand. Uncommenting and changig this code makes it able to update the data
    #18.03.-24.03. 25.03.-31.03. 01.04.-07.04. 08.04.-14.04. 15.04.-21.04. 22.04.-28.04. 29.04.-05.05. 06.05.-12.05. 13.05.-19.05.20.05.-26.05.
    #entspricht eigentlich nicht ganz der KW, da Datum immer von Mittwoch bis Dienstag
    print('You need to change the values given by the newest BAST mobility report by hand!')
    KW_BAST = np.array(('KW12', 'KW13', 'KW14', 'KW15', 'KW16', 'KW17', 'KW18', 'KW19', 'KW20'))
    day_BAST = np.array((78, 85, 92, 99, 106, 113, 120, 127, 134))
    #KFZ
    val_BAST = np.array((-40, -47, -45, -54, -40, -35, -36, -28, -15))
    data = {'KW_2020': np.arange(12,21), 'CorrDayOf2020': day_BAST, 'ValMobilityReport':val_BAST}
    df = pd.DataFrame(data)
    df.to_csv('BASTMobilityReport_weekly.csv', index=False)

    month, month_val = GetMonthlyValues(day_BAST, val_BAST)
    year = np.zeros(12,)
    year[:] = 2020
    data = {'year': year, 'month': month, 'ValMobilityReport': month_val}
    df = pd.DataFrame(data)
    df.to_csv('BASTMobilityReport_monthly.csv', index=False)




def Visualize_Comparison_MobilityReports():
    

    ################################################
    #TomTom Munich
    #read TomTom Munich data
    df = pd.read_csv(pathTomTom + 'TomTomMunichData.csv')

    #plot TomTom Munich data
    plt.plot(df.AssignedCorrDayOf2020, df.CongestionMunich.values * 100, label='TomTomMunich, weekly, base: corr. week in 2019', color='red')

    ################################################
    #BAST
    #read BAST data
    df = pd.read_csv(pathBAST + 'BASTData.csv')

    #plot BAST data
    plt.plot(df.CorrDayOf2020, df.ValMobilityReport, label='BAST, weekly, base: 02.02. - 07.03.2020', color='blue')

    ################################################
    #Apple
    #read Apple data and reduce it to Germany and driving
    df = pd.read_csv(pathApple + 'applemobilitytrends-2020-06-08.csv', encoding='latin-1', delimiter=',')
    df = df[df['region'] == 'Germany']
    df = df[df['transportation_type'] == 'driving'] 

    #drop some unused columns
    df = df.drop('geo_type', axis=1)
    df = df.drop('region', axis=1)
    df = df.drop('transportation_type', axis=1)
    df = df.drop('alternative_name', axis=1)
    df = df.drop('sub-region', axis=1)
    df = df.drop('country', axis=1)

    #shape of dataframe
    row, col = df.shape

    #array specifications
    val_Apple = np.empty([col,], dtype='float32')
    date_Apple = np.empty([col,], dtype='S10')

    #in this data the column names are dates -> store these dates in an array
    day_Apple = np.zeros((col,), 'float32')
    i = 0
    for column in df:
        val_Apple[i] = df[column]
        date_Apple[i] = column
        i = i + 1  

    #process the dates from above to the correlated days of the year to be able to plot and compare them
    ind = 0
    for date in date_Apple:
        day_Apple[ind] = GetDayOf2020ByDate(date)
        ind = ind + 1

    #reference baseline is in Apple data 100% but we are comparing at a reference line of 0%
    val_Apple = val_Apple - 100

    #plot Apple data
    plt.plot(day_Apple, val_Apple, label='Apple, daily, base: 13.01.2020', color='black')

    #update Apple monthly data
    month, month_val = GetMonthlyValues(day_Apple, val_Apple)
    year = np.zeros(12,)
    year[:] = 2020
    data = {'year': year, 'month': month, 'ValMobilityReport': month_val}
    df = pd.DataFrame(data)
    df.to_csv('AppleMobilityReport_monthly.csv', index=False)

    ################################################
    #Plot specifications for Mobility Reports from Apple, BAST, and TomTom Munich
    plt.fill_betweenx((125,-100), startRestrictions, endRestrictions, color='lightgray', label='Covid19 restrictions')
    plt.fill_betweenx((125,-100), startSeverveRestrictions, endSeverveRestrictions, color='darkgray', label = 'Covid19 severve restrictions')

    plt.fill_betweenx((-100,-115), 0, 31, color=monthColor1)
    plt.text(14, -110, 'J', color='black')
    plt.fill_betweenx((-100,-115), 31, 60, color=monthColor2)
    plt.text(45, -110, 'F', color='black')
    plt.fill_betweenx((-100,-115), 60, 91, color=monthColor1)
    plt.text(74, -110, 'M', color='black')
    plt.fill_betweenx((-100,-115), 91, 121, color=monthColor2)
    plt.text(105, -110, 'A', color='black')
    plt.fill_betweenx((-100,-115), 121, 152, color=monthColor1)
    plt.text(136, -110, 'M', color='black')
    plt.fill_betweenx((-100,-115), 152, 182, color=monthColor2)
    plt.text(166, -110, 'J', color='black')
    plt.ylim([-115,125])

    plt.grid()
    plt.legend()
    plt.ylabel('Deviation from base value in %')
    plt.xlabel('Day of the year 2020')
    plt.xlim([0,170])
    plt.show()

def VisualizeGoogleMR():
    ################################################
    #Google
    df = pd.read_csv(pathGoogle + '200610/Global_Mobility_Report.csv', encoding='latin-1', delimiter=',')
    df = df[df['country_region_code'] == 'DE'] #reduce to Germany
    df = df[df['sub_region_1'].isnull()] #reduce to only Germany and not Bundesländer

    #drop some unused columns
    df = df.drop('sub_region_1', axis = 1)
    df = df.drop('sub_region_2', axis = 1)
    df = df.drop('country_region_code', axis = 1)
    df = df.drop('country_region', axis = 1)

    #shape of df
    row, col = df.shape

    #assign day of 2020 from dates
    day_Google = np.zeros((row,), 'float32')
    ind = 0
    for date in df.date:
        day_Google[ind] = GetDayOf2020ByDate(date) 
        ind = ind + 1

    #new column in df named day and drop date
    df['day'] = day_Google
    df = df.drop('date', axis=1)


    #####
    #Plots
    
    #plot columns
    for column in df:
        if column != 'day':
            plt.plot(df.day.values, df[column].values, label=column)

    #plot specifications
    plt.fill_betweenx((280,-100), startRestrictions, endRestrictions, color='lightgray', label='Covid19 restrictions')
    plt.fill_betweenx((280,-100), startSeverveRestrictions, endSeverveRestrictions, color='darkgray', label = 'Covid19 severve restrictions')

    plt.fill_betweenx((-100,-115), 0, 31, color=monthColor1)
    plt.text(14, -110, 'J', color='black')
    plt.fill_betweenx((-100,-115), 31, 60, color=monthColor2)
    plt.text(45, -110, 'F', color='black')
    plt.fill_betweenx((-100,-115), 60, 91, color=monthColor1)
    plt.text(74, -110, 'M', color='black')
    plt.fill_betweenx((-100,-115), 91, 121, color=monthColor2)
    plt.text(105, -110, 'A', color='black')
    plt.fill_betweenx((-100,-115), 121, 152, color=monthColor1)
    plt.text(136, -110, 'M', color='black')
    plt.fill_betweenx((-100,-115), 152, 182, color=monthColor2)
    plt.text(166, -110, 'J', color='black')
    plt.ylim([-115,280])

    plt.title('daily, base: median of 03.01. - 06.02.2020')
    plt.grid()
    plt.legend()
    plt.xlim([0,170])
    plt.ylabel('Deviation from base value in %')
    plt.xlabel('Day of the year 2020')
    plt.show()


    #Plot with one week rolling mean
    for column in df:
        if column != 'day':
            df[column] = df[column].rolling(7).mean()
            plt.plot(df.day.values, df[column].values, label=column)

    df_month = pd.DataFrame()
    year = np.zeros(12,)
    year[:] = 2020
    df_month['year'] = year
    for column in df:
        if column != 'day':
            df_month['month'], df_month[column] = GetMonthlyValues(np.array(df.day.values), np.array(df[column].values))

    df_month.to_csv('GoogleMobilityReport_monthly.csv', index=False)

    plt.fill_betweenx((125,-100), startRestrictions, endRestrictions, color='lightgray', label='Covid19 restrictions')
    plt.fill_betweenx((125,-100), startSeverveRestrictions, endSeverveRestrictions, color='darkgray', label = 'Covid19 severve restrictions')

    plt.fill_betweenx((-100,-115), 0, 31, color=monthColor1)
    plt.text(14, -110, 'J', color='black')
    plt.fill_betweenx((-100,-115), 31, 60, color=monthColor2)
    plt.text(45, -110, 'F', color='black')
    plt.fill_betweenx((-100,-115), 60, 91, color=monthColor1)
    plt.text(74, -110, 'M', color='black')
    plt.fill_betweenx((-100,-115), 91, 121, color=monthColor2)
    plt.text(105, -110, 'A', color='black')
    plt.fill_betweenx((-100,-115), 121, 152, color=monthColor1)
    plt.text(136, -110, 'M', color='black')
    plt.fill_betweenx((-100,-115), 152, 182, color=monthColor2)
    plt.text(166, -110, 'J', color='black')
    plt.ylim([-115,125])

    plt.title('One week rolling mean, daily values, base: median of 03.01. - 06.02.2020')
    plt.grid()
    plt.legend()
    plt.xlim([0,170])
    plt.ylabel('Deviation from base value in %')
    plt.xlabel('Day of the year 2020')
    plt.show()

VisualizeGoogleMR()