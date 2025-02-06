from src.my_package.mlworkflow import TextBlobLabeling, BasicTextProcessor, BasicDataSplitter, SklearnPipelineTrainer, ModelEvaluator
from src.my_package.mlpipeline import SentimentAnalysisPipeline
import pandas as pd 

data : pd.DataFrame = ... # connect to some data

pipeline = SentimentAnalysisPipeline(
    labeling_strategy=TextBlobLabeling(),
    processing_strategy=BasicTextProcessor(),
    splitting_strategy=BasicDataSplitter(),
    training_strategy=SklearnPipelineTrainer(),
    evaluation_strategy=ModelEvaluator()
)

results = pipeline.run(data)
print("Evaluation Results:", results)
