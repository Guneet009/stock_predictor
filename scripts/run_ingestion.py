from stock_prediction.ingestion.fetch_prices import fetch_prices
from stock_prediction.ingestion.fetch_news import fetch_news

def main():

    output_price = fetch_prices()
    print(f"Date saved to {output_price}")
    output_file = fetch_news()
    print(f"\nNews data saved to {output_file}")

if __name__=="__main__":
    main()