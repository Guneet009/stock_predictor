from typing import List
import pandas as pd
from stock_prediction.utils.logger import logger

def validate_required_columns(df:pd.DataFrame, required_columns:List[str])-> None:
    """
    Ensure required columns exist in the dataframe.
    """
    missing_columns = [col for col in required_columns if col not in df.columns]

    if missing_columns:
        raise ValueError(f"Missing required columns: {missing_columns}")
    
    logger.info("Column validation passed")

def validate_no_nulls(df:pd.DataFrame, columns:List[str])->None:
    """
    Ensure required columns exist in the dataframe.
    """
    null_count = df[columns].isnull().sum()
    bad_columns = null_count[null_count>0]

    if not bad_columns.empty:
        raise ValueError(f"Null values found in column {bad_columns.to_dict()}")
    
    logger.info("Null validation passed")

def validate_no_duplicates(df:pd.DataFrame, subset:List[str])-> None:
    """
    Ensure no duplicate rows exist.
    """

    duplicates = df.duplicated(subset=subset).sum()

    if duplicates>0:
        raise ValueError(f"Found {duplicates} duplicate rows")
    
    logger.info("Duplicate Validation Passed")

def validate_sorted_by_date(df:pd.DataFrame,date_column:str)->None:
    """
    Ensure no duplicate rows exist.
    """
    if not df[date_column].is_monotonic_increasing:
        raise ValueError(f"Data is not sorted by {date_column}")
    
    logger.info("Date Sorting validation passed")

def validate_dataframe(df:pd.DataFrame,required_columns:List[str],date_column:str="Date")->None:
    """
    Run full validation suite on dataframe.
    """
    logger.info("Starting dataframe validation")

    validate_required_columns(df=df,required_columns=required_columns)
    validate_no_nulls(df=df,columns=required_columns)
    validate_no_duplicates(df=df,subset=[date_column])
    validate_sorted_by_date(df=df,date_column=date_column)

    logger.info("Dataframe validation completed")
