from src.logexception.exceptionhandler import CustomUserException
import os.path
# Error & Exception handling

# Import logger from framework
from src.logexception.logframework import CustomLogger

# Create logger
mylog = CustomLogger().logger

#Define function to parse csv and get columns
def parse_csv_and_get_columns(filename):

    try:
        # Read file
        mylog.info('Reading file')
        if os.path.isfile(filename):
            csvFile = open(filename, 'r')
        else:
            raise CustomUserException
        #Read lines in the file
        mylog.info('Reading lines in the file')
        lines = csvFile.readlines()
        mylog.info('Splitting lines in file')
        for line in lines[1:]:
            val = line.split(",")
            test_str_div = val[0] / val[11]
            test_zero_div = (int(val[0]) / int(val[11]))
    except CustomUserException:
        mylog.error('File not found!', exc_info=True)
    except TypeError:
        mylog.error('Can\'t divide these!', exc_info=True)
    except ZeroDivisionError:
        mylog.error('Zero Division Error!', exc_info=True)


if __name__ == "__main__":
    parse_csv_and_get_columns(filename="data/flights.csv")