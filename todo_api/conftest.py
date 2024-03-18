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
    url_thread = URL_TODO+"/threads"
    rest_client = RestClient()
    response = rest_client.request("post", url_thread)
    thread_id = response.json()["id"]

    yield thread_id
    delete_thread(thread_id, rest_client)


@pytest.fixture()
def get_thread():
    rest_client = RestClient()
    response = rest_client.request("get", URL_TODO+"/threads")
    thread_id = response.json()[1]["id"]
    LOGGER.debug("Thread ID: %s", thread_id)
    return thread_id


@pytest.fixture()
def test_log_name(request):
    LOGGER.info("Test '%s' STARTED", request.node.name)

    def fin():
        LOGGER.info("Test '%s' COMPLETED", request.node.name)

    request.addfinalizer(fin)


def delete_thread(project_id, rest_client):
    LOGGER.info("Cleanup thread...")
    url_delete_thread = f"{URL_TODO}/threads/{project_id}"
    response = rest_client.request("delete", url=url_delete_thread)
    if response.status_code == 204:
        LOGGER.info("Thread Id: %s deleted", project_id)


def pytest_addoption(parser):
    parser.addoption(
        '--env', action='store', default='dev', help="Environment where the tests are executed"
    )
    parser.addoption(
        '--browser', action='store', default='chrome', help="Browser type to execute the UI tests"
    )
