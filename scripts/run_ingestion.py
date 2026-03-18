from stock_prediction.ingestion.fetch_prices import fetch_prices

def main():
    output_file = fetch_prices()

    print(f"Date saved to {output_file}")

if __name__=="__main__":
    main()