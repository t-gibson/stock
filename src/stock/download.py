"""
Module for downloading images from the Pexels Api.

The images are found based on a range of query terms.
The results are stored to generate the image and the image name.

API Reference: https://www.pexels.com/api/
"""


import logging
import re

from typing import List, Optional

import requests

logger = logging.getLogger(__name__)

SEP = "[SEP]"
PHOTO_SIZE = "large"


# TODO: add in retrying with backoff
def get_photos(api_token: str, query: str, page: int = 1, num_results: int = 15) -> List[dict]:
    """
    Returns the n-length list of Photo objects from
    the Pexels API.

    Args:
        api_token (str): The API authorization token.
        query (str): The query string,
        page (int): The number of the page that you are requesting.
        num_results (int, optional): Customise the number of results to return.

    Returns:
        list of dict: A list of json objects representing images.
    """
    assert num_results <= 80, "The max querying per page is 80"

    url = "https://api.pexels.com/v1/search"
    params = {"query": query, "per_page": num_results, "page": page}
    headers = {"Authorization": api_token}

    logger.debug(f"Logging request with params: {params}")

    response = requests.get(url, params=params, headers=headers)

    logger.debug(response.headers)

    photos = response.json()["photos"]

    if not photos:
        logger.warning(f"Empty list of photos returned. Perhaps, page={page} is too high.")

    return photos


def encode_photo_object(photo: dict, query: Optional[str] = None) -> str:
    """
    Encode the Pexels API Photo object into a single text string

    Args:
        photo (dict): The Photo object returned by the Pexels API.
        query (str, optional): The query string that this image was found by.
            If provided, this string will be appended to the image's description.
    """
    photographer = photo["photographer"]
    main_url = encode_url(photo["url"])
    image_url = encode_url(photo["src"][PHOTO_SIZE])
    description = get_image_description(photo["url"])

    if query:
        description += f". {query}."

    return SEP.join([photographer, main_url, image_url, description])


def decode_photo_object(string: str) -> dict:
    """
    Decode the Pexels API Photo object from a string.
    """
    photographer, main_url, image_url, description = string.split(SEP)
    return {
        "photographer": photographer,
        "url": decode_url(main_url),
        "description": description,
        "src": {
            PHOTO_SIZE: decode_url(image_url)
        }
    }


def get_image_description(image_url: str) -> str:
    """
    Extract the text description of the image from it's url.
    """
    regex = r"https://www.pexels.com/photo/([^/]+)-[0-9]+/$"
    logger.debug(f"Getting description from: {image_url}")
    try:
        group = re.match(regex, image_url).group(1)
    except AttributeError as e:
        logger.error(f"Can't extract image description from {image_url}")
        raise e
    return group.replace("-", " ").strip()


def encode_url(url: str) -> str:
    """
    Sanitise the url for searching. Which is able to be parsed by downstream steps.

    Was having issues with the full url.
    """
    return (
        url
        .replace(":", "[COLON]")
        .replace("/", "[SLASH]")
        .replace(".", "[DOT]")
    )


def decode_url(sanitised_url: str) -> str:
    return(
        sanitised_url
        .replace("[COLON]", ":")
        .replace("[SLASH]", "/")
        .replace("[DOT]", ".")
    )
