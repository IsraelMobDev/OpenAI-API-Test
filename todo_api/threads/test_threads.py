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

    def test_delete_thread(self, create_project, test_log_name):

        url_todo = f"{self.url_threads}/{create_project}"
        LOGGER.debug("URL to delete: %s", url_todo)

        response = self.rest_client.request("delete", url=url_todo)

        assert response.status_code == 204, "wrong status code, expected 204"

    def test_update_thread(self, create_project, test_log_name):

        LOGGER.debug("Project to update: %s", create_project)
        url_todo_update = f"{self.url_threads}/{create_project}"
        body_project = {
            "name": "Update project"
        }
        response = self.rest_client.request("post", url=url_todo_update, body=body_project)

        # add to list of projects to be deleted in cleanup
        self.list_threads.append(create_project)
        assert response.status_code == 200, "wrong status code, expected 200"

    @classmethod
    def teardown_class(cls):
        """
        Delete all projects used in test
        """
        LOGGER.info("Cleanup threads...")
        for id_project in cls.list_threads:
            url_delete_project = f"{URL_TODO}/threads/{id_project}"
            response = cls.rest_client.request("delete", url=url_delete_project)
            if response.status_code == 204:
                LOGGER.info("Thread: %s deleted", id_project)
