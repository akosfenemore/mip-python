import pandas as pd
pd.options.display.max_columns = 20

import numpy as np

from sklearn import preprocessing

# Read the data/flights.csv dataset into Python
data = pd.read_csv('/Users/akofenem/PycharmProjects/mip-python/data/flights.csv', sep=',' , encoding="ISO-8859-1")

Summary_data = pd.DataFrame()

#Get flights that leave before 12am
Data_Leave_Early = data[(data.DEPARTURE_TIME.astype('float') < 1200)]

table = pd.pivot(Data_Leave_Early, values=data['AIRLINE'], )

# ivot_table(Data_Leave_Early, values=data['AIRLINE'], aggfunc=np.count)

