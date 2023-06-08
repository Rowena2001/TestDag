# file name: sentiment_analysis.py

# TO RUN AND TEST ON RAY SERVE: 
# serve run sentiment_analysis:deployment
# python sentiment_analysis_client.py

from starlette.requests import Request
from typing import Dict

from transformers import pipeline

from ray import serve


# 1: Wrap the pretrained sentiment analysis model in a Serve deployment.
@serve.deployment(route_prefix="/")
class SentimentAnalysisDeployment:
    def __init__(self):
        self._model = pipeline("sentiment-analysis", model="cardiffnlp/twitter-roberta-base-sentiment")

    def __call__(self, request: Request) -> Dict:
        return self._model(request.query_params["text"])[0]


# 2: Deploy the deployment.
deployment = SentimentAnalysisDeployment.bind()