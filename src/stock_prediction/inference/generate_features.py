import pandas as pd

from pathlib import Path
from stock_prediction.utils.logger import logger
from stock_prediction.utils.config import config
from stock_prediction.features.technical_features import TechnicalFeatureBuilder

def generate_features()->Path:
    """
    Generate technical features from raw stock price data
    and save feature dataset
    """
    ticker = config.get("stock_symbol")

    logger.info(f"Starting feature generation {ticker}")

    price_path = config.get_path("prices")/f"{ticker}.parquet"

    print(f"Ticker: {ticker}")
    print(f"Price Path: {price_path}")
    print(f"Exists: {price_path.exists()}")

    if not price_path.exists():
        raise FileNotFoundError(f"Price file now found at {price_path}")
    
    df = pd.read_parquet(price_path)
    logger.info(f"Loaded {len(df)} rows of raw price")

    builder = TechnicalFeatureBuilder(df)
    feature_df = builder.build_features()

    logger.info("Technical features generated")

    initial_rows = len(feature_df)

    feature_df = feature_df.dropna().reset_index(drop=True)

    dropped_rows = initial_rows - len(feature_df)

    logger.info(f"Dropped {dropped_rows} rows with NaN values")
    logger.info(f"Final feature data has {len(feature_df)} rows")

    output_dir = config.get_path("features")
    output_dir.mkdir(parents=True,exist_ok=True)

    output_file = output_dir/f"{ticker}_features.parquet"
    tmp_file = output_file.parent/f"{output_file.stem}_tmp.parquet"

    feature_df.to_parquet(tmp_file,index=False)
    tmp_file.replace(output_file)

    logger.info(f"Saved feature dataset to {output_file}")
    return output_file