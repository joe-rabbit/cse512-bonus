from flask import Flask, request, jsonify
from elasticsearch import Elasticsearch,helpers
from openai import OpenAI
import threading
from urllib.request import urlopen
import json
import os
import numpy as np
from gtts import gTTS
from scipy.stats import norm
from urllib.request import urlopen
from flask_cors import CORS
# Initialize Flask app
import requests
from sentence_transformers import SentenceTransformer

model = SentenceTransformer("all-MiniLM-L6-v2")
app = Flask(__name__)
CORS(app)
# Set up OpenAI and Elasticsearch clients
API_KEY = <YOUR_OPENAI_API>
ELASTIC_CLOUD_ID = <YOUR_cLOUD_API>
ELASTIC_API_KEY = <YOUR_ELASTIC_API>
client = Elasticsearch(
    cloud_id = ELASTIC_CLOUD_ID ,
    api_key = ELASTIC_API_KEY
)
openai_client = OpenAI(
    api_key=API_KEY,
)
# url ="https://raw.githubusercontent.com/linuxacademy/content-elasticsearch-deep-dive/refs/heads/master/sample_data/shakespeare.json"
# Ensure the folder for saving MP3 files exists
MP3_FOLDER = "mp3_files"
if not os.path.exists(MP3_FOLDER):
    os.makedirs(MP3_FOLDER)

#THIS SECTION OF THE CODE NEEDS TO BE RUN THE FIRST TIME , COMMENT AFTER SECOND RUN - IT TAKES A WHILE..TO PERFORM INDEXING
# response = requests.get(url)
# if response.status_code == 200:
#   data = response.text.splitlines()
# else:
#   print("FAILURE!!")
# openai_client = OpenAI(api_key=API_KEY)
# client = Elasticsearch(
#     cloud_id=ELASTIC_CLOUD_ID,
#             api_key=ELASTIC_API_KEY,
# )
# mapping = {
#   "mappings": {
#     "properties": {
#       "type": {
#         "type": "keyword"
#       },
#       "line_id": {
#         "type": "integer"
#       },
#       "play_name": {
#         "type": "text"
#       },
#       "speech_number": {
#         "type": "integer"
#       },
#       "line_number": {
#         "type": "text"
#       },
#       "speaker": {
#         "type": "text"
#       },
#       "text_entry": {
#         "type": "text"
#       },
#       "embedding": {
#         "type": "dense_vector",
#         "dims": 384
#       }
#     }
#   }
# }

# # Assuming `data` is a list of lines read from the Shakespeare JSON file
# bulk_data = []
# for i in range(0, len(data), 2):  # Process two lines at a time
#     metadata = json.loads(data[i])  # Parse the metadata line
#     record = json.loads(data[i + 1])  # Parse the record line

#     # Generate embedding if `text_entry` exists
#     if "text_entry" in record and record["text_entry"]:
#         embedding = model.encode(record["text_entry"]).tolist()
#         record['embedding'] = embedding

#     # Add to bulk_data
#     bulk_data.append({
#         "_op_type": "index",
#         "_index": metadata["index"]["_index"],
#         "_id": metadata["index"]["_id"],
#         **record
#     })
#     helpers.bulk(client, bulk_data)
# Flask route for handling queries
@app.route('/ask', methods=['POST'])
def get_query():
    QUERY = request.json
    
    print('THE QUERY IS:',QUERY)
    # Perform KNN search (dummy example since exact search is missing)
    # Replace this part with the actual Elasticsearch query
    query_vector = model.encode([QUERY['message']]).tolist()[0]

    response = client.search(
    index="shakespeare",
    query={
        "knn": {
            "field": "embedding",
            "query_vector": query_vector,
            "k": 1,
            "num_candidates": 10
        }
    }
)

    
    if not response["hits"]["hits"]:
        return jsonify({"error": "No results found"}), 404

    for hit in response['hits']['hits']:
        print(f"Passing to GPT: Score: {hit['_score']}, Text: {hit['_source']['text_entry']}")

        # Create the GPT prompt
        gpt_prompt = f"""
        I have retrieved a line from a Shakespeare database based on a KNN search with the query '{QUERY}'.
        Here is the closest result:

        Score: {hit['_score']}
        Text: {hit['_source']['text_entry']}

        Please provide an analysis or interpretation of the retrieved line in the context of Shakespeare's works, focusing on themes and language style.
        """

        text_entry = hit['_source']['text_entry']
  

        response = openai_client.chat.completions.create(
            model="gpt-4o",
            messages=[
                {"role": "system", "content": "You are a specialized text extraction tool."},
                {"role": "user", "content": gpt_prompt},
            ]
        )

     
        response_text = response.choices[0].message.content.strip()
        tts = gTTS(response_text, lang='en', slow=False)
        audio_path = os.path.join(MP3_FOLDER, "trail.mp3")
        tts.save(audio_path)
        return jsonify({
            "response": response_text,
            "audio_file": audio_path
        })

if __name__ == "__main__":
    app.run(debug=True)