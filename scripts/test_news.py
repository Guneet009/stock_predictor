from stock_prediction.data_sources.news_source import NewsSource

def main():

    source = NewsSource("AAPL")

    df = source.fetch_news()
    print(df.head())
    print("\nRows:", len(df))

if __name__=="__main__":
    main()