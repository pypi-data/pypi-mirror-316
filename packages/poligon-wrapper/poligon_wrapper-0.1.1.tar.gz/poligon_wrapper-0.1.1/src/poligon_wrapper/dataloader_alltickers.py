import requests
import pandas as pd
import logging
from .logging_config import setup_logging
from poligon_wrapper import polygon_apikey


# set-up logger 
setup_logging(level=logging.ERROR)

# create a logger for this file
logger = logging.getLogger(__name__)

class TickerRetriever:
    def __init__(self, api_key: str = polygon_apikey):
        """
        Initialize the TickerRetriever with the API key.

        Parameters:
        api_key (str): The API key for accessing the Polygon API.
        """
        self.api_key = api_key
        self.base_url = "https://api.polygon.io/v3/reference/tickers"
        self.active = True
        self.limit = 1000

    def fetch_tickers(self):
        """
        Fetch all active tickers from the Polygon API, handling pagination.

        Returns:
        pd.DataFrame: A DataFrame containing all retrieved tickers.
        """
        all_tickers = []
        url = f"{self.base_url}?active={self.active}&limit={self.limit}&apiKey={self.api_key}"

        logging.info(f"Fetching tickers from: {url}")

        while url:
            response = self._get_response(url)
            if response:
                all_tickers.append(pd.DataFrame(response.get("results", [])))
                # Get the next URL for pagination
                url = response.get("next_url", None)
                if url:
                    url += f"&active={self.active}&limit={self.limit}&apiKey={self.api_key}"
            else:
                break

        # Concatenate all DataFrames into one and reset the index
        return pd.concat(all_tickers, ignore_index=True) if all_tickers else pd.DataFrame()

    def _get_response(self, url):
        """
        Send a GET request to the provided URL and return the JSON response.

        Parameters:
        url (str): The URL to send the request to.

        Returns:
        dict: The JSON response from the API.
        """
        try:
            response = requests.get(url)
            response.raise_for_status()  # Raise an error for bad responses
            logging.info("Data retrieved successfully.")
            return response.json()
        except requests.exceptions.RequestException as e:
            logging.error(f"Error fetching data: {e}")
            return None

# Usage example
if __name__ == "__main__":
    ticker_retriever = TickerRetriever(polygon_apikey)
    all_tickers_df = ticker_retriever.fetch_tickers()
