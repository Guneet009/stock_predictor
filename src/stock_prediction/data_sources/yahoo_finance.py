import pandas as pd
import yfinance as yf
from datetime import datetime

from stock_prediction.utils.logger import logger
from stock_prediction.utils.data_validation import validate_dataframe

class YahooFinanceSource:
    """
    Data source for downloading historical stock prices from Yahoo Finance.
    """
    REQUIRED_COLUMNS = [
        "Date",
        "Open",
        "High",
        "Low",
        "Close",
        "Volume"
    ]

    def __init__(self,ticker:str):
        self.ticker = ticker
    
    def fetch_history(self,start_date:str="2000-01-01",end_date:str|None = None)->pd.DataFrame:
        """
        Download historical price data from Yahoo Finance.
        """
        if end_date is None:
            end_date = datetime.today().strftime("%Y-%m-%d")
        
        logger.info(f"Downloading price data for {self.ticker} from {start_date} to {end_date}")
        

        df = yf.download(
            self.ticker,
            start=start_date,
            end=end_date,
            progress=False
        )
        
        if df is None or df.empty:
            raise ValueError(f"No price data returned for {self.ticker}")
        
        df = self._normaliza_dataframe(df=df)

        print(df.columns)
        validate_dataframe(df=df,required_columns=self.REQUIRED_COLUMNS)

        logger.info(f"Downloaded {len(df)} rows for {self.ticker}")

        return df

    
    def _normaliza_dataframe(self,df:pd.DataFrame)->pd.DataFrame:
        """
        Normalize dataframe schema.
        """
        df = df.reset_index()

        #Flatten MultiIndex columns if present
        if isinstance(df.columns,pd.MultiIndex):
            df.columns = [col[0] for col in df.columns]

        # Standardize_Column_Name
        if "Adj Close" in df.columns:
            df["Close"] = df["Adj Close"]

        #Keep only required columns
        df = df[self.REQUIRED_COLUMNS]

        #Ensure Date columns is datetime
        df["Date"] = pd.to_datetime(df["Date"])

        #Sort by date
        df = df.sort_values("Date")

        # -------------------------------------------------
        # Ensure continuous trading days
        # -------------------------------------------------

        df = df.set_index("Date")

        # Business-day frequency (Mon–Fri)
        df = df.asfreq("B")

        # Forward fill missing prices
        df = df.ffill()

        df = df.reset_index()

        # -------------------------------------------------
        # Enforce numeric columns
        # -------------------------------------------------

        numeric_cols = ["Open", "High", "Low", "Close", "Volume"]

        for col in numeric_cols:
            df[col] = pd.to_numeric(df[col], errors="coerce")


        return df
