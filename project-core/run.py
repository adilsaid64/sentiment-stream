from src.my_package.mlworkflow import TextBlobLabeling, BasicTextProcessor, BasicDataSplitter, SklearnPipelineTrainer, ModelEvaluator
from src.my_package.mlpipeline import SentimentAnalysisPipeline
import pandas as pd 

data : pd.DataFrame = pd.read_csv("../twitter-streamer/data/twitter_dataset.csv").rename(columns = {"Text":"text"}) # connect to some data
print(data)
data = pd.DataFrame(data['text'])
pipeline = SentimentAnalysisPipeline(
    labeling_strategy=TextBlobLabeling(),
    processing_strategy=BasicTextProcessor(),
    splitting_strategy=BasicDataSplitter(),
    training_strategy=SklearnPipelineTrainer(),
    evaluation_strategy=ModelEvaluator()
)

results = pipeline.run(data)

print("Evaluation Results:", results)
