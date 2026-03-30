import pandas as pd

from stock_prediction.utils.config import config
from stock_prediction.features.technical_features import TechnicalFeatureBuilder

def main():
    price_path = config.get_path("prices")/"AAPL.parquet"

    df = pd.read_parquet(price_path)

    builder = TechnicalFeatureBuilder(df)
    feature_df = builder.build_features()

    print(feature_df.head(20))
    print("\nColumns:")
    print(feature_df.columns.tolist())

if __name__=="__main__":
    main()