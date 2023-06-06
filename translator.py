# TO RUN ON RAY SERVER:
# serve build translator:serve_dag -o translator_config.yaml
# ray start --head
# serve deploy translator_config.yaml
# curl -H "Content-Type: application/json" -d '["Hello does the translator work?"]' "http://localhost:8000/"
# curl -H "Content-Type: application/json" -d '["The quick brown fox jumps over the lazy dog."]' "http://localhost:8000/"

from typing import List

from ray import serve
from ray.serve.deployment_graph import InputNode
from ray.serve.drivers import DAGDriver

import starlette.requests
from starlette.requests import Request

from transformers import pipeline

@serve.deployment(num_replicas=2, ray_actor_options={"num_cpus": 0.2, "num_gpus": 0})
class Translator:
    def __init__(self):
        # Load model
        self.model = pipeline("translation_en_to_fr", model="t5-small")

    def translate(self, text: str) -> str:
        # Run inference
        model_output = self.model(text)

        # Post-process output to return only the translation text
        translation = model_output[0]["translation_text"]

        return translation

    async def __call__(self, http_request: Request) -> str:
        english_text: str = await http_request.json()
        return self.translate(english_text)

async def json_resolver(request: starlette.requests.Request) -> List:
    return await request.json()

with InputNode() as inp:
    statement = inp[0]
    translator = Translator.bind()
    translated_statement = translator.translate.bind(statement)

serve_dag = DAGDriver.bind(translated_statement, http_adapter=json_resolver)