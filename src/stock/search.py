import os
from typing import List, Tuple

import requests

from stock import download


def set_config():
    os.environ["REPLICAS"] = os.environ.get("REPLICA", str(1))
    os.environ["SHARDS"] = os.environ.get("SHARDS", str(1))
    os.environ["WORKSPACE"] = os.environ.get("WORKSPACE", "./workspace")
    os.environ['JINA_PORT'] = os.environ.get('JINA_PORT', str(45678))


def post_search(query: str, top_k: int = 10):
    """
    Send a query string to the waiting search rest API on localhost.
    Return a set of images (and their description)

    It is assumed that the API returns the results in order of greatest
    relevance first.
    """
    port = os.environ["JINA_PORT"]
    url = f"http://localhost:{port}/api/search"
    payload = {"top_k": top_k, "mode": "search", "data": [f"text:{query}"]}
    response = requests.post(url, json=payload)
    docs = [doc["matchDoc"]["text"].rstrip() for doc in response.json()["search"]["docs"][0]["topkResults"]]

    return docs


def split_results(documents: List[str]) -> Tuple[List[str], List[str]]:
    urls = []
    captions = []

    for doc in documents:
        photo = download.decode_photo_object(doc)
        photographer = photo["photographer"]
        main_url = photo["url"]
        url = photo["src"][download.PHOTO_SIZE]
        caption = photo["description"] + f". Photo by {photographer}. {main_url}"

        urls.append(url)
        captions.append(caption)

    return urls, captions
