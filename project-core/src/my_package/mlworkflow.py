from abc import ABC, abstractmethod
from typing import Tuple, Dict, Any, Union
import pandas as pd
import numpy as np
from scipy.sparse import csr_matrix
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.pipeline import Pipeline
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, f1_score
from textblob import TextBlob  # For weak labeling
from zenml import pipeline, step

# Strategy Interfaces
class LabelingStrategy(ABC):
    @abstractmethod
    def label(self, data: pd.DataFrame) -> pd.DataFrame:
        pass

class DataProcessorStrategy(ABC):
    @abstractmethod
    def process(self, data: pd.DataFrame) -> pd.DataFrame:
        pass

class DataSplitterStrategy(ABC):
    @abstractmethod
    def split(self, data: pd.DataFrame) -> Tuple[pd.Series, pd.Series, pd.Series, pd.Series]:
        pass

class TrainerStrategy(ABC):
    @abstractmethod
    def train(self, X_train: pd.Series, y_train: pd.Series) -> Pipeline:
        pass

class EvaluatorStrategy(ABC):
    @abstractmethod
    def evaluate(self, model: Pipeline, X_test: pd.Series, y_test: pd.Series) -> Dict[str, float]:
        pass

# Concrete Implementations
class TextBlobLabeling(LabelingStrategy):
    def label(self, data: pd.DataFrame) -> pd.DataFrame:
        def get_sentiment(text: str) -> int:
            analysis = TextBlob(text)
            return 1 if analysis.sentiment.polarity > 0 else 0
        
        data['sentiment'] = data['text'].apply(get_sentiment)
        return data

class BasicTextProcessor(DataProcessorStrategy):
    def process(self, data: pd.DataFrame) -> pd.DataFrame:
        data['text'] = data['text'].str.lower()
        data.dropna(inplace=True)
        return data

class BasicDataSplitter(DataSplitterStrategy):
    def split(self, data: pd.DataFrame) -> Tuple[pd.Series, pd.Series, pd.Series, pd.Series]:
        X_train, X_test, y_train, y_test = train_test_split(
            data['text'], data['sentiment'], test_size=0.2, random_state=42
        )
        return X_train, X_test, y_train, y_test

class SklearnPipelineTrainer(TrainerStrategy):
    def train(self, X_train: pd.Series, y_train: pd.Series) -> Pipeline:
        pipeline = Pipeline([
            ('vectorizer', TfidfVectorizer()),
            ('classifier', LogisticRegression())
        ])
        pipeline.fit(X_train, y_train)
        return pipeline

class ModelEvaluator(EvaluatorStrategy):
    def evaluate(self, model: Pipeline, X_test: pd.Series, y_test: pd.Series) -> Dict[str, float]:
        y_pred: np.ndarray = model.predict(X_test)
        acc: float = accuracy_score(y_test, y_pred)
        f1: float = f1_score(y_test, y_pred, average='weighted')
        return {'accuracy': acc, 'f1_score': f1}

