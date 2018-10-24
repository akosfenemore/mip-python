"""
Insert code here for all the transformations you are going to do
"""
import pandas as pd
pd.options.display.max_columns = 20

import numpy as np

from sklearn import preprocessing

# Read the data/flights.csv dataset into Python
data = pd.read_csv('/Users/akofenem/PycharmProjects/mip-python/data/flights.csv', sep=',' , encoding="ISO-8859-1")

# remove the column "DAY_OF_WEEK"
del data['DAY_OF_WEEK']

# rename the column "WHEELS_OFF" to "HAS_WHEELS"
data = data.rename(index=str, columns={'WHEELS_OFF':'HAS_WHEELS'})

# slice the dataset row-wise into 4 equal-sized chunks
dfs = np.array_split(data, 4, axis=0)
#dfs[0], dfs[1], dfs[2], dfs[3]

# concatenate back the chucks produced above into 1 dataset
conc_data = pd.concat([dfs[0], dfs[1], dfs[2], dfs[3]])

# get the slice of the dataset that is only relevant to the airline AA
data_AA = data[data['AIRLINE'].str.match('AA')]
#data = data[data.AIRLINE != 'AA'] #If slice is to be removed from original.

# get the slice of the dataset where delay is <10 and destination is PBI
Data_Small_Delay = data[(data.LATE_AIRCRAFT_DELAY.astype('float') < 10) & (data.DESTINATION_AIRPORT == 'PBI')]
#Data_Small_Delay = Data_Small_Delay[Data_Small_Delay.DESTINATION_AIRPORT == 'PBI']


# fill the blanks in the AIR_SYSTEM_DELAY column with the average of the column itself
data['AIR_SYSTEM_DELAY'] = data['AIR_SYSTEM_DELAY'].fillna(data['AIR_SYSTEM_DELAY'].mean())

# Create a column "has_A", which contains 1 if the airline name contains the letter 'A', 0 otherwise
data['has_A'] = np.where(data['AIRLINE'].apply(lambda x: 'A' in x), 1, 0)

#bget a random sample of the rows in the dataframe
data_sample = data.sample(20)

# normalise the column "DEPARTURE_DELAY" to the range 0-1 with MinMax normalisation
data['DEPARTURE_DELAY_NORMALISED'] = preprocessing.MinMaxScaler().fit_transform(data[['DEPARTURE_DELAY']].values.astype(float))

# binarise the column "ORIGIN_AIRPORT"
data = data.merge(pd.get_dummies(data['ORIGIN_AIRPORT']))
