import pytest
import responses

from pbipy.models import Dataset, DatasetUserAccess


@responses.activate
def test_get_dataset(powerbi):
    responses.get(
        "https://api.powerbi.com/v1.0/myorg/datasets/cfafbeb1-8037-4d0c-896e-a46fb27ff229",
        body="""
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
        """,
        content_type="application/json",
    )

    dataset = powerbi.datasets.get_dataset("cfafbeb1-8037-4d0c-896e-a46fb27ff229")

    assert dataset.id == "cfafbeb1-8037-4d0c-896e-a46fb27ff229"
    assert dataset.name == "SalesMarketing"
    assert not dataset.add_rows_api_enabled
    assert dataset.is_refreshable


@responses.activate
def test_get_dataset_in_group_using_group_id(powerbi):
    responses.get(
        "https://api.powerbi.com/v1.0/myorg/groups/f089354e-8366-4e18-aea3-4cb4a3a50b48/datasets/cfafbeb1-8037-4d0c-896e-a46fb27ff229",
        body="""
        {
        "id": "cfafbeb1-8037-4d0c-896e-a46fb27ff229",
        "name": "SalesMarketing",
        "addRowsAPIEnabled": false,
        "configuredBy": "john@contoso.com",
        "isRefreshable": true,
        "isEffectiveIdentityRequired": false,
        "isEffectiveIdentityRolesRequired": false,
        "isOnPremGatewayRequired": false
        }
        """,
        content_type="application/json",
    )

    dataset = powerbi.datasets.get_dataset_in_group(
        "f089354e-8366-4e18-aea3-4cb4a3a50b48", "cfafbeb1-8037-4d0c-896e-a46fb27ff229"
    )

    assert isinstance(dataset, Dataset)
    assert dataset.id == "cfafbeb1-8037-4d0c-896e-a46fb27ff229"
    assert dataset.name == "SalesMarketing"
    assert dataset.configured_by == "john@contoso.com"
    assert dataset.is_refreshable
    assert not dataset.is_effective_identity_required
    assert not dataset.is_effective_identity_roles_required
    assert not dataset.is_on_prem_gateway_required

    # Keys not in the API response are set to None
    assert dataset.target_storage_mode == None
    assert dataset.upstream_datasets == None
    assert dataset.users == None


@responses.activate
def test_get_dataset_in_group_using_group_object(powerbi, group):
    responses.get(
        "https://api.powerbi.com/v1.0/myorg/groups/3d9b93c6-7b6d-4801-a491-1738910904fd/datasets/cfafbeb1-8037-4d0c-896e-a46fb27ff229",
        body="""
        {
        "id": "cfafbeb1-8037-4d0c-896e-a46fb27ff229",
        "name": "SalesMarketing",
        "addRowsAPIEnabled": false,
        "configuredBy": "john@contoso.com",
        "isRefreshable": true,
        "isEffectiveIdentityRequired": false,
        "isEffectiveIdentityRolesRequired": false,
        "isOnPremGatewayRequired": false,
        "upstreamDatasets": []
        }
        """,
        content_type="application/json",
    )

    dataset = powerbi.datasets.get_dataset_in_group(
        group, "cfafbeb1-8037-4d0c-896e-a46fb27ff229"
    )

    assert isinstance(dataset, Dataset)
    assert dataset.id == "cfafbeb1-8037-4d0c-896e-a46fb27ff229"
    assert dataset.name == "SalesMarketing"
    assert dataset.configured_by == "john@contoso.com"
    assert dataset.is_refreshable
    assert not dataset.is_effective_identity_required
    assert not dataset.is_effective_identity_roles_required
    assert not dataset.is_on_prem_gateway_required
    assert len(dataset.upstream_datasets) == 0

    # Keys not in the API response are set to None
    assert dataset.target_storage_mode == None
    assert dataset.users == None


@responses.activate
def test_get_datasets_in_group_using_group_id(powerbi):
    responses.get(
        "https://api.powerbi.com/v1.0/myorg/groups/f089354e-8366-4e18-aea3-4cb4a3a50b48/datasets",
        body="""
        {
        "value": [
            {
            "id": "cfafbeb1-8037-4d0c-896e-a46fb27ff229",
            "name": "SalesMarketing",
            "addRowsAPIEnabled": false,
            "configuredBy": "john@contoso.com",
            "isRefreshable": true,
            "isEffectiveIdentityRequired": false,
            "isEffectiveIdentityRolesRequired": false,
            "isOnPremGatewayRequired": false
            }
        ]
        }
        """,
        content_type="application/json",
    )

    datasets = powerbi.datasets.get_datasets_in_group(
        "f089354e-8366-4e18-aea3-4cb4a3a50b48"
    )

    assert len(datasets) == 1
    assert datasets[0].id == "cfafbeb1-8037-4d0c-896e-a46fb27ff229"
    assert hasattr(datasets[0], "is_effective_identity_roles_required")
    assert not datasets[0].is_effective_identity_roles_required


@responses.activate
def test_get_datasets_in_group_using_group_object(powerbi, group):
    responses.get(
        "https://api.powerbi.com/v1.0/myorg/groups/3d9b93c6-7b6d-4801-a491-1738910904fd/datasets",
        body="""
        {
        "value": [
            {
            "id": "cfafbeb1-8037-4d0c-896e-a46fb27ff229",
            "name": "SalesMarketing",
            "addRowsAPIEnabled": false,
            "configuredBy": "john@contoso.com",
            "isRefreshable": true,
            "isEffectiveIdentityRequired": false,
            "isEffectiveIdentityRolesRequired": false,
            "isOnPremGatewayRequired": false
            }
        ]
        }
        """,
        content_type="application/json",
    )

    datasets = powerbi.datasets.get_datasets_in_group(group)

    assert len(datasets) == 1
    assert datasets[0].id == "cfafbeb1-8037-4d0c-896e-a46fb27ff229"
    assert hasattr(datasets[0], "is_effective_identity_roles_required")
    assert not datasets[0].is_effective_identity_roles_required


@responses.activate
def test_get_refresh_history_from_dataset_object(powerbi, dataset):
    responses.get(
        "https://api.powerbi.com/v1.0/myorg/datasets/cfafbeb1-8037-4d0c-896e-a46fb27ff229/refreshes",
        body="""
        {
        "value": [
            {
            "refreshType": "ViaApi",
            "startTime": "2017-06-13T09:25:43.153Z",
            "endTime": "2017-06-13T09:31:43.153Z",
            "status": "Completed",
            "requestId": "9399bb89-25d1-44f8-8576-136d7e9014b1"
            },
            {
            "refreshType": "ViaApi",
            "startTime": "2017-06-13T09:25:43.153Z",
            "endTime": "2017-06-13T09:31:43.153Z",
            "serviceExceptionJson": "{\\"errorCode\\":\\"ModelRefreshFailed_CredentialsNotSpecified\\"}",
            "status": "Failed",
            "requestId": "11bf290a-346b-48b7-8973-c5df149337ff"
            }
        ]
        }
        """,
        content_type="application/json",
    )

    refresh_history = powerbi.datasets.get_refresh_history(dataset)

    assert len(refresh_history) == 2
    assert not refresh_history[0].service_exception_json
    assert refresh_history[1].service_exception_json


@responses.activate
def test_get_refresh_history_from_dataset_id(powerbi):
    """Test get_refresh_history retrieves the Dataset details before retrieving the refresh history."""

    dataset_get_request = responses.get(
        "https://api.powerbi.com/v1.0/myorg/datasets/cfafbeb1-8037-4d0c-896e-a46fb27ff229",
        body="""
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
        """,
        content_type="application/json",
    )

    responses.get(
        "https://api.powerbi.com/v1.0/myorg/datasets/cfafbeb1-8037-4d0c-896e-a46fb27ff229/refreshes",
        body="""
        {
        "value": [
            {
            "refreshType": "ViaApi",
            "startTime": "2017-06-13T09:25:43.153Z",
            "endTime": "2017-06-13T09:31:43.153Z",
            "status": "Completed",
            "requestId": "9399bb89-25d1-44f8-8576-136d7e9014b1"
            },
            {
            "refreshType": "ViaApi",
            "startTime": "2017-06-13T09:25:43.153Z",
            "endTime": "2017-06-13T09:31:43.153Z",
            "serviceExceptionJson": "{\\"errorCode\\":\\"ModelRefreshFailed_CredentialsNotSpecified\\"}",
            "status": "Failed",
            "requestId": "11bf290a-346b-48b7-8973-c5df149337ff"
            }
        ]
        }
        """,
        content_type="application/json",
    )

    dataset_id = "cfafbeb1-8037-4d0c-896e-a46fb27ff229"

    refresh_history = powerbi.datasets.get_refresh_history(dataset_id)

    assert dataset_get_request.call_count == 1
    assert len(refresh_history) == 2
    assert not refresh_history[0].service_exception_json
    assert refresh_history[1].service_exception_json


@responses.activate
def test_get_dataset_to_dataflow_links_in_group_from_group_id(powerbi):
    responses.get(
        "https://api.powerbi.com/v1.0/myorg/groups/f089354e-8366-4e18-aea3-4cb4a3a50b48/datasets/upstreamDataflows",
        body="""
        {
        "value": [
            {
            "datasetObjectId": "cfafbeb1-8037-4d0c-896e-a46fb27ff229",
            "dataflowObjectId": "928228ba-008d-4fd9-864a-92d2752ee5ce",
            "workspaceObjectId": "f089354e-8366-4e18-aea3-4cb4a3a50b48"
            }
        ]
        }
        """,
        content_type="application/json",
    )

    group_id = "f089354e-8366-4e18-aea3-4cb4a3a50b48"
    dataflow_links = powerbi.datasets.get_dataset_to_dataflow_links_in_group(group_id)

    assert len(dataflow_links) == 1
    assert hasattr(dataflow_links[0], "workspace_object_id")
    assert (
        dataflow_links[0].workspace_object_id == "f089354e-8366-4e18-aea3-4cb4a3a50b48"
    )


@responses.activate
def test_get_dataset_to_dataflow_links_in_group_from_group_object(powerbi, group):
    responses.get(
        "https://api.powerbi.com/v1.0/myorg/groups/3d9b93c6-7b6d-4801-a491-1738910904fd/datasets/upstreamDataflows",
        body="""
        {
        "value": [
            {
            "datasetObjectId": "cfafbeb1-8037-4d0c-896e-a46fb27ff229",
            "dataflowObjectId": "928228ba-008d-4fd9-864a-92d2752ee5ce",
            "workspaceObjectId": "f089354e-8366-4e18-aea3-4cb4a3a50b48"
            }
        ]
        }
        """,
        content_type="application/json",
    )

    dataflow_links = powerbi.datasets.get_dataset_to_dataflow_links_in_group(group)

    assert len(dataflow_links) == 1
    assert hasattr(dataflow_links[0], "workspace_object_id")
    assert (
        dataflow_links[0].workspace_object_id == "f089354e-8366-4e18-aea3-4cb4a3a50b48"
    )


@responses.activate
def test_get_dataset_users_from_dataset_id(powerbi):
    responses.get(
        "https://api.powerbi.com/v1.0/myorg/datasets/cfafbeb1-8037-4d0c-896e-a46fb27ff229/users",
        body="""
        {
        "value": [
            {
            "identifier": "john@contoso.com",
            "principalType": "User",
            "datasetUserAccessRight": "Read"
            },
            {
            "identifier": "154aef10-47b8-48c4-ab97-f0bf9d5f8fcf",
            "principalType": "Group",
            "datasetUserAccessRight": "ReadReshare"
            },
            {
            "identifier": "3d9b93c6-7b6d-4801-a491-1738910904fd",
            "principalType": "App",
            "datasetUserAccessRight": "ReadWriteReshareExplore"
            }
        ]
        }
        """,
    )

    dataset_id = "cfafbeb1-8037-4d0c-896e-a46fb27ff229"
    dataset_users = powerbi.datasets.get_dataset_users(dataset_id)

    assert len(dataset_users) == 3
    assert hasattr(dataset_users[0], "identifier")
    assert hasattr(dataset_users[1], "principal_type")
    assert hasattr(dataset_users[2], "dataset_user_access_right")
    assert isinstance(dataset_users[1], DatasetUserAccess)
    assert dataset_users[0].identifier == "john@contoso.com"
    assert dataset_users[1].principal_type == "Group"
    assert dataset_users[2].dataset_user_access_right == "ReadWriteReshareExplore"


@responses.activate
def test_get_dataset_users_from_dataset_object(powerbi, dataset):
    responses.get(
        "https://api.powerbi.com/v1.0/myorg/datasets/cfafbeb1-8037-4d0c-896e-a46fb27ff229/users",
        body="""
        {
        "value": [
            {
            "identifier": "john@contoso.com",
            "principalType": "User",
            "datasetUserAccessRight": "Read"
            },
            {
            "identifier": "154aef10-47b8-48c4-ab97-f0bf9d5f8fcf",
            "principalType": "Group",
            "datasetUserAccessRight": "ReadReshare"
            },
            {
            "identifier": "3d9b93c6-7b6d-4801-a491-1738910904fd",
            "principalType": "App",
            "datasetUserAccessRight": "ReadWriteReshareExplore"
            }
        ]
        }
        """,
    )

    dataset_users = powerbi.datasets.get_dataset_users(dataset)

    assert len(dataset_users) == 3
    assert hasattr(dataset_users[0], "identifier")
    assert hasattr(dataset_users[1], "principal_type")
    assert hasattr(dataset_users[2], "dataset_user_access_right")
    assert isinstance(dataset_users[1], DatasetUserAccess)
    assert dataset_users[0].identifier == "john@contoso.com"
    assert dataset_users[1].principal_type == "Group"
    assert dataset_users[2].dataset_user_access_right == "ReadWriteReshareExplore"


def test_get_refresh_history_raises_type_error_on_not_refreshable_dataset(
    powerbi, dataset_not_refreshable
):
    with pytest.raises(TypeError):
        powerbi.datasets.get_refresh_history(dataset_not_refreshable)