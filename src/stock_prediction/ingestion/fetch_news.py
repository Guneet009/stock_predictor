import pandas as pd

from pathlib import Path
from stock_prediction.utils.config import config
from stock_prediction.utils.logger import logger
from stock_prediction.data_sources.news_source import NewsSource

def fetch_news()->Path:
    """
    Fetch news article for given stock symbol
    """
    query = config.get("stock_symbol")
    logger.info(f"Starting news ingestion for: {query}")

    source = NewsSource(query=query)

    output_dir = config.get_path("news")
    output_dir.mkdir(parents=True,exist_ok=True)

    output_file = output_dir/f"{query}_news.parquet"

    # ----------------------------------------
    # Incremental update logic
    # ----------------------------------------

    if output_file.exists():
        existing_df = pd.read_parquet(output_file)

        logger.info(f"Existing news dataset found with {len(existing_df)} rows")

        df_new = source.fetch_news()

        if df_new is None or df_new.empty:
            logger.info("No new news article found")
            df = existing_df
        else:
            df = pd.concat([existing_df,df_new]).drop_duplicates(subset=["Title","Date"])
    
    else:
        df = source.fetch_news()

# ----------------------------------------
# Safe write
# ----------------------------------------

    tmp_file = output_file.parent / f"{output_file.stem}_tmp.parquet"
    df.to_parquet(tmp_file,index=False)

    tmp_file.replace(output_file)

    logger.info(f"Saved news data to {output_file}")
    logger.info(f"Total news rows saved: {len(df)}")

    return output_file
        