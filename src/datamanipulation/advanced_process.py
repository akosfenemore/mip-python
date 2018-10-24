import pandas as pd
pd.options.display.max_columns = 20

import numpy as np

from sklearn import preprocessing

# Read the data/flights.csv dataset into Python
data = pd.read_csv('/Users/akofenem/PycharmProjects/mip-python/data/flights.csv', sep=',' , encoding="ISO-8859-1")

# Create a "Route" column by merging departure airport and destination airport
data['ROUTE'] = data['ORIGIN_AIRPORT'].astype('str') + ' - ' + data['DESTINATION_AIRPORT'].astype('str')

# Write a function that, for all the quantitative cols, returns mean, quartiles, stdev, max, kurtosis
def quant(data):
    return pd.concat([data.describe(),data.kurtosis().to_frame().transpose().rename(index={0:'kurt'})])

# replace the NaN with mean values in the column 'AIR_SYSTEM_DELAY'
# Remove outliers for 'departure_delay' - remove rows in excess of 3 standard deviations from mean
# Winsorise all quantitative columns to a 95% upper and lower bound
# log transform the column 'departure_delay' into a new column 'Log_dep_delay'
# create a new dataframe where all the quantitative columns are log-transformed
# Normalise all the quantitative columns with standard normalisation
# Apply the sigmoid function to the column 'ARRIVAL_DELAY'
# Perform a left join with the dataset airports.csv, on departure_airport
# Calculate the mean "Departure_delay" for each airline, over the whole dataset
# The mean geohash of "longitude" and "latitude" for each airline
# The number of flights leaving before 12pm for each airline
# The percentage of flights leaving before 12pm, over total flights for each airline
# For each airline, the count of flights for each Route (see task1),each route being a separate column
# for each airline, the percentage of flights in each route over all the routes
# Do PCA to reduce the variables 'departure_delay' and 'arrival_delay' to a single component
# For each airline, the percentage delay for each dep_airport, over total delay across all dep_airport