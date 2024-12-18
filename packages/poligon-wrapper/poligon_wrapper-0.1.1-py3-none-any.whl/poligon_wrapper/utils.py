from datetime import datetime, timedelta
from dateutil.relativedelta import relativedelta
import ssl, os
import pandas as pd
from datetime import datetime, date, time
from dotenv import find_dotenv, load_dotenv
from poligon_wrapper import polygon_apikey

"""
---------------------------------------------------------------------------------------------------------
"""
"""
---------------------------------------------------------------------------------------------------------
"""



"""
---------------------------------------------------------------------------------------------------------
"""

default_params = {
            "multiplier": 1,
            "api_key": polygon_apikey,
            "adjusted": "true",
            "sort": "asc",
            "timespan": "minute",
            "limit": 50000
        }

"""
---------------------------------------------------------------------------------------------------------
"""

class MonthlyDateRange:
    def __init__(self, start_date: str, end_date: str):
        """
        Initialize the date range.

        Parameters:
        start_date (str): Start date in 'MM-DD-YYYY' format.
        end_date (str): End date in 'MM-DD-YYYY' format.
        """
        self.start_date = datetime.strptime(start_date, "%Y-%m-%d")
        self.end_date = datetime.strptime(end_date, "%Y-%m-%d")
    
    def get_monthly_intervals(self):
        """
        Splits the date range into monthly intervals.

        Returns:
        list of tuples: List of (start_date, end_date) tuples for each month in the range.
        """
        date_ranges = []
        current_start = self.start_date

        while current_start <= self.end_date:
            # Determine the last day of the current month
            current_end = (current_start + relativedelta(months=1)).replace(day=1) - timedelta(days=1)
            
            # Adjust the end date if it goes beyond the specified end date
            if current_end > self.end_date:
                current_end = self.end_date
            
            # Append the start and end of the current month to the list
            date_ranges.append((current_start.strftime("%Y-%m-%d"), current_end.strftime("%Y-%m-%d")))
            
            # Move to the first day of the next month
            current_start = current_end + timedelta(days=1)

        return date_ranges


"""
---------------------------------------------------------------------------------------------------------
"""


# ssl context to help aiohttp requests

ssl_context = ssl.create_default_context()
ssl_context.check_hostname = False
ssl_context.verify_mode = ssl.CERT_NONE


"""
---------------------------------------------------------------------------------------------------------
"""

def get_columns_and_types(df: pd.DataFrame) -> dict:
    """
    Given a pandas DataFrame, return a dictionary mapping column names to SQLite data types.
    
    Extends type inference to cover common SQLite types including strings, dates, and others.
    
    :param df: pandas DataFrame
    :return: Dictionary of column names and SQLite data types
    """
    type_mapping = {
        "int64": "INTEGER",
        "float64": "REAL",
        "object": "TEXT",
        "bool": "INTEGER",
        "datetime64[ns]": "DATETIME",
        "timedelta[ns]": "TEXT"  # SQLite has no direct duration type
    }

    # Infer column types
    columns = {}
    for col, dtype in df.dtypes.items():
        dtype_str = str(dtype)
        sqlite_type = type_mapping.get(dtype_str, "TEXT")  # Default to TEXT if type is unknown
        columns[col] = sqlite_type

    return columns


"""
---------------------------------------------------------------------------------------------------------
"""

# Function to format datetime, date, or time columns
def format_datetime_columns(dataframe: pd.DataFrame) -> pd.DataFrame:
    """
    Format datetime-related columns in a DataFrame:
    - %Y-%m-%d %H:%M:%S for datetime.datetime
    - %Y-%m-%d for datetime.date
    - %H:%M:%S for datetime.time

    :param dataframe: Input pandas DataFrame
    :return: DataFrame with formatted datetime columns
    """
    for column in dataframe.columns:
        if dataframe[column].dtype == "datetime64[ns]":  # Handle pandas datetime
            dataframe[column] = dataframe[column].dt.strftime("%Y-%m-%d %H:%M:%S")
        elif isinstance(dataframe[column].iloc[0], datetime):  # Handle Python datetime
            dataframe[column] = dataframe[column].apply(lambda x: x.strftime("%Y-%m-%d %H:%M:%S") if pd.notnull(x) else None)
        elif isinstance(dataframe[column].iloc[0], date):  # Handle Python date
            dataframe[column] = dataframe[column].apply(lambda x: x.strftime("%Y-%m-%d") if pd.notnull(x) else None)
        elif isinstance(dataframe[column].iloc[0], time):  # Handle Python time
            dataframe[column] = dataframe[column].apply(lambda x: x.strftime("%H:%M:%S") if pd.notnull(x) else None)
    return dataframe


"""
---------------------------------------------------------------------------------------------------------
"""
