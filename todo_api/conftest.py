import logging

import pytest
import requests

from config.config import URL_TODO, HEADERS_TODO
from helpers.rest_client import RestClient
from utils.logger import get_logger

LOGGER = get_logger(__name__, logging.DEBUG)


@pytest.fixture()
def create_thread(request):

    LOGGER.debug("Create thread")
    environment = request.config.getoption("--env")
    LOGGER.critical("Environment selected: %s", environment)
    url_project = URL_TODO+"/threads"
    rest_client = RestClient()
    response = rest_client.request("post", url_project)
    project_id = response.json()["id"]

    yield project_id
    delete_project(project_id, rest_client)


@pytest.fixture()
def test_log_name(request):
    LOGGER.info("Test '%s' STARTED", request.node.name)

    def fin():
        LOGGER.info("Test '%s' COMPLETED", request.node.name)

    request.addfinalizer(fin)


def delete_project(thread_id, rest_client):
    LOGGER.info("Cleanup project...")
    url_delete_project = f"{URL_TODO}/threads/{thread_id}"
    response = rest_client.request("delete", url=url_delete_project)
    if response.status_code == 204:
        LOGGER.info("Project Id: %s deleted", thread_id)
