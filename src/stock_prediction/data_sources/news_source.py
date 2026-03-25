import pandas as pd
import feedparser
import re
from datetime import datetime
from html import unescape
from typing import Any

from stock_prediction.utils.logger import logger


class NewsSource:
    """
    Fetch financial news using Google News RSS.
    """

    REQUIRED_COLUMNS = [
        "Date",
        "Title",
        "Source",
        "Link",
        "Summary",
        "Query",
        "IngestedAt",
    ]

    def __init__(self, query: str):
        self.query = query

    def fetch_news(self) -> pd.DataFrame:
        """
        Fetch news articles for a given query.
        """
        url = f"https://news.google.com/rss/search?q={self.query}"

        logger.info(f"Fetching news for query: {self.query}")

        feed = feedparser.parse(url)

        if not feed.entries:
            raise ValueError("No news articles found")

        records = []

        for entry in feed.entries:
            record = {
                "Date": self._parse_date(entry),
                "Title": self._safe_str(entry.get("title")),
                "Source": self._extract_source(entry),
                "Link": self._safe_str(entry.get("link")),
                "Summary": self._clean_html(self._safe_str(entry.get("summary"))),
                "Query": self.query,
                "IngestedAt": datetime.utcnow(),
            }

            records.append(record)

        df = pd.DataFrame(records)
        df = self._normalize_dataframe(df)

        logger.info(f"Fetched {len(df)} news articles")

        return df

    def _parse_date(self, entry: Any) -> datetime:
        """
        Convert published date into datetime.
        """
        if hasattr(entry, "published_parsed") and entry.published_parsed:
            return datetime(*entry.published_parsed[:6])

        return datetime.utcnow()

    def _safe_str(self, value: Any) -> str:
        """
        Safely convert unknown feedparser field into string.
        """
        if value is None:
            return ""

        if isinstance(value, list):
            return " ".join(str(v) for v in value)

        return str(value).strip()

    def _extract_source(self, entry: Any) -> str:
        """
        Safely extract source title from RSS entry.
        """
        source = entry.get("source", {})

        if isinstance(source, dict):
            return self._safe_str(source.get("title"))

        return ""

    def _clean_html(self, text: str) -> str:
        """
        Remove HTML tags and decode HTML entities.
        """
        text = re.sub(r"<.*?>", "", text)
        text = unescape(text)
        return text.strip()

    def _normalize_dataframe(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        Normalize schema and clean data.
        """
        df = df[self.REQUIRED_COLUMNS]

        df["Date"] = pd.to_datetime(df["Date"])
        df["IngestedAt"] = pd.to_datetime(df["IngestedAt"])

        df = df.sort_values("Date")

        # Remove duplicates
        df = df.drop_duplicates(subset=["Title", "Date"])

        return df