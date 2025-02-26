from typing import Tuple, Dict

from botocore.client import BaseClient
import boto3
from zenml import step, pipeline
import pandas as pd
from sklearn.pipeline import Pipeline

from my_package.mlworkflow import (LabelingStrategy, TextBlobLabeling, 
                                   DataProcessorStrategy, BasicTextProcessor, 
                                   DataSplitterStrategy, BasicDataSplitter,
                                   TrainerStrategy, SklearnPipelineTrainer,
                                   EvaluatorStrategy, ModelEvaluator, DataLoadingStrategy, LoadDatasetFromS3)
import mlflow


@step
def load_data_step(bucket:str, path:str) -> pd.DataFrame:
    client : BaseClient = ...
    data_loader : DataLoadingStrategy = LoadDatasetFromS3(client=client, bucket=bucket)
    data : pd.DataFrame = data_loader.load_data(path = path)
    return data

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

@step(experiment_tracker="mlflow_tracker")
def train_model_step(X_train: pd.Series, y_train: pd.Series) -> Pipeline:
    mlflow.autolog()
    trainer: TrainerStrategy = SklearnPipelineTrainer()
    return trainer.train(X_train, y_train)

@step
def evaluate_model_step(model: Pipeline, X_test: pd.Series, y_test: pd.Series) -> Dict[str, float]:
    evaluator: EvaluatorStrategy = ModelEvaluator()
    return evaluator.evaluate(model, X_test, y_test)

@pipeline
def sentiment_analysis_pipeline(data: pd.DataFrame) -> None:
    labeled_data: pd.DataFrame = label_data_step(data)
    processed_data: pd.DataFrame = process_data_step(labeled_data)
    X_train, X_test, y_train, y_test = split_data_step(processed_data)
    model = train_model_step(X_train, y_train)
    results: Dict[str, float] = evaluate_model_step(model, X_test, y_test)

    # TODO: add mlflow for tracking experiments
    # TODO: add mlflow to register model
    print("Evaluation Results:", results)