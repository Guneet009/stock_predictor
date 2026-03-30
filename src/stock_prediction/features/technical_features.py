import pandas as pd
import numpy as np

from stock_prediction.utils.logger import logger
from stock_prediction.utils.data_validation import validate_required_columns

REQUIRED_COLUMNS = ["Date","Open","High","Low","Close","Volume"]

class TechnicalFeatureBuilder:
    """
    Generate Technical indicators from stock price data
    """

    def __init__(self,df:pd.DataFrame):
        self.df = df.copy()

    def build_features(self)->pd.DataFrame:
        """
        Main method to generate all technical features
        """
        logger.info("Starting technical features generation")
        validate_required_columns(self.df,REQUIRED_COLUMNS)

        self.df["Date"] = pd.to_datetime(self.df["Date"])
        self.df = self.df.sort_values("Date").reset_index(drop=True)

        self._add_returns()
        self._add_moving_averages()
        self._add_volatility()
        self._add_momentum()
        self._add_rsi()
        self._add_macd()

        logger.info("Technical feature generation completed")

        return self.df
    
    def _add_returns(self)->None:
        """
        Add dail and multi day returns
        """
        self.df["return_1d"] = self.df["Close"].pct_change()
        self.df["return_5d"] = self.df["Close"].pct_change(periods=5)

    def _add_moving_averages(self) ->None:
        """
        Add moving averages features
        """

        self.df["ma_5"] = self.df["Close"].rolling(window=5).mean()
        self.df["ma_20"] = self.df["Close"].rolling(window=20).mean()

    def _add_volatility(self)->None:
        """
        Add rolling volatility features
        """
        self.df["volatility_10d"] = self.df["return_1d"].rolling(window=10).std()

    def _add_momentum(self)->None:
        """
        Add momentum feature
        """
        self.df["momentum_10d"] = self.df["Close"]-self.df["Close"].shift(10)

    def _add_rsi(self,period:int=14)->None:
        """
        Add RSI (Relative Strength Index)
        """
        delta = self.df["Close"].diff()

        gain = delta.where(delta > 0, 0.0)
        loss = -delta.where(delta < 0, 0.0)

        avg_gain = gain.rolling(window=period).mean()
        avg_loss = loss.rolling(window=period).mean()

        rs = avg_gain/avg_loss
        self.df["rsi_14"] = 100 - (100/ (1+rs))

    def _add_macd(self)->None:
        """
        Add MACD and signal line
        """
        ema_12 = self.df["Close"].ewm(span=12, adjust=False).mean()
        ema_26 = self.df["Close"].ewm(span=26, adjust=False).mean()

        self.df["macd"] = ema_12 - ema_26
        self.df["macd_signal"] = self.df["macd"].ewm(span=9,adjust=False).mean()


        