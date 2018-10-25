import pandas as pd
pd.options.display.max_columns = 20

import numpy as np

import seaborn as sns

from sklearn import preprocessing

# Read the data/flights.csv dataset into Python
data = pd.read_csv('/Users/akofenem/PycharmProjects/mip-python/data/flights.csv', sep=',' , encoding="ISO-8859-1")

# Create a "Route" column by merging departure airport and destination airport
data['ROUTE'] = data['ORIGIN_AIRPORT'].astype('str') + ' - ' + data['DESTINATION_AIRPORT'].astype('str')

# Write a function that, for all the quantitative cols, returns mean, quartiles, stdev, max, kurtosis
def quant(dataframe):
    return pd.concat([dataframe.describe(),dataframe.kurtosis().to_frame().transpose().rename(index={0:'kurt'})])

desc = quant(data)

# replace the NaN with mean values in the column 'AIR_SYSTEM_DELAY'
data['AIR_SYSTEM_DELAY'] = data['AIR_SYSTEM_DELAY'].fillna(data['AIR_SYSTEM_DELAY'].mean())

# Remove outliers for 'departure_delay' - remove rows in excess of 3 standard deviations from mean
data = data[(data['DEPARTURE_DELAY'] > data['DEPARTURE_DELAY'].describe()['mean'] - 3*data['DEPARTURE_DELAY'].describe()['std']) &
            (data['DEPARTURE_DELAY'] < data['DEPARTURE_DELAY'].describe()['mean'] + 3*data['DEPARTURE_DELAY'].describe()['std'])]

# Winsorise all quantitative columns to a 95% upper and lower bound


quant_col = desc.columns

def winsorise_data(data):
    temp = data.copy()
    quantiles = temp.quantile([0.05,0.95])
    del quantiles['YEAR'], quantiles['MONTH'], quantiles['DAY'], quantiles['DAY_OF_WEEK'], quantiles['FLIGHT_NUMBER'], quantiles['SCHEDULED_DEPARTURE'],\
        quantiles['DEPARTURE_TIME'], quantiles['SCHEDULED_ARRIVAL'], quantiles['ARRIVAL_TIME'], quantiles['DIVERTED'], quantiles['CANCELLED'], \
        quantiles['SECURITY_DELAY']
    for col in quantiles.columns:
        temp = temp[(temp[col] >= quantiles.loc[0.05,col]) & (temp[col] <= quantiles.loc[0.95,col])]
        # print('After winsorining column ' + col + ' we are left with:')
        # print(temp.shape)
    return temp

data_win = winsorise_data(data)

# log transform the column 'departure_delay' into a new column 'Log_dep_delay'
data['LOG_DEP_DELAY'] = np.log(data['DEPARTURE_DELAY']+1)


# # create a new dataframe where all the quantitative columns are log-transformed
# def logarize_data(data):
#     temp = data.copy()

#EXERCISE IN SESSION

#group = data_win.groupby('AIRLINE').mean()['ARRIVAL_DELAY']

group = data_win[['AIRLINE','ARRIVAL_DELAY']].groupby('AIRLINE').mean()

#data_early = data_win[data_win['DEPARTURE_TIME'] < 1200]

# group = data_win[data_win['DEPARTURE_TIME'] < 1200][['AIRLINE','DEPARTURE_TIME']].groupby('AIRLINE').count()
#
# group['PCT_12PM'] = ((group['DEPARTURE_TIME'])/(data_win[['AIRLINE','DEPARTURE_TIME']].groupby('AIRLINE').count()['DEPARTURE_TIME']))*100

# Normalise all the quantitative columns with standard normalisation
# Apply the sigmoid function to the column 'ARRIVAL_DELAY'
# Perform a left join with the dataset airports.csv, on departure_airport
# Calculate the mean "Departure_delay" for each airline, over the whole dataset
# The mean geohash of "longitude" and "latitude" for each airline
# The number of flights leaving before 12pm for each airline
group = data_win[data_win['DEPARTURE_TIME'] < 1200][['AIRLINE','DEPARTURE_TIME']].groupby('AIRLINE').count()

# The percentage of flights leaving before 12pm, over total flights for each airline
group['PCT_12PM'] = ((group['DEPARTURE_TIME'])/(data_win[['AIRLINE','DEPARTURE_TIME']].groupby('AIRLINE').count()['DEPARTURE_TIME']))*100

# For each airline, the count of flights for each Route (see task1),each route being a separate column
# for each airline, the percentage of flights in each route over all the routes
# Do PCA to reduce the variables 'departure_delay' and 'arrival_delay' to a single component
# For each airline, the percentage delay for each dep_airport, over total delay across all dep_airport