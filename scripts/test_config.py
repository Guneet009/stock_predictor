import sys
from pathlib import Path

from stock_prediction.utils.config import config


def main():
    print("----- Testing Config Loader -----")

    # Test Project Root Detection
    print("Project Root:")
    print(config.project_root)

    # Test Stock Symbol
    print("\nStock Symbol:")
    print(config.get("stock_symbol"))

    # Test prediction section
    print("\nPrediction section:")
    print(config.get_section("prediction"))

    # Test data path
    print("\nPrice data path:")
    print(config.get_path("prices"))


if __name__ == "__main__":
    main()