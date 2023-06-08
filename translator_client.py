# file name: translator_client.py

# TO RUN AND TEST ON RAY SERVE: 
# serve run translator_deployment:deployment
# python translator_client.py

import requests

english_text = "Hello world!"

response = requests.post("http://127.0.0.1:8000/", json=english_text)
french_text = response.text

print(french_text)