import requests
import json
import os
import logging

# https://rapidapi.com/microsoft-azure/api/microsoft-computer-vision
NLP_API = "https://microsoft-azure-microsoft-computer-vision-v1.p.rapidapi.com/describe"

# https://api.random.org/dashboard/details
RANDOMORG_API = "https://api.random.org/json-rpc/1/invoke"

# https://unsplash.com/oauth/applications/117014
UNSPLASH_API = "https://api.unsplash.com/search/photos"


configs = json.load(open(os.path.join(os.path.dirname(__file__), 'config.json')))
logging.basicConfig(filename=os.path.join(os.path.dirname(__file__), 'logging_info.log'), level=logging.INFO)
# to_search = input("Search photo: ")

LOGS = []

def get_metrics():
    # print(LOGS)
    total_requests = len(LOGS)
    total_ok_status_code = len(list(filter(lambda x: x[0] == 200, LOGS)))

    # print(list(zip(*LOGS)))
    average_latency = sum(list(zip(*LOGS))[1]) / total_requests
    ok_status_code_ratio = total_ok_status_code / total_requests

    return {"OK_STATUS_CODE_RATIO": ok_status_code_ratio, "AVG_LATENCY_SECONDS": average_latency}

def log_info(response):
    method = response.request.method
    status_code = response.status_code
    latency = response.elapsed.total_seconds()

    LOGS.append((status_code, latency))
    
    logging.info('Request: {}\tResponse: {}\tLatency: {} seconds'.format(method, status_code, latency))

# Get a random integer
def get_random_integer(max_integer):
    request_data = {
        "jsonrpc": "2.0",
        "method": "generateIntegers",
        "params": {
            "apiKey": configs['RANDOMORG_API_KEY'],
            "n": 1,
            "min": 0,
            "max": max_integer-1,
            "replacement": True
        },
        "id": 42
    }

    response = requests.post(RANDOMORG_API, json=request_data)
    # response.raise_for_status()

    log_info(response)

    json_response = response.json()
    
    return json_response['result']['random']['data'][0]


# Get an image
def get_url_by_search(search_keyword):
    query_data = {"query": search_keyword, "client_id": configs['UNSPLASH_API_KEY']}

    response = requests.get(UNSPLASH_API, params=query_data)
    # response.raise_for_status()

    log_info(response)

    json_response = response.json()

    # print(len(json_response['results']))
    index = get_random_integer(len(json_response['results']))
    # print(index)

    return json_response['results'][index]['urls']['regular']


# Get description by image url
def get_image_description(img_url):
    payload = "{\"url\":\"" + img_url + "\"}"

    headers = {
        'x-rapidapi-host': "microsoft-azure-microsoft-computer-vision-v1.p.rapidapi.com",
        'x-rapidapi-key': configs['NLP_API_KEY'],
        'content-type': "application/json",
        'accept': "application/json"
        }

    response = requests.post(NLP_API, data=payload, headers=headers)
    # response.raise_for_status()

    log_info(response)

    json_response = response.json()
    # print(json_response)
    if len(json_response['description']['captions']) > 0:
        return json_response['description']['captions'][0]['text']
    else:
        return 'No image description was generated.'


# RANDOM_INTEGER = get_random_integer(10)
# IMG_URL = get_url_by_search(to_search)
# IMAGE_DESCRIPTION = get_image_description(IMG_URL).capitalize()

# print(RANDOM_INTEGER, IMG_URL)
# print("NLP description: ", IMAGE_DESCRIPTION)
