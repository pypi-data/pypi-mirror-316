import requests

from msfabricutils.core.auth import get_fabric_bearer_token


def get_paginated(endpoint: str, data_key: str) -> list[dict]:
    """
    Retrieves paginated data from the specified API endpoint.

    This function makes repeated GET requests to the specified endpoint of the
    Fabric REST API, handling pagination automatically. It uses a bearer token
    for authentication and retrieves data from each page, appending the results
    to a list. Pagination continues until no `continuationToken` is returned.

    Args:
        endpoint (str): The API endpoint to retrieve data from.
        data_key (str): The key in the response JSON that contains the list of data to be returned.

    Returns:
        A list of dictionaries containing the data from all pages.

    Raises:
        requests.exceptions.RequestException: If the HTTP request fails or returns an error.
    """
    base_url = "https://api.fabric.microsoft.com/v1"
    token = get_fabric_bearer_token()
    headers = {"Authorization": f"Bearer {token}"}

    responses = []
    continuation_token = None
    while True:
        params = {"continuationToken": continuation_token} if continuation_token else {}

        response = requests.get(f"{base_url}/{endpoint}", headers=headers, params=params)
        response.raise_for_status()
        data: dict = response.json()

        responses.extend(data.get(data_key))

        continuation_token = data.get("continuationToken")
        if not continuation_token:
            break

    return responses


def get_item_from_paginated(endpoint: str, data_key: str, item_key: str, item_value: str) -> list[dict]:
    """
    Recursively paginates the API endpoint until specified item is found and returns it.

    This function makes repeated GET requests to the specified endpoint of the
    Fabric REST API, handling pagination automatically. It uses a bearer token
    for authentication and retrieves data from each page, appending the results
    to a list. Pagination continues until the specified item is found or no
    `continuationToken` is returned.

    Args:
        endpoint (str): The API endpoint to retrieve data from.
        data_key (str): The key in the response JSON that contains the list of data to be returned.
        item_key (str): The key in the data dictionary that contains the item to be returned.
        item_value (str): The value of the item to be returned.

    Returns:
        A dictionary containing the item to be returned.

    Raises:
        requests.exceptions.RequestException: If the HTTP request fails or returns an error.
        ValueError: If the item is not found.
    """
    base_url = "https://api.fabric.microsoft.com/v1"
    token = get_fabric_bearer_token()
    headers = {"Authorization": f"Bearer {token}"}

    continuation_token = None
    while True:
        params = {"continuationToken": continuation_token} if continuation_token else {}

        response = requests.get(f"{base_url}/{endpoint}", headers=headers, params=params)
        response.raise_for_status()
        data: dict = response.json()

        for item in data.get(data_key):
            if item.get(item_key) == item_value:
                return item

        continuation_token = data.get("continuationToken")
        if not continuation_token:
            break

    raise ValueError(f"Item with {item_key} {item_value} not found")


def get_page(endpoint: str) -> list[dict]:
    """
    Retrieves data from a specified API endpoint.

    This function makes a GET request to the specified endpoint of the Azure Fabric API,
    using a bearer token for authentication. It returns the JSON response as a list of
    dictionaries containing the data returned by the API.

    Args:
        endpoint (str): The API endpoint to send the GET request to.

    Returns:
        A list of dictionaries containing the data returned from the API.

    Raises:
        requests.exceptions.RequestException: If the HTTP request fails or returns an error.
    """
    base_url = "https://api.fabric.microsoft.com/v1"
    token = get_fabric_bearer_token()
    headers = {"Authorization": f"Bearer {token}"}
    params = {}

    response = requests.get(f"{base_url}/{endpoint}", headers=headers, params=params)
    response.raise_for_status()

    return response.json()
