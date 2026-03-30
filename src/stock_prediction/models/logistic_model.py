import pandas as pd
from pathlib import Path

from stock_prediction.utils.config import config
from stock_prediction.utils.logger import logger

from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, classification_report

class LogisticModel:
    """
    Logistic Regression model
    """
    def __init__(self) -> None:
        self.model = LogisticRegression(max_iter=1000)

    def load_data(self) -> pd.DataFrame:
        """
        Load feature dataset
        """
        ticker = config.get("stock_symbol")
        features_path = config.get_path("features")/f"{ticker}_features.parquet"

        if not features_path.exists():
            raise FileNotFoundError(f"File now found {features_path}")
        
        df = pd.read_parquet(features_path)

        logger.info(f"Feature dataset loaded with rows {len(df)}")

        return df
    
    def create_target(self,df:pd.DataFrame) -> pd.DataFrame:
        """
        Create binary target: 1 = price go up, 0 = price go down
        """
        df = df.copy()
        df["future_return"] = df["Close"].pct_change().shift(-1)
        df["target"] = (df["future_return"]>0).astype(int)
        df = df.dropna().reset_index(drop=True)

        return df
    
    def prepare_features(self,df:pd.DataFrame):
        """
        Prepare X and y
        """
        feature_cols = [
            "return_1d",
            "return_5d",
            "ma_5",
            "ma_20",
            "volatility_10d",
            "momentum_10d",
            "rsi_14",
            "macd",
            "macd_signal",
        ]

        X = df[feature_cols]
        y = df["target"]

        return X,y
    
    def train(self):
        """
        Train and evaluate model
        """
        df = self.load_data()
        df = self.create_target(df)

        X,y = self.prepare_features(df)

        #Important: time based split
        split_index = int(len(df)*0.8)

        X_train,X_test = X[:split_index],X[split_index:]
        y_train,y_test = y[:split_index],y[split_index:]

        logger.info(f"Training sample: {len(X_train)}")
        logger.info(f"Test sample: {len(X_test)}")
        
        #Model training
        self.model.fit(X_train,y_train)

        #Prediction
        y_pred = self.model.predict(X_test)

        #Evaluation
        accuracy = accuracy_score(y_test,y_pred)

        logger.info(f"Model accuracy: {accuracy}")

        print("\nClassification Report:")
        print(classification_report(y_test,y_pred))

        return self.model