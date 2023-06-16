# File name: serve_deployment.py
from starlette.requests import Request

import ray
from ray import serve
from ray.serve.deployment_graph import RayServeDAGHandle

from transformers import pipeline

@serve.deployment(num_replicas=1, ray_actor_options={"num_gpus": 0.2})
class Translator:
    def __init__(self):
        # Load model
        print("hello1")
        self.model = pipeline("translation_en_to_fr", model="t5-small", device="cuda:1")
        print("hello2")

    def translate(self, text: str) -> str:
        # Run inference
        model_output = self.model(text)

        # Post-process output to return only the translation text
        translation = model_output[0]["translation_text"]

        return translation

    async def __call__(self, http_request: Request) -> str:
        english_text: str = await http_request.json()
        translation = self.translate(english_text)
        return translation

@serve.deployment(ray_actor_options={"num_cpus": 0.2})
class BasicDriver:
    def __init__(self, dag: RayServeDAGHandle):
        self.dag = dag

    async def __call__(self, http_request: Request):
        object_ref = await self.dag.remote(http_request)
        result = await object_ref
        return result

translator_app = Translator.bind()
# translation = translator_app.translate.bind()
DagNode = BasicDriver.bind(translator_app)