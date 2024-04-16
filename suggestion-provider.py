from elasticsearch import Elasticsearch

# Connect to Elasticsearch
es = Elasticsearch(hosts=["http://localhost:9200"])

RESULTS_SIZE = 10


def generate_suggestions(text):
    result = get_full_prefix_match_suggestions(text)
    print(f'Full match: {result}')

    if len(result) == RESULTS_SIZE:
        return result
    
    suggestions_count = RESULTS_SIZE - len(result)
    typos_suggestions = get_suggestions_with_typos(text, suggestions_count)
    print(f'Fuzzy match: {typos_suggestions}')
    result.extend(typos_suggestions)

    return result

def get_full_prefix_match_suggestions(text):
    search_results = es.search(index="words", body={
        "size": RESULTS_SIZE, 
        "query": {
            "prefix": 
            {
                "text": text
            }
        }
    })
    suggestions = [hit["_source"]["text"] for hit in search_results["hits"]["hits"]]
    return suggestions

def get_suggestions_with_typos(text, suggestions_count):
    query =  {
            "bool": {
                "must": [
                   {
                        "range": {
                            "text_length": {
                                "gte": 7
                            }
                        }
                    },
                    {
                        "fuzzy": {
                            "text": {
                                "value": text,
                                "fuzziness": 3,
                                "prefix_length": 2,
                                "max_expansions": 50
                            }
                        }
                    }
                ],
                "must_not": [
                    {
                        "prefix": {
                            "text": text
                        }
                    }
                ]
            }
        }

    search_results = es.search(index="words", body={
        "size": suggestions_count,
        "query": query
    })
    suggestions = [hit["_source"]["text"] for hit in search_results["hits"]["hits"]]
    return suggestions

def main():
    while True:
        user_input = input('Input for suggestions: ')
        if user_input == 'exit':
            break
        suggested_inputs = generate_suggestions(user_input)
        print('Full result:', suggested_inputs)

if __name__ == '__main__':
    main()