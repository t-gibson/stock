"""
Streamlit App for displaying results.
"""

import logging

import requests
import streamlit as st

from design_search import search


logger = logging.getLogger(__name__)


pexels_reference = """
<a href="https://www.pexels.com">Photos provided by Pexels</a>
"""


def main():
    search.set_config()
    st.title("Semantic Search for Stock Images")

    st.write(pexels_reference, unsafe_allow_html=True)

    query = st.text_input("Search for a stock image")
    top_k = st.number_input("How many results should be returned?", min_value=1, max_value=10, value=5)

    outputs = st.empty()

    if query:
        response = search.post_search(query, top_k)
        urls, captions = search.split_results(response)
        images = [load_image(url) for url in urls]
        outputs.image(images, captions, use_column_width=True)


@st.cache(show_spinner=True)
def load_image(url) -> bytes:
    """
    Load an image from a url.

    Returns:
        bytes: The raw bytes of an image.
    """
    logger.debug(f"Loading image from {url}")
    response = requests.get(url)
    return response.content


if __name__ == "__main__":
    main()
