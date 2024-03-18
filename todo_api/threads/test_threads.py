import logging

import pytest

from config.config import URL_TODO
from helpers.rest_client import RestClient
from utils.logger import get_logger


LOGGER = get_logger(__name__, logging.DEBUG)

class TestThreads:
    @classmethod
    def setup_class(cls):
        LOGGER.debug("SetupClass method")
        cls.url_threads = f"{URL_TODO}/threads"
        cls.list_threads = []
        cls.rest_client = RestClient()
        # call method first token refresh_token if needed
        # call second method using token to generate access_token if needed

    def test_create_thread(self, test_log_name):
        response = self.rest_client.request("post", url=self.url_threads)
        id_project_created = response.json()["id"]
        self.list_threads.append(id_project_created)
        assert response.status_code == 200, "wrong status code, expected 200"

    def test_get_thread(self, create_thread, test_log_name):
        LOGGER.debug("Thread to read: %s", create_thread)
        url_todo_get = f"{self.url_threads}/{create_thread}"
        response = self.rest_client.request("get", url=url_todo_get)
        self.list_threads.append(create_thread)
        assert response.status_code == 200, "wrong status code, expected 200"

    def test_delete_thread(self, create_thread, test_log_name):

        url_todo = f"{self.url_threads}/{create_thread}"
        LOGGER.debug("URL to delete: %s", url_todo)

        response = self.rest_client.request("delete", url=url_todo)
        # In the case of Open AI it returns status 200 when a thread is deleted
        assert response.status_code == 200, "wrong status code, expected 200"

    def test_update_thread(self, create_thread, test_log_name):

        LOGGER.debug("Thread to update: %s", create_thread)
        url_todo_update = f"{self.url_threads}/{create_thread}"
        body_thread = {
            "metadata": {
                "modified": "true",
                "user": "abc123"
            }
        }
        response = self.rest_client.request_json("post", url=url_todo_update, body=body_thread)

        # add to list of threads to be deleted in cleanup
        self.list_threads.append(create_thread)
        assert response.status_code == 200, "wrong status code, expected 200"

    @classmethod
    def teardown_class(cls):
        """
        Delete all threads used in test
        """
        LOGGER.info("Cleanup threads...")
        for id_project in cls.list_threads:
            url_delete_project = f"{URL_TODO}/threads/{id_project}"
            response = cls.rest_client.request("delete", url=url_delete_project)
            if response.status_code == 204:
                LOGGER.info("Thread: %s deleted", id_project)
