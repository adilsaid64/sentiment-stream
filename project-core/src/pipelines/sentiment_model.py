from typing import Tuple, Dict

from zenml import step, pipeline
import pandas as pd
from sklearn.pipeline import Pipeline

from my_package.mlworkflow import (LabelingStrategy, TextBlobLabeling, 
                                   DataProcessorStrategy, BasicTextProcessor, 
                                   DataSplitterStrategy, BasicDataSplitter,
                                   TrainerStrategy, SklearnPipelineTrainer,
                                   EvaluatorStrategy, ModelEvaluator)

# ZenML Steps
@step
def label_data_step(data: pd.DataFrame) -> pd.DataFrame:
    labeler: LabelingStrategy = TextBlobLabeling()
    return labeler.label(data)

@step
def process_data_step(data: pd.DataFrame) -> pd.DataFrame:
    processor: DataProcessorStrategy = BasicTextProcessor()
    return processor.process(data)

@step
def split_data_step(data: pd.DataFrame) -> Tuple[pd.Series, pd.Series, pd.Series, pd.Series]:
    splitter: DataSplitterStrategy = BasicDataSplitter()
    return splitter.split(data)

@step
def train_model_step(X_train: pd.Series, y_train: pd.Series) -> Pipeline:
    trainer: TrainerStrategy = SklearnPipelineTrainer()
    return trainer.train(X_train, y_train)

@step
def evaluate_model_step(model: Pipeline, X_test: pd.Series, y_test: pd.Series) -> Dict[str, float]:
    evaluator: EvaluatorStrategy = ModelEvaluator()
    return evaluator.evaluate(model, X_test, y_test)

# ZenML Pipeline
@pipeline
def sentiment_analysis_pipeline(data: pd.DataFrame) -> None:
    labeled_data: pd.DataFrame = label_data_step(data)
    processed_data: pd.DataFrame = process_data_step(labeled_data)
    X_train, X_test, y_train, y_test = split_data_step(processed_data)
    model = train_model_step(X_train, y_train)
    results: Dict[str, float] = evaluate_model_step(model, X_test, y_test)
    print("Evaluation Results:", results)