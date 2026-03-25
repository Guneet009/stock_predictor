import pandas as pd
from pathlib import Path

from stock_prediction.utils.logger import logger
from stock_prediction.utils.config import config

from stock_prediction.data_sources.yahoo_finance import YahooFinanceSource

def fetch_prices()-> Path:
    """
    Fetch Stock price data and store locally
    """

    ticker = config.get("stock_symbol")
    logger.info(f"Starting data ingestion for ticker {ticker}")

    #Intialize data source
    source = YahooFinanceSource(ticker=ticker)

    #Determine output path
    output_dir = config.get_path("prices")
    output_dir.mkdir(parents=True,exist_ok=True)

    output_file = output_dir/f"{ticker}.parquet"

    #Fetch historical data
    if output_file.exists():
        existing_df = pd.read_parquet(output_file)
        last_date = existing_df["Date"].max()
        logger.info(f"Existing dataset found. Last date: {last_date}")
        start_date = (last_date + pd.Timedelta(days=1)).strftime("%Y-%m-%d")
        df_new = source.fetch_history(start_date=start_date)

        if df_new is None or df_new.empty:
            logger.info("No new rows downloaded")
            df = existing_df
        else:
            df = pd.concat([existing_df, df_new]).drop_duplicates(subset=["Date"])

    else:
        df = source.fetch_history()

    #Save dataset
    tmp_file = output_file.parent / f"{output_file.stem}_tmp.parquet"
    df.to_parquet(tmp_file, index=False)
    tmp_file.replace(output_file)

    logger.info(f"Saved file to {output_file}")
    logger.info(f"Rows saved:{len(df)}")

    return output_file

