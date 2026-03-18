import pandas as pd

from stock_prediction.utils.data_validation import validate_dataframe

def main():

    df = pd.DataFrame({
        "Date":pd.date_range("2023-01-01",periods=5),
        "Open":[10,11,12,13,14],
        "High":[11,12,13,14,15],
        "Low":[9,10,11,12,13],
        "Close":[10.5,11.5,12.5,13.5,14.5],
        "Volume":[100,120,130,140,150]
    })
    required_col = ["Date","Open","High","Low","Close","Volume"]

    validate_dataframe(df=df,required_columns=required_col)

if __name__=="__main__":
    main()