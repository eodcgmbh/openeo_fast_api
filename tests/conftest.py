import os
from unittest import mock

import pytest
from fastapi import FastAPI
from requests_mock.contrib import fixture

from openeo_fastapi.api.app import OpenEOApi
from openeo_fastapi.client import models
from openeo_fastapi.client.core import OpenEOCore

pytestmark = pytest.mark.unit


@pytest.fixture(autouse=True)
def mock_settings_env_vars():
    with mock.patch.dict(
        os.environ, {"STAC_API_URL": "http://test-stac-api.mock.com/api/"}
    ):
        yield


@pytest.fixture()
def core_api():
    client = OpenEOCore(
        title="Test Api",
        description="My Test Api",
        backend_version="1",
        links=[
            models.Link(
                href="https://eodc.eu/",
                rel="about",
                type="text/html",
                title="Homepage of the service provider",
            )
        ],
        billing=models.Billing(
            currency="credits",
            default_plan="a-cloud",
            plans=[
                models.Plan(name="user", description="Subscription plan.", paid=True)
            ],
        ),
        endpoints=[
            models.Endpoint(
                path="/",
                methods=["GET"],
            ),
            models.Endpoint(
                path="/collections",
                methods=["GET"],
            ),
            models.Endpoint(
                path="/collections/{collection_id}",
                methods=["GET"],
            ),
        ],
    )

    api = OpenEOApi(client=client, app=FastAPI())

    return api