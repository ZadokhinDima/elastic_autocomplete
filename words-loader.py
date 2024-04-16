from elasticsearch import Elasticsearch
from elasticsearch.helpers import bulk

# Connect to Elasticsearch
es = Elasticsearch(hosts=["http://localhost:9200"])

# Define the index name
index_name = "words"

# Open the file and read the lines
with open("words.txt", "r") as file:
    lines = file.readlines()

# Remove newline characters from each line
lines = [line.strip() for line in lines]

# Prepare the actions for the bulk API
actions = [
    {
        "_index": "words",
        "_source": {
            "text": line, 
            "text_length": len(line)
        }
    }
    for line in lines
]

try:
    response = bulk(es, actions)
    print("Indexed {} documents".format(response[0]))
except Exception as e:
    print("Error in bulk indexing: ", e)
