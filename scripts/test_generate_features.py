import pandas as pd

from stock_prediction.inference.generate_features import generate_features

def main():
    output_file = generate_features()

    print(f"\nFeature dataset saved to {output_file}")
    df = pd.read_parquet(output_file)

    print("\nPreview features")
    print(df.head())

    print("\nColumns")
    print(df.columns.to_list())

    print(f"\nRows: {len(df)}")

if __name__=="__main__":
    main()