import matplotlib as plt
import pandas as pd

pd.options.display.max_columns = 50

import numpy as np

# import seaborn as sns

# from sklearn import preprocessing


# Function to define quantitative columns
def quantitative_columns(data):
    init = data.describe()

    del init['YEAR'], init['MONTH'], init['DAY'], init['DAY_OF_WEEK'], init['FLIGHT_NUMBER'], \
        init['SCHEDULED_DEPARTURE'], init['DEPARTURE_TIME'], init['SCHEDULED_ARRIVAL'], init['ARRIVAL_TIME'], \
        init['DIVERTED'], init['CANCELLED']
    return init.columns


# Read the data/flights.csv dataset into Python
data = pd.read_csv('/Users/akofenem/PycharmProjects/mip-python/data/flights.csv', sep=',', encoding="ISO-8859-1")

# Create a "Route" column by merging departure airport and destination airport
data['ROUTE'] = data['ORIGIN_AIRPORT'].astype('str') + ' - ' + data['DESTINATION_AIRPORT'].astype('str')


# Write a function that, for all the quantitative cols, returns mean, quartiles, stdev, max, kurtosis
def quant_df(dataframe):
    return pd.concat([dataframe.describe(), dataframe.kurtosis().to_frame().transpose().rename(index={0: 'kurt'})])


data_desc = quant_df(data)

# replace the NaN with mean values in the column 'AIR_SYSTEM_DELAY'
data['AIR_SYSTEM_DELAY'] = data['AIR_SYSTEM_DELAY'].fillna(data['AIR_SYSTEM_DELAY'].mean())

# Remove outliers for 'departure_delay' - remove rows in excess of 3 standard deviations from mean
data = data[(data['DEPARTURE_DELAY'] > data['DEPARTURE_DELAY'].describe()['mean'] - 3 *
             data['DEPARTURE_DELAY'].describe()['std']) &
            (data['DEPARTURE_DELAY'] < data['DEPARTURE_DELAY'].describe()['mean'] + 3 *
             data['DEPARTURE_DELAY'].describe()['std'])]


# Winsorise all quantitative columns to a 95% upper and lower bound

def winsorise_data(data):
    temp = data.copy()
    quantiles = temp.quantile([0.05, 0.95])
    del quantiles['YEAR'], quantiles['MONTH'], quantiles['DAY'], quantiles['DAY_OF_WEEK'], quantiles['FLIGHT_NUMBER'], \
    quantiles['SCHEDULED_DEPARTURE'], \
        quantiles['DEPARTURE_TIME'], quantiles['SCHEDULED_ARRIVAL'], quantiles['ARRIVAL_TIME'], quantiles['DIVERTED'], \
    quantiles['CANCELLED'], \
        quantiles['SECURITY_DELAY']
    for col in quantiles.columns:
        temp = temp[(temp[col] >= quantiles.loc[0.05, col]) & (temp[col] <= quantiles.loc[0.95, col])]
        # print('After winsorising column ' + col + ' we are left with:')
        # print(temp.shape)
    return temp


data_win = winsorise_data(data)


# log transform the column 'departure_delay' into a new column 'Log_dep_delay'
def log_transform_column(data, colname):
    temp_data = data.copy()
    temp_data['LOG_' + colname] = np.log(temp_data[colname] - temp_data[colname].describe()['min'] + 0.1)
    return temp_data


data_with_log_dep_delay = log_transform_column(data, 'DEPARTURE_DELAY')


# Create a new dataframe where all the quantitative columns are log-transformed
def logarize_data(data):
    Q_col = quantitative_columns(data)
    for col in Q_col:
        data = log_transform_column(data, col)
    return data


data_log = logarize_data(data)


# Normalise all the quantitative columns with standard normalisation


def normalise_columns(data):
    temp_data = data.copy()
    Q_col = quantitative_columns(temp_data)
    for col in Q_col:
        temp_data['NORM_' + col] = preprocessing.MinMaxScaler().fit_transform(temp_data[[col]].values.astype(float))
    return temp_data


data_norm = normalise_columns(data)


# Apply the sigmoid function to the column 'ARRIVAL_DELAY'

def sigmoid_columns(data):
    temp_data = data.copy()
    Q_col = quantitative_columns(temp_data)
    for col in Q_col:
        temp_data['SIG_' + col] = 1 / (1 + np.exp(-temp_data[col]))
    return temp_data


data_sig = sigmoid_columns(data)

# Perform a left join with the dataset airports.csv, on departure_airport

data_join = pd.merge(left=data,
                     right=pd.read_csv('/Users/akofenem/PycharmProjects/mip-python/data/airports.csv', sep=',',
                                       encoding="ISO-8859-1"),
                     how='left',
                     left_on='ORIGIN_AIRPORT',
                     right_on='IATA_CODE',
                     left_index=False,
                     right_index=False,
                     sort=True,
                     suffixes=('_x', '_y'),
                     copy=True,
                     indicator=False,
                     validate=None)


# Calculate the mean "Departure_delay" for each airline, over the whole dataset
def summarise_mean_for_airline(data):
    return data[['AIRLINE', 'ARRIVAL_DELAY']].groupby('AIRLINE').mean()


mean_summary = summarise_mean_for_airline(data)


# TODO: The mean geohash of "longitude" and "latitude" for each airline

# data_geo = data_join[['AIRLINE', 'LATITUDE', 'LONGITUDE']].groupby('AIRLINE').mean()


# The number of flights leaving before 12pm for each airline
def number_of_early_flights(data):
    return data[data['DEPARTURE_TIME'] < 1200][['AIRLINE', 'DEPARTURE_TIME']].groupby('AIRLINE').count()


number_summary = number_of_early_flights(data)


# The percentage of flights leaving before 12pm, over total flights for each airline
def pct_of_early_flights(data):
    number_of_early_flights(data)['PCT_12PM'] = ((number_of_early_flights(data)['DEPARTURE_TIME']) / (
        data[['AIRLINE', 'DEPARTURE_TIME']].groupby('AIRLINE').count()['DEPARTURE_TIME'])) * 100


pct_summary = pct_of_early_flights(data)


# For each airline, the count of flights for each Route (see task1),each route being a separate column

def airline_flight_count(data):
    return pd.pivot_table(data=data[['AIRLINE','ROUTE']],
                          index=data['AIRLINE'],
                          columns=data['ROUTE'],
                          aggfunc=len,
                          # margins=True,
                          # margins_name='All'
                          )


data_flight_count = airline_flight_count(data)['ROUTE']

def airline_flight_delay(data):
    return pd.pivot_table(data=data,
                          values=['DEPARTURE_DELAY'],
                          index=['AIRLINE'],
                          columns=['ROUTE'],
                          aggfunc=np.sum,
                          # margins=True,
                          # margins_name='All'
                          )

data_flight_delay = airline_flight_delay(data)['DEPARTURE_DELAY']

# TODO:for each airline, the percentage of flights in each route over all the routes
#


data_flight_pct = pd.DataFrame()
col = data_flight_count.columns
data_flight_pct[col] = data_flight_count[col].div(data_flight_count[col].sum(axis=1), axis=0).multiply(100)


#
#
# data_flight_pct = airline_flight_pct(data,data_flight_count)
#
# for col in data_flight_count['ROUTE'].columns:
#    data_flight_pct = data_flight_count['ROUTE'][col]/data_flight_count['TOTAL_FLIGHTS']
#

# TODO: Do PCA to reduce the variables 'departure_delay' and 'arrival_delay' to a single component


# TODO: For each airline, the percentage delay for each dep_airport, over total delay across all dep_airport
