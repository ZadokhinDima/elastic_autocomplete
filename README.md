This is a simple python demo for autocompele implementation using Elastic Search.

It will return up to 10 suggestions for input.
First step is to fetch results by full prefix match. If there are less then 10 results fuzzy search is also performed. It will return long words (>= 7 chars) with not more then 3 typos. 

Index `words` was created with the next configuration:
```
{
  "settings": {
    "analysis": {
      "analyzer": {
        "autocomplete": {
          "type": "custom",
          "tokenizer": "standard",
          "filter": ["lowercase", "autocomplete_filter"]
        }
      },
      "filter": {
        "autocomplete_filter": {
          "type": "edge_ngram",
          "min_gram": 1,
          "max_gram": 20
        }
      }
    }
  },
  "mappings": {
    "properties": {
      "text": {
        "type": "text",
        "analyzer": "autocomplete",
        "search_analyzer": "standard"
      },
      "text_length": {
        "type": "integer"
      }
    }
  }
}
```