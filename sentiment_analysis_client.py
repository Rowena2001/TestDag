# file name: sentiment_analysis_client.py

# TO RUN AND TEST ON RAY SERVE: 
# serve run sentiment_analysis:deployment
# python sentiment_analysis_client.py

import requests



# 3: Query the deployment and print the result.
print(
    "HUGGING FACE MODEL cardiffnlp/twitter-roberta-base-sentiment",
    "\nLABEL_O = Negative, LABEL_1 = Neutral, LABEL_2 = Positive"
    "\n", requests.get("http://localhost:8000/", params={"text": "Ray Serve is great!"}).json(),
    "\n", requests.get("http://localhost:8000/", params={"text": "I'm feeling blue."}).json(),
    "\n", requests.get("http://localhost:8000/", params={"text": "I'm feeling sad."}).json()
)
# {'label': 'POSITIVE', 'score': 0.9998476505279541}