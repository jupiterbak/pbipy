import json

import pytest

from pbipy.models import App, Dashboard, Dataset, Gateway, Group, Refresh, Report, Tile


@pytest.fixture
def refresh_from_raw():
    raw = {
        "refreshType": "ViaApi",
        "startTime": "2017-06-13T09:25:43.153Z",
        "endTime": "2017-06-13T09:31:43.153Z",
        "serviceExceptionJson": '{"errorCode":"ModelRefreshFailed_CredentialsNotSpecified"}',
        "status": "Failed",
        "requestId": "11bf290a-346b-48b7-8973-c5df149337ff",
    }

    return Refresh.from_raw(raw=raw)


@pytest.fixture
def group_from_raw():
    raw = {
        "id": "3d9b93c6-7b6d-4801-a491-1738910904fd",
        "isReadOnly": False,
        "isOnDedicatedCapacity": False,
        "name": "marketing group",
    }

    return Group.from_raw(raw=raw)


@pytest.fixture
def dataset_from_raw():
    raw = {
        "id": "cfafbeb1-8037-4d0c-896e-a46fb27ff229",
        "name": "SalesMarketing",
        "addRowsAPIEnabled": False,
        "configuredBy": "john@contoso.com",
        "isRefreshable": True,
        "isEffectiveIdentityRequired": True,
        "isEffectiveIdentityRolesRequired": True,
        "isOnPremGatewayRequired": False,
        "createdDate": "2017-06-13T09:25:43.153Z",
    }

    return Dataset.from_raw(raw=raw)


@pytest.fixture
def group():
    return Group(id="3d9b93c6-7b6d-4801-a491-1738910904fd", name="marketing group")


@pytest.fixture
def dataset():
    js = json.loads(
        """
        {
        "id": "cfafbeb1-8037-4d0c-896e-a46fb27ff229",
        "name": "SalesMarketing",
        "addRowsAPIEnabled": false,
        "configuredBy": "john@contoso.com",
        "isRefreshable": true,
        "isEffectiveIdentityRequired": true,
        "isEffectiveIdentityRolesRequired": true,
        "isOnPremGatewayRequired": false
        }
        """
    )
    return Dataset.from_raw(js)


@pytest.fixture
def dataset_not_refreshable():
    js = json.loads(
        """
        {
        "id": "cfafbeb1-8037-4d0c-896e-a46fb27ff229",
        "name": "SalesMarketing",
        "addRowsAPIEnabled": false,
        "configuredBy": "john@contoso.com",
        "isRefreshable": false,
        "isEffectiveIdentityRequired": true,
        "isEffectiveIdentityRolesRequired": true,
        "isOnPremGatewayRequired": false
        }
        """
    )
    return Dataset.from_raw(js)


@pytest.fixture
def app_from_raw():
    js = json.loads(
        """
        {
        "id": "3d9b93c6-7b6d-4801-a491-1738910904fd",
        "description": "The marketing app",
        "name": "Marketing",
        "publishedBy": "Ben",
        "lastUpdate": "2018-11-13T09:46:53.094+02:00"
        }
    """
    )

    return App.from_raw(js)


@pytest.fixture
def report_from_raw():
    js = json.loads(
        """
    {
    "appId": "3d9b93c6-7b6d-4801-a491-1738910904fd",
    "datasetId": "cfafbeb1-8037-4d0c-896e-a46fb27ff229",
    "id": "66b2570c-d9d3-40b2-83d9-1095c6700041",
    "name": "SalesMarketing",
    "description":"The Sales and Marketing App",
    "isOwnedByMe": true,
    "webUrl": "https://app.powerbi.com/reports/66b2570c-d9d3-40b2-83d9-1095c6700041",
    "embedUrl": "https://app.powerbi.com/reportEmbed?reportId=66b2570c-d9d3-40b2-83d9-1095c6700041&appId=3d9b93c6-7b6d-4801-a491-1738910904fd&config=eyJjbHVzdGVyVXJsIjoiaHR0cHM6Ly9XQUJJLVNPVVRILUNFTlRSQUwtVVMtcmVkaXJlY3QuYW5hbHlzaXMud2luZG93cy5uZXQifQ",
    "users":[]
    }
    """
    )

    return Report.from_raw(js)


@pytest.fixture
def dashboard_from_raw():
    js = json.loads(
        """
        {
        "appId": "3d9b93c6-7b6d-4801-a491-1738910904fd",
        "id": "03dac094-2ff8-47e8-b2b9-dedbbc4d22ac",
        "displayName": "SalesMarketing",
        "embedUrl": "https://app.powerbi.com/dashboardEmbed?dashboardId=335aee4b-7b38-48fd-9e2f-306c3fd67482&appId=3d9b93c6-7b6d-4801-a491-1738910904fd&config=eyJjbHVzdGVyVXJsIjoiaHR0cHM6Ly9XQUJJLVNPVVRILUNFTlRSQUwtVVMtcmVkaXJlY3QuYW5hbHlzaXMud2luZG93cy5uZXQifQ%3d%3d",
        "isReadOnly": false,
        "users": [],
        "subscriptions": []
        }
        """
    )

    return Dashboard.from_raw(js)


@pytest.fixture
def tile_from_raw():
    js = json.loads(
        """
        {
        "id": "312fbfe9-2eda-44e0-9ed0-ab5dc571bb4b",
        "title": "SalesMarketingTile",
        "embedUrl": "https://app.powerbi.com/embed?dashboardId=69ffaa6c-b36d-4d01-96f5-1ed67c64d4af&tileId=312fbfe9-2eda-44e0-9ed0-ab5dc571bb4b&groupId=f089354e-8366-4e18-aea3-4cb4a3a50b48",
        "rowSpan": 0,
        "colSpan": 0,
        "reportId": "5b218778-e7a5-4d73-8187-f10824047715",
        "datasetId": "cfafbeb1-8037-4d0c-896e-a46fb27ff229"
    }
        """
    )

    return Tile.from_raw(js)

@pytest.fixture
def gateway_from_raw():
    js = json.loads(
        """
        {
        "id": "1f69e798-5852-4fdd-ab01-33bb14b6e934",
        "name": "My_Sample_Gateway",
        "type": "Resource",
        "publicKey": {
            "exponent": "AQAB",
            "modulus": "o6j2....cLk="
            }
        }
        """
    )

    return Gateway.from_raw(js)