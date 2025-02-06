from typing import Dict

import pandas as pd
from sklearn.pipeline import Pipeline

from .mlworkflow import (LabelingStrategy, DataProcessorStrategy, DataSplitterStrategy, TrainerStrategy,
                          EvaluatorStrategy, TextBlobLabeling, BasicDataSplitter, BasicTextProcessor, 
                          SklearnPipelineTrainer, ModelEvaluator)



class SentimentAnalysisPipeline:
    def __init__(
        self,
        labeling_strategy: LabelingStrategy,
        processing_strategy: DataProcessorStrategy,
        splitting_strategy: DataSplitterStrategy,
        training_strategy: TrainerStrategy,
        evaluation_strategy: EvaluatorStrategy
    ) -> None:
        self.labeling_strategy = labeling_strategy
        self.processing_strategy = processing_strategy
        self.splitting_strategy = splitting_strategy
        self.training_strategy = training_strategy
        self.evaluation_strategy = evaluation_strategy

    def run(self, data: pd.DataFrame) -> Dict[str, float]:
        labeled_data: pd.DataFrame = self.labeling_strategy.label(data)
        processed_data: pd.DataFrame = self.processing_strategy.process(labeled_data)
        X_train, X_test, y_train, y_test = self.splitting_strategy.split(processed_data)
        model: Pipeline = self.training_strategy.train(X_train, y_train)
        results: Dict[str, float] = self.evaluation_strategy.evaluate(model, X_test, y_test)
        return results