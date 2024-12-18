# Poligon Wrapper

## Overview

**Poligon Wrapper** is a Python package designed to interact with Poligon.io API to fetch aggregate bar data for single or multiple stocks over customizable timeframes. It leverages both synchronous and asynchronous API calls for efficient data retrieval. The package is built with logging, progress tracking, and robust error handling to ensure seamless performance.

## Features
- Retrieve **aggregate stock bar data** (open, high, low, close, volume, etc.) for single or multiple stocks.
- Supports multiple timeframes and custom parameters.
- Synchronous and asynchronous API calls for optimal performance.
- Handles large date ranges by splitting them into monthly intervals.
- Built-in logging and progress bar support using `tqdm`.

---

## Installation
To install the package, use the following:

```bash
pip install poligon-wrapper
```

---

## Usage

### 1. Setting the API Key
When you import the package for the first time, you will be asked to provide an API key. The key will be stored in a `.env` file in the same directory as the source code.

You can use the following features to manage your API key:
- **Change the API key**: Update the stored key using a dedicated function.
- **Delete the API key**: Remove the key from the `.env` file.

#### Example:
```python
import poligon_wrapper

# change api_key
poligon_wrapper.change_api_key()

# delete api_key
poligon_wrapper.delete_api_key()
```

---

### 2. Single Stock Data Retrieval
Use the `SingleStockBarRetriever` class to retrieve aggregate bar data for a single stock.

#### Example:
```python
from poligon_wrapper.dataloader_stocks import SingleStockBarRetriever

# Parameters
symbol = "AAPL"
start_date = "2023-02-01"
end_date = "2023-03-01"

# Initialize retriever
retriever = SingleStockBarRetriever(symbol, start_date, end_date)

# Fetch data
data = retriever.get_data()
print(data.head())
```

#### Output:
| time                | open   | high   | low    | close  | volume | ticker |
|---------------------|--------|--------|--------|--------|--------|--------|
| 2023-02-01 09:30:00 | 145.60 | 146.00 | 145.20 | 145.85 | 150000 | AAPL   |
| 2023-02-01 09:31:00 | 145.85 | 146.10 | 145.60 | 146.00 | 160000 | AAPL   |
| ...                 | ...    | ...    | ...    | ...    | ...    | ...    |

---

### 3. Multiple Stock Data Retrieval
Use the `MultipleStockBarRetriever` class to retrieve aggregate bar data for multiple stocks over a given date range.

#### Example:
```python
from poligon_wrapper.dataloader_stocks import MultipleStockBarRetriever

# Parameters
tickers = ["AAPL", "TSLA"]
start_date = "2023-02-01"
end_date = "2023-03-01"

# Initialize retriever
retriever = MultipleStockBarRetriever(tickers, start_date, end_date)

# Fetch data
data = retriever.get_data()
print(data.head())
```

#### Output:
| time                | open   | high   | low    | close  | volume | ticker |
|---------------------|--------|--------|--------|--------|--------|--------|
| 2023-02-01 09:30:00 | 145.60 | 146.00 | 145.20 | 145.85 | 150000 | AAPL   |
| 2023-02-01 09:31:00 | 145.85 | 146.10 | 145.60 | 146.00 | 160000 | AAPL   |
| 2023-02-01 09:30:00 | 195.20 | 196.00 | 194.50 | 195.90 | 200000 | TSLA   |
| ...                 | ...    | ...    | ...    | ...    | ...    | ...    |


---

### 4. Work in Progress: Ticker Retrieval
The `TickerRetriever` class is under development and will allow users to retrieve all available tickers from the Polygon API.

#### Features:
- Retrieve all active tickers.
- Handle large datasets using **pagination**.
- Return data in a structured `pandas.DataFrame` format.

#### Example (Upcoming):
```python
from poligon_wrapper.dataloader_stocks import TickerRetriever

# Initialize retriever
ticker_retriever = TickerRetriever()

# Fetch all tickers
tickers_df = ticker_retriever.fetch_tickers()
print(tickers_df.head())
```

This module will make it easier to work with all available tickers when analyzing or retrieving stock data.

---

## Customizing Parameters
Both `SingleStockBarRetriever` and `MultipleStockBarRetriever` allow you to customize API parameters using the `custom_params` argument:

```python
custom_params = {
    "multiplier": 1,       # Time multiplier for aggregation
    "timespan": "minute", # Timespan (e.g., minute, day)
    "limit": 1000,         # Limit on the number of results
    "api_key": "YOUR_API_KEY" # Your API key
}

retriever = SingleStockBarRetriever("AAPL", "2023-02-01", "2023-03-01", custom_params=custom_params)
data = retriever.get_data()
print(data)
```

---

## Dependencies
This package relies on the following libraries:
- `requests` for synchronous HTTP requests
- `aiohttp` for asynchronous HTTP requests
- `pandas` for data manipulation
- `tqdm` for progress bars
- `nest_asyncio` to handle nested event loops
- `logging` for logging errors and progress

To install all dependencies, run:
```bash
pip install -r requirements.txt
```

---

## Logging
By default, logging is set to `ERROR` level. You can configure the logging level as needed by modifying the `setup_logging` function in `logging_config.py`.

Example:
```python
from poligon_wrapper.logging_config import setup_logging
setup_logging(level=logging.DEBUG)
```

---

## Contributing
Contributions are welcome! To contribute:
1. Fork the repository.
2. Create a new branch for your feature or bug fix.
3. Submit a pull request with a clear description of the changes.

---

## License
This package is licensed under the MIT License.

---

## Author
Filippo Caretti 
filippo.caretti@icloud.com  
fcaretti01




