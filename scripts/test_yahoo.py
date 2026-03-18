from stock_prediction.data_sources.yahoo_finance import YahooFinanceSource

def main():
    source = YahooFinanceSource("AAPL")

    df = source.fetch_history(start_date="2020-01-01")

    print(df.head(10))
    print("\nRows:",len(df))
if __name__=="__main__":
    main()