"""
Module containing the main entry point to this project.
"""

import logging
import os
import subprocess as sp
from typing import Dict, List, Optional, Tuple

import click
import click_log
from dotenv import load_dotenv

from stock.version import __version__


logger = logging.getLogger("stock")
click_log.basic_config(logger)


DOTENV_PATH = ".env"
if os.path.exists(DOTENV_PATH):
    load_dotenv(DOTENV_PATH)


CONTEXT_SETTINGS = dict(auto_envvar_prefix="SEARCH")


@click.command()
@click.password_option("--api-token", help="The token for the Pexels API.", required=True)
@click.option("--output-csv", help="The file in which to save the results.", required=True)
@click.option("-n", "--num-results", default=15, help="The number of results to return for each QUERY", show_default=True)
@click.option("-p", "--page", default=1, help="The number of the page that you are requesting.", show_default=True)
@click.option("--append/--no-append", default=True, help="Append to the output csv if already exists", show_default=True)
@click.option(
    "-q",
    "--query-page-logs",
    default=None,
    help="Read and write the page each QUERY is up to in a file.This will be prioritised over the --page option"
)
@click.argument("queries", nargs=-1)
def download(
    api_token: str,
    queries: Tuple[str],
    output_csv: str,
    num_results: int,
    page: int,
    query_page_logs: Optional[str],
    append: bool
) -> None:
    """
    Download info on stock images based on a list of QUERYs. Save the results to a csv.
    """
    from stock import download

    if not queries:
        logger.warning("No QUERYs have been passed. Nothing to do.")

    total_requests = len(queries) * num_results
    if total_requests > 200:
        raise Exception(
            "The Pexels API is rate-limited to 200 requests an hour.\n"
            f"You are attempting to run {total_requests} requests.\n"
            "Reduce the number of QUERYs you use or decrease your value for num-results."
        )


    # read in a csv file of '<query>,<page>' per row to prioritise as the page to read per query
    query_current_page: Dict[str, int] = {}
    if query_page_logs and os.path.exists(query_page_logs):
        with open(query_page_logs) as f:
            for line in f:
                query, query_page = line.split(",")
                query_current_page[query] = int(query_page)

    docs: List[str] = []

    for query in queries:
        effective_page: int = query_current_page.get(query, page)
        photos = download.get_photos(api_token, query, effective_page, num_results)
        # record in the query page log file the next page to query i.e. page + 1
        query_current_page[query] = int(effective_page) + 1
        docs += [download.encode_photo_object(photo, query) for photo in photos]

    if query_page_logs:
        dir_ = os.path.dirname(query_page_logs)
        if dir_:
            os.makedirs(dir_, exist_ok=True)
        with open(query_page_logs, "w") as f:
            f.writelines(f"{query},{page}\n" for query, page in query_current_page.items())

    # Construct the directory if needed.
    dir_ = os.path.dirname(output_csv)
    if dir_:
        os.makedirs(dir_, exist_ok=True)

    with open(output_csv, "a" if append else "w") as f:
        # we ensure that there is a newline at the end of the file
        f.writelines(doc + "\n" for doc in docs)


@click.command()
@click.option('--workspace', help="Folder path in which to save index results.", required=True)
@click.option("--file", default="data/raw/pexels.csv")
@click.option('--num_docs', '-n', default=None, help="The maximum number of rows to index.")
def index(workspace, file, num_docs):
    """
    Index a file ready for searching.
    """
    try:
        from jina.flow import Flow
    except ImportError:
        raise ImportError("Jina is not installed. Did you install the package with .[app] extras?")
    from stock import search, utils

    num_docs: Optional[int] = int(num_docs) if num_docs is not None else num_docs

    yml = utils.resource_filename("flow-index.yml")
    os.environ["SRC"] = os.path.dirname(yml)
    os.environ["WORKSPACE"] = workspace

    search.set_config()
    flow = Flow().load_config(yml)
    logger.debug(f"Loading config from {yml}")
    with flow:
        flow.index_lines(filepath=file, batch_size=8, size=num_docs)


@click.command()
@click.option('--workspace', help="Folder path from which to load index results.", required=True)
def search(workspace):
    """
    Launch a neural search application to return the top-k search results
    given an input prompt.

    Requires install of package as stock[app]
    """
    try:
        from jina.flow import Flow
    except ImportError:
        raise ImportError("Jina is not installed. Did you install the package with .[app] extras?")
    from stock import search, utils

    yml = utils.resource_filename("flow-query.yml")
    os.environ["SRC"] = os.path.dirname(yml)
    os.environ["WORKSPACE"] = workspace

    search.set_config()
    flow = Flow().load_config(yml)
    with flow:
        with sp.Popen(["streamlit", "run", utils.resource_filename("app.py")]):
            flow.block()


@click.group(
    commands={"download": download, "index": index, "search": search},
    context_settings=CONTEXT_SETTINGS,
    invoke_without_command=True
)
@click.version_option(version=__version__)
@click_log.simple_verbosity_option(logger)
def main():
    level = logging.getLevelName(logger.level)
    logger.debug(f"Setting search app to have logging level: {level}")
    os.environ["JINA_LOG_VERBOSITY"] = level
