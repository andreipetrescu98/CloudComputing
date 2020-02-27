import requests
from multiprocessing import Pool

"""
https://skipperkongen.dk/2016/09/09/easy-parallel-http-requests-with-python-and-asyncio/
https://hackernoon.com/how-to-run-asynchronous-web-requests-in-parallel-with-python-3-5-without-aiohttp-264dc0f8546

https://realpython.com/python-concurrency/
"""

words_to_search = ['dog', 'cloud', 'blue sky', 'wild animals', 'house', 'parrot', 'Iasi', 'Romania', 'cat', 'winter'] * 50

def todo(word_to_search):
    response = requests.get("http://127.0.0.1:8080/data/{}".format(word_to_search))
    response.raise_for_status()


if __name__ == '__main__':
    for i in range(2):
        pool = Pool(50)
        print(pool)
        pool.map(todo, words_to_search)
    
