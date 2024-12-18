import requests
import pandas as pd
import logging
from tqdm import tqdm
from .logging_config import setup_logging
from .utils import MonthlyDateRange, ssl_context, default_params

# import for async calls
import asyncio, nest_asyncio, aiohttp
nest_asyncio.apply()


# set-up logger 
setup_logging(level=logging.ERROR)

# create a logger for this file
logger = logging.getLogger(__name__)

"""
-------------------------------------------------------------------------------------------------------------------
"""


class SingleStockBarRetriever:
    def __init__(self, symbol: str, start_date: str, end_date: str, custom_params: dict = None, session: aiohttp.ClientSession = None):
        """
        Initialize the data retriever for a specific ticker symbol. The maximum time frame 
        allowed is 50,000 minutes of data.

        Parameters:
        symbol (str): The stock ticker symbol.
        params (dict): A dictionary containing the API call parameters, including:
            - multiplier (int): Time multiplier for aggregation.
            - api_key (str): API key for Polygon.io.
            - adjusted (str): Whether to adjust the data (e.g., "true" or "false").
            - sort (str): Sorting order of the results (e.g., "asc" or "desc").
            - timespan (str): Timespan for the data (e.g., "minute", "day").
            - limit (int): Maximum number of results to return.
        """
        self.session = session
        self.symbol = symbol
        self.start_date = str(start_date)
        self.end_date = str(end_date)
        
        
        # Update defaults with any values from custom_params
        self.params = {**default_params, **(custom_params or {})}

    @property
    def URL(self):
        return (
            f"https://api.polygon.io/v2/aggs/ticker/{self.symbol}/"
            f"range/{self.params.get('multiplier')}/{self.params.get('timespan')}/"
            f"{self.start_date}/{self.end_date}?"
            f"adjusted={self.params.get('adjusted')}&sort={self.params.get('sort')}&"
            f"limit={self.params.get('limit')}&apiKey={self.params.get('api_key')}"
        )
        
    @property
    def columns(self):
        return {
            "v" : "volume",
            "vw" : "volume_weighted_average_price",
            "o" : "open",
            "c" : "close",
            "h" : "high",
            "l" : "low",
            "t" : "time",
            "n" : "transactions"
        }


    def get_data(self):
        try:
            # try getting the data
            logging.info(f"Attempting to retrieve data from: {self.URL}")
            response = requests.get(self.URL)

            # Check response status
            if response.status_code == 200:
                logging.info("Response received successfully.")
                data = response.json()

                # Check if the 'results' key is present in the data
                if "results" not in data:
                    logging.warning(f"No 'results' found in the response data: {data}")
                    return None  

                # Get data into a DataFrame and clean it 
                df = pd.DataFrame(data["results"])
                logging.debug(f"Raw data retrieved: {df.head()}")  # Log the first few rows of the data

                # Clean df
                df.rename(columns=self.columns, inplace=True)
                df['time'] = pd.to_datetime(df['time'], unit="ms")
                df['ticker']= self.symbol
                
                return df
              
            else:
                logging.error(f"Failed to retrieve data for {self.URL}: HTTP {response.status_code}")
                response.raise_for_status()

        except requests.exceptions.RequestException as e:
            logging.error(f"Request exception occurred: {e}")
            return None 

        except Exception as e:
            logging.error(f"An unexpected error occurred: {e}")
            return None
        


    async def get_data_async(self):
        try:
            logger.info(f"Attempting to retrieve data from: {self.URL}")
            async with self.session.get(self.URL, timeout=None, ssl=ssl_context) as response:
                if response.status == 200:
                    data = await response.json()

                    if "results" not in data:
                        logger.warning(f"No 'results' found in response data for {self.symbol}: {self.URL}")
                        return pd.DataFrame()  # Return empty DataFrame if no results

                    df = pd.DataFrame(data["results"])
                    logger.debug(f"Raw data retrieved: {df.head()}")

                    # Rename and clean the DataFrame
                    df.rename(columns=self.columns, inplace=True)
                    df['time'] = pd.to_datetime(df['time'], unit="ms")
                    df['ticker']= self.symbol
                    return df

                else:
                    logger.error(f"Failed to retrieve data: HTTP {response.status}")
                    return pd.DataFrame()

        except Exception as e:
            logger.error(f"An error occurred while fetching data: {e}")
            return pd.DataFrame()        



"""
-------------------------------------------------------------------------------------------------------------------
"""




class MultipleStockBarRetriever():
    def __init__(self, symbols: list[str], start_date: str, end_date: str, custom_params: dict = None):
        """
        Initializes asynchronous API calls for multiple symbols.

        Parameters:
        - symbols (list of str): Stock ticker symbols.
        - start_date (str): Start date for data retrieval.
        - end_date (str): End date for data retrieval.
        - custom_params (dict, optional): Dictionary to override default parameters.
        """
        self.symbols = symbols
        self.start_date = str(start_date)
        self.end_date = str(end_date)
        
        
        # Update defaults with any values from custom_params
        self.params = {**default_params, **(custom_params or {})}
        

    @property
    def date_ranges(self):
        """
        Generate monthly intervals for the given date range.

        Returns:
        list of tuples: List of (start_date, end_date) tuples for each month.
        """
        return MonthlyDateRange(self.start_date, self.end_date).get_monthly_intervals()


    async def fetch_bars(self, symbol, start_date, end_date, session):
        """
        Fetches aggregate bar data for a symbol within a specific date range.
        """

        retriever = SingleStockBarRetriever(symbol, start_date, end_date, custom_params=self.params, session=session)
        return await retriever.get_data_async()


    async def main(self):
        """
        Main function to fetch data asynchronously for all symbols over the specified date ranges.
        """        
        async with aiohttp.ClientSession() as session:

            # define the tasks
            tasks = []
            
            # loop through each symbol, each time frame:
            prog_bar = tqdm(total = len(self.symbols), desc="Finding historical Prices", dynamic_ncols=True, position=0, leave=True)
            for symbol in self.symbols:
                for start_date, end_date in self.date_ranges:
                    tasks.append(self.fetch_bars(symbol, start_date, end_date, session))
                    prog_bar.update()
                
            prog_bar.close()
            logger.info("Generated all tasks for data retrieval")

            # gather all the tasks
            results = await asyncio.gather(*tasks)
            grouped_bars_df = pd.concat(results)
            logger.info("Finished gathering all the tasks")


            return grouped_bars_df
        
    
    def get_data(self):
        """
        Runs the asynchronous main function to fetch data and return combined DataFrame.
        """
        return asyncio.run(self.main())

    

    
"""
-------------------------------------------------------------------------------------------------------------------
"""


